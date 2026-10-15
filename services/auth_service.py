"""
auth_service.py — Layanan Autentikasi LaptopExpert
Menangani login, logout, validasi peran, dan hashing password.
"""
import hashlib
import streamlit as st
from typing import Optional, Tuple


def hash_password(password: str) -> str:
    """Hash password menggunakan SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def get_credentials() -> dict:
    """
    Ambil kredensial dari st.secrets.
    Format secrets.toml:
        [credentials]
        admin_username = "admin"
        admin_password_hash = "<sha256>"
        user_username = "mahasiswa"
        user_password_hash = "<sha256>"
    """
    try:
        creds = st.secrets["credentials"]
        return {
            creds["admin_username"]: {
                "password_hash": creds["admin_password_hash"],
                "role": "admin",
                "nama": creds.get("admin_nama", "Administrator")
            },
            creds["user_username"]: {
                "password_hash": creds["user_password_hash"],
                "role": "user",
                "nama": creds.get("user_nama", "Mahasiswa")
            }
        }
    except Exception:
        # Fallback untuk development (jangan digunakan di produksi)
        return {
            "admin": {
                "password_hash": hash_password("admin123"),
                "role": "admin",
                "nama": "Administrator"
            },
            "mahasiswa": {
                "password_hash": hash_password("user123"),
                "role": "user",
                "nama": "Mahasiswa"
            }
        }


def login(username: str, password: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Verifikasi login pengguna.
    
    Returns:
        Tuple (berhasil, peran, nama_pengguna)
    """
    if not username or not password:
        return False, None, None
    
    credentials = get_credentials()
    username = username.strip().lower()
    
    if username not in credentials:
        return False, None, None
    
    user_data = credentials[username]
    input_hash = hash_password(password)
    
    if input_hash == user_data["password_hash"]:
        return True, user_data["role"], user_data["nama"]
    
    return False, None, None


def is_authenticated() -> bool:
    """Cek apakah pengguna sudah login."""
    return st.session_state.get("authenticated", False)


def is_admin() -> bool:
    """Cek apakah pengguna yang login adalah admin."""
    return (
        is_authenticated() and
        st.session_state.get("role") == "admin"
    )


def get_current_user() -> Optional[dict]:
    """Ambil data pengguna yang sedang login."""
    if not is_authenticated():
        return None
    return {
        "username": st.session_state.get("username"),
        "role": st.session_state.get("role"),
        "nama": st.session_state.get("nama")
    }


def set_session(username: str, role: str, nama: str) -> None:
    """Set sesi pengguna setelah login berhasil."""
    st.session_state["authenticated"] = True
    st.session_state["username"] = username
    st.session_state["role"] = role
    st.session_state["nama"] = nama
    if "riwayat" not in st.session_state:
        st.session_state["riwayat"] = []


def logout() -> None:
    """Hapus sesi pengguna."""
    keys_to_remove = ["authenticated", "username", "role", "nama", "riwayat"]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]


def require_auth(admin_only: bool = False) -> bool:
    """
    Decorator/guard untuk halaman yang memerlukan autentikasi.
    Panggil di awal setiap halaman yang dilindungi.
    
    Returns:
        True jika pengguna punya akses, False jika tidak.
    """
    if not is_authenticated():
        st.warning("⚠️ Silakan login terlebih dahulu untuk mengakses halaman ini.")
        st.page_link("app.py", label="Kembali ke Halaman Login", icon="🔐")
        st.stop()
        return False
    
    if admin_only and not is_admin():
        st.error("🚫 Akses Ditolak — Halaman ini hanya dapat diakses oleh Admin.")
        st.page_link("pages/1_🏠_Dashboard.py", label="Kembali ke Dashboard", icon="🏠")
        st.stop()
        return False
    
    return True
