"""
1_Dashboard.py — Dashboard Utama LaptopExpert (Modern UI)
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ui_helpers import setup_page
from services.prolog_engine import get_prolog_engine
from services.auth_service import get_current_user, is_admin

setup_page("Dashboard", icon="🏠")

user = get_current_user()
engine = get_prolog_engine()

# ============================================================
# HERO HEADER
# ============================================================
st.markdown(f"""
<div style="background: linear-gradient(135deg, #0EA5E9 0%, #3B82F6 50%, #6366F1 100%); border-radius: 20px; padding: 2.25rem 2rem; color: white; margin-bottom: 2rem; box-shadow: 0 12px 30px -10px rgba(14, 165, 233, 0.35);">
    <span style="background: rgba(255, 255, 255, 0.2); padding: 4px 12px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Sistem Pakar Berbasis Logika Predikat</span>
    <h1 style="color: white; margin: 0.6rem 0 0.4rem 0; font-size: 2.2rem; font-weight: 800;">Selamat Datang, {user['nama']}! 👋</h1>
    <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.05rem; max-width: 700px; margin: 0; line-height: 1.5;">
        Temukan rekomendasi spesifikasi laptop paling tepat dan objektif untuk kebutuhan kuliah Anda melalui penalaran logika <strong>SWI-Prolog</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# Status Mesin Inferensi
if not engine.is_loaded:
    st.error(f"❌ **Knowledge Base Prolog Gagal Terhubung**\n\n{engine.error_message}")
    st.stop()

# ============================================================
# STATISTIK PROLOG (REAL-TIME METRICS)
# ============================================================
st.markdown("<h3 style='font-weight: 700; color: #0F172A; margin-bottom: 0.2rem;'>📊 Statistik Knowledge Base</h3>", unsafe_allow_html=True)
st.caption("Data berikut dihitung secara dinamis melalui kueri evaluasi predikat Prolog.")

stats = engine.get_stats()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
        <span style="font-size: 1.75rem;">💾</span>
        <div style="font-size: 2rem; font-weight: 800; color: #0EA5E9; margin: 0.25rem 0;">{stats.get('laptop', 0)}</div>
        <div style="font-weight: 600; color: #334155;">Total Laptop Database</div>
        <div style="font-size: 0.75rem; color: #64748B;">Fakta <code>spesifikasi/8</code> aktif</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
        <span style="font-size: 1.75rem;">📋</span>
        <div style="font-size: 2rem; font-weight: 800; color: #6366F1; margin: 0.25rem 0;">{stats.get('kategori', 8)}</div>
        <div style="font-weight: 600; color: #334155;">Profil Penggunaan</div>
        <div style="font-size: 0.75rem; color: #64748B;">Kategori beban kerja software</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
        <span style="font-size: 1.75rem;">⚙️</span>
        <div style="font-size: 2rem; font-weight: 800; color: #10B981; margin: 0.25rem 0;">12+</div>
        <div style="font-weight: 600; color: #334155;">Aturan Inferensi Aktif</div>
        <div style="font-size: 0.75rem; color: #64748B;">Rules <code>cocok_untuk</code> & <code>kelas</code></div>
    </div>
    """, unsafe_allow_html=True)

# Distribusi Kelas Harga
st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
st.markdown("<p style='font-weight: 600; color: #475569; font-size: 0.9rem; margin-bottom: 0.5rem;'>Distribusi Unit Berdasarkan Kelas Anggaran:</p>", unsafe_allow_html=True)

col_e, col_m, col_h, col_f = st.columns(4)
with col_e:
    st.metric("🟢 Entry (< 10 Juta)", f"{stats.get('entry', 0)} Unit")
with col_m:
    st.metric("🔵 Midrange (10 - 19 Jt)", f"{stats.get('midrange', 0)} Unit")
with col_h:
    st.metric("🟣 High-End (20 - 34 Jt)", f"{stats.get('high_end', 0)} Unit")
with col_f:
    st.metric("🟡 Flagship (≥ 35 Jt)", f"{stats.get('flagship', 0)} Unit")

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
st.divider()

# ============================================================
# TENTANG SISTEM & CTA
# ============================================================
col_desc, col_cta = st.columns([1.8, 1.2])

with col_desc:
    st.markdown("### 💡 Bagaimana LaptopExpert Bekerja?")
    st.markdown("""
    Aplikasi ini mengimplementasikan konsep sistem pakar formal dengan pemisahan tegas antara basis pengetahuan dan mesin penarik kesimpulan:
    
    1. **Knowledge Representation (Fakta & Aturan):** Spesifikasi 70 laptop direpresentasikan sebagai fakta logika orde pertama `spesifikasi/8`, dan kriteria hardware software dimodelkan via aturan `cocok_untuk/2`.
    2. **Rule-Based Inference:** Ketika Anda menekan tombol konsultasi, SWI-Prolog mengevaluasi *goal* menggunakan mekanisme pembuktian resolusi *backward chaining*.
    3. **Explainable Output:** Sistem menampilkan *reasoning trace* yang merinci alasan spesifikasi hardware dan aturan yang terpenuhi.
    """)

with col_cta:
    st.markdown("""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.5rem; text-align: center;">
        <span style="font-size: 2.2rem;">🚀</span>
        <h4 style="margin: 0.5rem 0 0.25rem 0; font-weight: 700; color: #0F172A;">Mulai Konsultasi</h4>
        <p style="font-size: 0.85rem; color: #64748B; margin-bottom: 1.25rem;">Pilih kebutuhan beban kuliah Anda dan dapatkan rekomendasi terbaik.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    if st.button("🔍 Konsultasi Rekomendasi Sekarang", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Rekomendasi.py")
    
    if is_admin():
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
        if st.button("📚 Buka Panel Basis Pengetahuan", use_container_width=True):
            st.switch_page("pages/3_Basis_Pengetahuan.py")
