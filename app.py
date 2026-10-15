"""
app.py — Entry Point LaptopExpert (Modern Glassmorphism Login)
"""
import streamlit as st
from services.auth_service import login, set_session, is_authenticated

st.set_page_config(
    page_title="LaptopExpert — Masuk",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling Login Modern
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="collapsedControl"] {display: none;}

/* Background modern subtle gradient */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.05) 0%, rgba(248, 250, 252, 1) 90%);
}

.login-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 24px;
    padding: 2.5rem 2rem;
    box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.08);
    text-align: center;
}

.brand-icon {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%);
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin: 0 auto 1.25rem auto;
    box-shadow: 0 10px 20px -5px rgba(14, 165, 233, 0.4);
}
</style>
""", unsafe_allow_html=True)

# Jika sudah login langsung alihkan
if is_authenticated():
    st.switch_page("pages/1_Dashboard.py")

col1, col2, col3 = st.columns([1, 2.5, 1])

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div class="brand-icon">💻</div>
        <h2 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">LaptopExpert</h2>
        <p style="color: #64748B; font-size: 0.95rem; margin-top: 4px;">Sistem Pakar Rekomendasi Laptop Mahasiswa</p>
        <span style="display: inline-block; background: #E0F2FE; color: #0284C7; font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 9999px;">AI WITH PROLOG</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        st.markdown("<p style='font-weight: 600; color: #334155; margin-bottom: 0.5rem;'>Autentikasi Pengguna</p>", unsafe_allow_html=True)
        
        username = st.text_input(
            "Username",
            placeholder="Masukkan username (cth: mahasiswa / admin)",
            key="login_username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Masukkan password",
            key="login_password"
        )
        
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🚀 Masuk ke Sistem",
            use_container_width=True,
            type="primary"
        )
    
    if submitted:
        if not username or not password:
            st.error("⚠️ Username dan password wajib diisi.")
        else:
            with st.spinner("Memvalidasi kredensial keamanan..."):
                berhasil, role, nama = login(username, password)
            
            if berhasil:
                set_session(username.strip().lower(), role, nama)
                st.success(f"✅ Berhasil masuk! Selamat datang, {nama}.")
                st.rerun()
            else:
                st.error("❌ Kredensial tidak valid. Silakan periksa kembali kombinasi username dan password.")
    
    # Petunjuk Kredensial Demo
    st.markdown("""
    <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 12px; padding: 12px; margin-top: 1.5rem; font-size: 0.8rem; color: #64748B;">
        <strong>🔑 Akun Pengujian Demo:</strong><br>
        • <strong>Mahasiswa:</strong> <code>mahasiswa</code> / <code>user123</code><br>
        • <strong>Administrator:</strong> <code>admin</code> / <code>admin123</code>
    </div>
    """, unsafe_allow_html=True)
