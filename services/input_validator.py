"""
input_validator.py — Validasi Input Form LaptopExpert
Memastikan input pengguna valid sebelum dikirim ke Prolog.
"""
from typing import Tuple, List, Optional

# Atom Prolog yang valid untuk kategori kebutuhan
VALID_KEBUTUHAN = {
    "office", "koding", "editing_ringan",
    "editing_berat", "gaming", "streaming",
    "data_science", "virtualisasi"
}

# Atom Prolog yang valid untuk kelas anggaran
VALID_KELAS = {
    "entry", "midrange", "high_end", "flagship"
}

# Preferensi yang valid
VALID_PREFERENSI = {
    "ram_besar", "gpu_dedicated", "portabilitas"
}


def validate_form(
    kebutuhan: Optional[str],
    kelas: Optional[str],
    preferensi: Optional[List[str]] = None
) -> Tuple[bool, List[str]]:
    """
    Validasi input form rekomendasi.
    
    Args:
        kebutuhan: Atom kebutuhan yang dipilih
        kelas: Atom kelas anggaran yang dipilih
        preferensi: List preferensi tambahan
        
    Returns:
        Tuple (valid, list_pesan_error)
    """
    errors = []
    
    if not kebutuhan:
        errors.append("Kebutuhan utama harus dipilih.")
    elif kebutuhan not in VALID_KEBUTUHAN:
        errors.append(f"Kebutuhan '{kebutuhan}' tidak valid.")
    
    if not kelas:
        errors.append("Kategori anggaran harus dipilih.")
    elif kelas not in VALID_KELAS:
        errors.append(f"Kelas anggaran '{kelas}' tidak valid.")
    
    if preferensi:
        invalid_pref = [p for p in preferensi if p not in VALID_PREFERENSI]
        if invalid_pref:
            errors.append(f"Preferensi tidak valid: {', '.join(invalid_pref)}")
    
    return len(errors) == 0, errors


def build_query(kebutuhan: str, kelas: str, preferensi: List[str]) -> str:
    """
    Bangun string query Prolog berdasarkan input yang sudah divalidasi.
    """
    if 'ram_besar' in preferensi and 'gpu_dedicated' in preferensi:
        query = (
            f"rekomendasi_lengkap({kebutuhan}, {kelas}, "
            f"ID, Merk, Model, CPU, RAM, Storage, VGA, Harga), "
            f"RAM >= 16, "
            f"("
            f"sub_atom(VGA, _, _, _, 'RTX') ; "
            f"sub_atom(VGA, _, _, _, 'GTX') ; "
            f"sub_atom(VGA, _, _, _, 'RX') ; "
            f"sub_atom(VGA, _, _, _, 'Apple')"
            f")"
        )
    elif 'ram_besar' in preferensi:
        query = (
            f"rekomendasi_dengan_ram({kebutuhan}, {kelas}, "
            f"Merk, Model, RAM, Storage, VGA, Harga)"
        )
    elif 'gpu_dedicated' in preferensi:
        query = (
            f"rekomendasi_dengan_gpu({kebutuhan}, {kelas}, "
            f"Merk, Model, RAM, VGA, Harga, _)"
        )
    else:
        query = (
            f"rekomendasi_lengkap({kebutuhan}, {kelas}, "
            f"_, Merk, Model, CPU, RAM, Storage, VGA, Harga)"
        )
    
    return query


def build_alasan_query(id_laptop: str, kebutuhan: str) -> str:
    """Bangun query untuk mengambil alasan rekomendasi."""
    return f"alasan_rekomendasi({id_laptop}, {kebutuhan}, Alasan)"


def sanitize_atom(value: str) -> str:
    """Sanitasi string agar aman sebagai atom Prolog."""
    return ''.join(c for c in value if c.isalnum() or c == '_')

