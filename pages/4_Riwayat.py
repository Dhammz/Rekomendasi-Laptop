"""
Riwayat Sesi — LaptopExpert
Menampilkan riwayat rekomendasi selama sesi aktif.
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ui_helpers import setup_page

setup_page("Riwayat Rekomendasi", icon="📜")

# ============================================================
# HEADER
# ============================================================

st.markdown("## 📜 Riwayat Rekomendasi Sesi")
st.info(
    "ℹ️ Riwayat hanya disimpan selama sesi aktif. "
    "Data akan hilang ketika Anda logout atau menutup browser."
)
st.divider()

# ============================================================
# TAMPILAN RIWAYAT
# ============================================================

riwayat = st.session_state.get("riwayat", [])

if not riwayat:
    st.warning("📭 Belum ada riwayat rekomendasi dalam sesi ini.")
    st.markdown("Mulai dengan mengklik **Rekomendasi Laptop** di sidebar.")
    if st.button("🔍 Mulai Rekomendasi Sekarang"):
        st.switch_page("pages/2_🔍_Rekomendasi.py")
else:
    st.success(f"📊 Total rekomendasi dalam sesi ini: **{len(riwayat)}**")
    st.markdown("")
    
    # Tampilkan dari yang terbaru
    for i, entry in enumerate(reversed(riwayat), 1):
        with st.expander(
            f"#{len(riwayat) - i + 1} — {entry['timestamp']} | {entry['kebutuhan_label']}",
            expanded=(i == 1)
        ):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Kebutuhan:** {entry['kebutuhan_label']}")
            with col2:
                st.markdown(f"**Anggaran:** {entry['kelas_label']}")
            with col3:
                st.markdown(f"**Hasil:** {entry['jumlah_hasil']} laptop ditemukan")
            
            if entry['jumlah_hasil'] > 0:
                st.markdown(f"**Hasil Teratas:** {entry['hasil_teratas']}")
            else:
                st.markdown("**Hasil:** Tidak ada laptop yang cocok")
            
            if entry.get('preferensi'):
                st.markdown(f"**Preferensi:** {', '.join(entry['preferensi'])}")
    
    if st.button("🗑️ Hapus Semua Riwayat", type="secondary"):
        st.session_state['riwayat'] = []
        st.success("Riwayat berhasil dihapus.")
        st.rerun()
