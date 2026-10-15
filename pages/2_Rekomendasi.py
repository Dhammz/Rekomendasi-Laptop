"""
2_Rekomendasi.py — Halaman Konsultasi & Rekomendasi (Modern & Interaktif)
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ui_helpers import setup_page, render_laptop_card, render_no_results, render_error_message
from services.prolog_engine import get_prolog_engine
from services.input_validator import validate_form, build_query
from services.result_formatter import (
    format_laptop_result, deduplicate_results, sort_results,
    format_query_info, add_to_history
)

setup_page("Rekomendasi Laptop", icon="🔍")

engine = get_prolog_engine()

if not engine.is_loaded:
    st.error(f"❌ Knowledge Base Prolog tidak tersedia: {engine.error_message}")
    st.stop()

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <h2 style="margin: 0; font-weight: 800; color: #0F172A; font-size: 1.85rem;">🔍 Konsultasi Pemilihan Laptop</h2>
    <p style="color: #64748B; font-size: 0.95rem; margin-top: 4px;">
        Tentukan profil penggunaan komputasi Anda. Mesin inferensi SWI-Prolog akan mencocokkan kriteria Anda dengan 70+ basis fakta.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FORM KONSULTASI
# ============================================================
with st.form("form_rekomendasi", clear_on_submit=False):
    st.markdown("""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 1.25rem 1.5rem; margin-bottom: 1rem;">
        <span style="font-weight: 700; color: #334155; font-size: 1rem;">📋 Parameter Kebutuhan Pengguna</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_form1, col_form2 = st.columns(2)
    
    with col_form1:
        st.markdown("**1. Kebutuhan Beban Kerja Utama** *(Wajib)*")
        kebutuhan_options = {
            "Pilih beban kerja...": None,
            "🖥️ Kuliah Umum & Produktivitas Dokumen": "office",
            "💻 Pemrograman & Pengembangan Perangkat Lunak": "koding",
            "🎨 Desain Grafis Ringan (Canva, Figma, Photoshop)": "editing_ringan",
            "🎬 Desain & Multimedia Berat (Video 4K, 3D Render)": "editing_berat",
            "🎮 Gaming Kompetitif & Game AAA": "gaming",
            "📡 Gaming Sambil Live Streaming (OBS)": "streaming",
            "📊 Data Science & Komputasi Machine Learning": "data_science",
            "🌐 Jaringan Komputer & Virtual Machine (VirtualBox/VMware)": "virtualisasi",
        }
        
        kebutuhan_label = st.selectbox(
            "Kebutuhan Utama",
            options=list(kebutuhan_options.keys()),
            label_visibility="collapsed"
        )
        kebutuhan_val = kebutuhan_options[kebutuhan_label]
    
    with col_form2:
        st.markdown("**2. Batasan Kelas Anggaran** *(Wajib)*")
        kelas_options = {
            "Pilih batas anggaran...": None,
            "🟢 Entry (Di bawah Rp 10.000.000)": "entry",
            "🔵 Midrange (Rp 10.000.000 – Rp 19.000.000)": "midrange",
            "🟣 High-End (Rp 20.000.000 – Rp 34.000.000)": "high_end",
            "🟡 Flagship (Rp 35.000.000 ke atas)": "flagship",
        }
        
        kelas_label = st.selectbox(
            "Rentang Anggaran",
            options=list(kelas_options.keys()),
            label_visibility="collapsed"
        )
        kelas_val = kelas_options[kelas_label]
    
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.markdown("**3. Preferensi Hardware Tambahan** *(Opsional)*")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        pref_ram = st.checkbox("💾 Wajib RAM Besar (≥ 16 GB)")
    with col_p2:
        pref_gpu = st.checkbox("🎮 Wajib GPU Diskrit (Dedicated)")
    with col_p3:
        pref_portabilitas = st.checkbox("🪶 Prioritas Portabilitas Ringan")
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns([3.5, 1])
    with col_b1:
        submitted = st.form_submit_button(
            "⚡ Jalankan Inferensi Prolog",
            use_container_width=True,
            type="primary"
        )
    with col_b2:
        reset = st.form_submit_button("🔄 Reset Pilihan", use_container_width=True)

