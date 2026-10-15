"""
ui_helpers.py — Fungsi Bantu Tampilan LaptopExpert (Modern Light & Clear Contrast UI)
Menggunakan native Streamlit components untuk kestabilan render 100%.
"""
import streamlit as st
from services.auth_service import is_authenticated, is_admin, get_current_user, logout


def setup_page(
    title: str,
    icon: str = "💻",
    admin_only: bool = False,
    layout: str = "wide"
) -> None:
    """Setup halaman Streamlit dengan tema cerah, kontras tinggi, dan pengaman sesi."""
    st.set_page_config(
        page_title=f"{title} — LaptopExpert",
        page_icon=icon,
        layout=layout,
        initial_sidebar_state="expanded"
    )
    
    inject_custom_css()
    
    # Cek autentikasi
    if not is_authenticated():
        st.warning("⚠️ Sesi Anda belum aktif. Silakan login terlebih dahulu.")
        st.page_link("app.py", label="Menuju Halaman Login", icon="🔐")
        st.stop()
    
    # Cek akses khusus admin
    if admin_only and not is_admin():
        st.error("🚫 **Akses Terbatas** — Halaman ini dikhususkan untuk Administrator.")
        st.page_link("pages/1_Dashboard.py", label="Kembali ke Dashboard", icon="🏠")
        st.stop()
    
    render_sidebar()