# ============================================================
# EVALUASI & TAMPILAN REKOMENDASI
# ============================================================
if submitted:
    preferensi = []
    if pref_ram:
        preferensi.append('ram_besar')
    if pref_gpu:
        preferensi.append('gpu_dedicated')
    if pref_portabilitas:
        preferensi.append('portabilitas')
    
    valid, errors = validate_form(kebutuhan_val, kelas_val, preferensi)
    
    if not valid:
        for err in errors:
            st.warning(f"⚠️ {err}")
    else:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.divider()
        
        query_info = format_query_info(kebutuhan_val, kelas_val, preferensi)
        
        # Header Hasil Modern
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 1.25rem;">
            <div>
                <h3 style="margin: 0; font-weight: 800; color: #0F172A;">🎯 Hasil Inferensi Sistem Pakar</h3>
                <span style="font-size: 0.88rem; color: #64748B;">
                    Kriteria: <strong>{query_info['kebutuhan_label']}</strong> &bull; Anggaran: <strong>{query_info['kelas_label']}</strong>
                </span>
            </div>
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 9999px; padding: 6px 14px; font-size: 0.8rem; font-weight: 700; color: #166534;">
                Mesin: SWI-Prolog Resolution Engine
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        query_str = build_query(kebutuhan_val, kelas_val, preferensi)
        
        with st.spinner("🧠 SWI-Prolog sedang melakukan backward chaining evaluation..."):
            try:
                raw_results = engine.query(query_str)
                if not raw_results and 'gpu_dedicated' not in preferensi and 'ram_besar' not in preferensi:
                    fallback_query = f"rekomendasi_lengkap({kebutuhan_val}, {kelas_val}, _, Merk, Model, CPU, RAM, Storage, VGA, Harga)"
                    raw_results = engine.query(fallback_query)
                error_occurred = False
                error_msg = ""
            except RuntimeError as e:
                raw_results = []
                error_occurred = True
                error_msg = str(e)
        
        if error_occurred:
            render_error_message(error_msg)
        elif not raw_results:
            render_no_results(query_info['kebutuhan_label'], query_info['kelas_label'])
        else:
            formatted = [format_laptop_result(r) for r in raw_results]
            unique = deduplicate_results(formatted)
            sorted_results = sort_results(unique, 'harga')
            
            st.success(f"🎉 Berhasil membuktikan **{len(unique)} unit laptop** yang memenuhi seluruh kriteria dan aturan logika!")
            
            # Ambil panduan spesifikasi
            try:
                r_min = engine.query_once(f"spesifikasi_minimum({kebutuhan_val}, SpesMin)")
                r_ideal = engine.query_once(f"spesifikasi_ideal({kebutuhan_val}, SpesIdeal)")
                r_profil = engine.query_once(f"profil_penggunaan({kebutuhan_val}, Profil)")
                r_tips = engine.query_once(f"tips_kebutuhan({kebutuhan_val}, Tips)")
            except Exception:
                r_min = r_ideal = r_profil = r_tips = None
            
            tab_hasil, tab_pedoman = st.tabs(["💻 Daftar Laptop yang Memenuhi Syarat", "📖 Pedoman Spesifikasi & Rule Logika"])
            
            with tab_hasil:
                st.markdown(f"<p style='font-size: 0.85rem; color: #64748B; margin-bottom: 1rem;'>Menampilkan hasil rekomendasi (diurutkan dari harga paling terjangkau):</p>", unsafe_allow_html=True)
                
                for laptop in sorted_results[:12]:
                    # Ambil alasan dari Prolog
                    try:
                        id_query = f"spesifikasi(ID, {laptop['merk']}, '{laptop['model']}', _, {laptop['ram']}, {laptop['storage']}, _, {laptop['harga_juta']})"
                        r_id = engine.query_once(id_query)
                        if r_id and 'ID' in r_id:
                            laptop_id = str(r_id['ID'])
                            alasan_query = f"alasan_rekomendasi({laptop_id}, {kebutuhan_val}, Alasan)"
                            r_alasan = engine.query_once(alasan_query)
                            alasan_text = str(r_alasan['Alasan']) if r_alasan else ""
                        else:
                            alasan_text = ""
                    except Exception:
                        alasan_text = ""
                    
                    render_laptop_card(
                        laptop,
                        alasan=alasan_text,
                        show_prolog_rule=True,
                        kebutuhan=kebutuhan_val
                    )
            
            with tab_pedoman:
                if r_profil:
                    st.markdown("#### 👤 Karakteristik Pengguna")
                    st.info(str(r_profil['Profil']))
                
                c_min, c_idl = st.columns(2)
                with c_min:
                    st.markdown("#### 📋 Spesifikasi Minimum")
                    if r_min:
                        for sp in str(r_min['SpesMin']).split(' | '):
                            st.markdown(f"- {sp}")
                
                with c_idl:
                    st.markdown("#### ⭐ Spesifikasi Ideal (Recommended)")
                    if r_ideal:
                        for sp in str(r_ideal['SpesIdeal']).split(' | '):
                            st.markdown(f"- {sp}")
                
                if r_tips:
                    st.markdown("#### 💡 Tips Pakar Hardware")
                    st.success(str(r_tips['Tips']))
                
                st.markdown("#### 🔍 Kueri Prolog yang Dipanggil")
                st.code(query_str, language="prolog")
            
            # Simpan histori sesi
            hist_entry = add_to_history(kebutuhan_val, kelas_val, preferensi, sorted_results)
            if 'riwayat' not in st.session_state:
                st.session_state['riwayat'] = []
            st.session_state['riwayat'].append(hist_entry)

elif reset:
    st.rerun()