def inject_custom_css() -> None:
    """CSS Modern Cerah, Bersih, dengan Kontras Tulisan Sangat Jelas dan Mudah Dibaca."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sembunyikan navigasi otomatis bawaan Streamlit (yang di atas) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    ul[data-testid="stSidebarNavItems"] {
        display: none !important;
    }

    /* ====================================================
       SIDEBAR: MODERN CRISP WHITE & HIGH CONTRAST
       ==================================================== */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 2px 0 12px rgba(15, 23, 42, 0.03) !important;
    }

    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 0.6rem 0.9rem !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.2s ease !important;
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
        background-color: #E0F2FE !important;
        border-color: #38BDF8 !important;
        transform: translateX(3px) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] span,
    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p {
        color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    section[data-testid="stSidebar"] button {
        background-color: #FEF2F2 !important;
        color: #DC2626 !important;
        border: 1px solid #FECACA !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #FEE2E2 !important;
        border-color: #F87171 !important;
        color: #B91C1C !important;
    }

    /* Badges Status GPU */
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .badge-dedicated {
        background-color: #DCFCE7 !important;
        color: #15803D !important;
        border: 1px solid #86EFAC !important;
    }
    .badge-unified {
        background-color: #E0E7FF !important;
        color: #3730A3 !important;
        border: 1px solid #A5B4FC !important;
    }
    .badge-integrated {
        background-color: #F1F5F9 !important;
        color: #334155 !important;
        border: 1px solid #CBD5E1 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar() -> None:
    """Render sidebar navigasi bersih dengan tulisan terang dan mudah dibaca."""
    user = get_current_user()
    if not user:
        return
    
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: linear-gradient(135deg, #0EA5E9, #3B82F6); padding: 10px; border-radius: 12px; font-size: 1.6rem; color: white;">💻</div>
                <div>
                    <h3 style="margin: 0; font-size: 1.35rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">LaptopExpert</h3>
                    <span style="font-size: 0.78rem; font-weight: 600; color: #0EA5E9; background: #E0F2FE; padding: 2px 8px; border-radius: 6px;">SISTEM PAKAR PROLOG</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        is_adm = user['role'] == 'admin'
        chip_bg = "#FEF3C7" if is_adm else "#EFF6FF"
        chip_border = "#FCD34D" if is_adm else "#BFDBFE"
        chip_title_color = "#92400E" if is_adm else "#1E40AF"
        chip_name_color = "#78350F" if is_adm else "#1E3A8A"
        role_label = "👑 ADMINISTRATOR" if is_adm else "🎓 MAHASISWA"
        
        st.markdown(f"""
        <div style="background: {chip_bg}; border: 1.5px solid {chip_border}; border-radius: 12px; padding: 12px 14px; margin-bottom: 1.5rem;">
            <div style="font-size: 0.72rem; font-weight: 800; color: {chip_title_color}; letter-spacing: 0.04em;">{role_label}</div>
            <div style="font-size: 1.05rem; font-weight: 800; color: {chip_name_color}; margin-top: 2px;">{user['nama']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <p style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: #475569; letter-spacing: 0.06em; margin-bottom: 0.75rem;">
            MENU NAVIGASI
        </p>
        """, unsafe_allow_html=True)
        
        st.page_link("pages/1_Dashboard.py", label="Dashboard Utama", icon="🏠")
        st.page_link("pages/2_Rekomendasi.py", label="Konsultasi Rekomendasi", icon="🔍")
        
        if is_adm:
            st.page_link("pages/3_Basis_Pengetahuan.py", label="Basis Pengetahuan (Admin)", icon="📚")
        
        st.page_link("pages/4_Riwayat.py", label="Riwayat Konsultasi", icon="📜")
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.divider()
        
        if st.button("🚪 Keluar Akun (Logout)", use_container_width=True):
            logout()
            st.switch_page("app.py")


def render_laptop_card(
    laptop: dict,
    alasan: str = "",
    show_prolog_rule: bool = False,
    kebutuhan: str = ""
) -> None:
    """
    Render kartu laptop menggunakan native Streamlit container & metrics
    agar 100% rapi dan tidak ada tag HTML mentah yang bocor.
    """
    gpu_badge_str = laptop.get('gpu_badge', '⚪ Integrated')
    if 'Dedicated' in gpu_badge_str:
        badge_class = 'badge-dedicated'
    elif 'Unified' in gpu_badge_str:
        badge_class = 'badge-unified'
    else:
        badge_class = 'badge-integrated'

    with st.container(border=True):
        # Baris Header: Nama Laptop & Harga
        c_head1, c_head2 = st.columns([2.5, 1])
        with c_head1:
            st.subheader(f"{laptop['merk_icon']} {laptop['display_name']}")
            st.markdown(f"**Prosesor:** `{laptop['cpu']}`")
        with c_head2:
            st.metric("Estimasi Harga", laptop['harga_display'])
        
        st.divider()
        
        # Baris Grid Spesifikasi (RAM, Storage, Tipe Grafis, Chipset VGA)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Kapasitas RAM", f"{laptop['ram']} GB DDR")
        with c2:
            st.metric("Penyimpanan", f"{laptop['storage']} GB SSD")
        with c3:
            st.markdown("**Tipe Grafis**")
            st.markdown(f'<span class="badge-pill {badge_class}">{gpu_badge_str}</span>', unsafe_allow_html=True)
        with c4:
            st.markdown("**Chipset VGA**")
            st.code(laptop['vga'], language=None)
        
        # Alasan Rekomendasi
        if alasan:
            st.success(f"💡 **Justifikasi Sistem Pakar:**\n\n{alasan}")
        
        # Rule Inspector
        if show_prolog_rule and kebutuhan:
            with st.expander("🔍 Tinjau Eksekusi Predikat Prolog (Reasoning Trace)"):
                rule_syntax = (
                    f"% Evaluasi Goal:\n"
                    f"?- rekomendasi_ideal({kebutuhan}, Kelas, {laptop['merk']}, '{laptop['model']}', "
                    f"{laptop['ram']}, '{laptop['vga']}', {laptop['harga_juta']})."
                )
                st.code(rule_syntax, language="prolog")
                st.caption(f"✅ Terpenuhi: Aturan `cocok_untuk(ID, {kebutuhan})` dan `kelas_laptop(ID, Kelas)` bernilai True.")


def render_no_results(kebutuhan_label: str, kelas_label: str) -> None:
    """Tampilan jelas ketika inferensi tidak menemukan kecocokan."""
    st.warning("⚠️ **Aturan Belum Terpenuhi (No Matching Rules)**")
    st.info(
        f"Tidak ditemukan laptop dalam basis pengetahuan yang memenuhi beban komputasi **{kebutuhan_label}** "
        f"pada batas anggaran **{kelas_label}**."
    )
    with st.container(border=True):
        st.markdown("**💡 Rekomendasi Kompromi dari Pakar Hardware:**")
        st.markdown("""
        - Tingkatkan batas anggaran satu kelas ke atas untuk mendapatkan GPU diskrit atau RAM $\ge 16$ GB.
        - Atau turunkan intensitas komputasi (contoh: dari *Editing Berat 4K* ke *Editing Ringan*).
        - Hapus centang preferensi tambahan jika kriteria terlalu spesifik.
        """)


def render_error_message(error: str) -> None:
    """Tampilkan notifikasi error human-friendly."""
    st.error("❌ Terjadi kendala saat berkomunikasi dengan mesin logika SWI-Prolog.")
    with st.expander("Detail Pesan Error"):
        st.code(error, language="text")
