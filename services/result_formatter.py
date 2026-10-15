"""
result_formatter.py — Pemformatan Hasil Rekomendasi
Mengubah hasil query Prolog menjadi struktur data Python yang siap ditampilkan.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

KEBUTUHAN_LABELS = {
    "office": "Kuliah Umum & Produktivitas",
    "koding": "Pemrograman & Pengembangan Perangkat Lunak",
    "editing_ringan": "Desain Grafis Ringan (Figma, Canva)",
    "editing_berat": "Desain Grafis & Multimedia Berat",
    "gaming": "Gaming",
    "streaming": "Gaming + Streaming",
    "data_science": "Data Science & Machine Learning",
    "virtualisasi": "Jaringan Komputer & Virtualisasi",
}

KELAS_LABELS = {
    "entry": "Di bawah Rp10.000.000",
    "midrange": "Rp10.000.000 – Rp19.000.000",
    "high_end": "Rp20.000.000 – Rp34.000.000",
    "flagship": "Di atas Rp35.000.000",
}

MERK_ICONS = {
    "apple": "🍎",
    "asus": "🔷",
    "lenovo": "🔴",
    "acer": "💚",
    "hp": "🔵",
    "msi": "🟡",
}


def parse_prolog_atom(value: Any) -> str:
    """Konversi atom PySwip ke string Python."""
    if hasattr(value, 'decode'):
        return value.decode('utf-8')
    return str(value)


def format_harga(harga_juta: int) -> str:
    """Format harga dalam jutaan menjadi string rupiah."""
    harga_rupiah = harga_juta * 1_000_000
    return f"Rp{harga_rupiah:,.0f}".replace(',', '.')


def format_laptop_result(raw_result: dict) -> dict:
    """Format satu hasil query Prolog menjadi dict."""
    merk = parse_prolog_atom(raw_result.get('Merk', ''))
    model = parse_prolog_atom(raw_result.get('Model', ''))
    cpu = parse_prolog_atom(raw_result.get('CPU', '-'))
    vga = parse_prolog_atom(raw_result.get('VGA', '-'))
    ram = raw_result.get('RAM', 0)
    storage = raw_result.get('Storage', 0)
    harga = raw_result.get('Harga', 0)
    
    vga_str = str(vga).upper()
    if 'RTX' in vga_str or 'GTX' in vga_str or 'RX' in vga_str:
        gpu_type = 'Dedicated GPU'
        gpu_badge = '🟢 Dedicated'
    elif 'APPLE' in vga_str:
        gpu_type = 'Apple GPU'
        gpu_badge = '🔵 Unified'
    elif 'ARC' in vga_str:
        gpu_type = 'Intel Arc'
        gpu_badge = '🟡 Dedicated'
    else:
        gpu_type = 'Integrated'
        gpu_badge = '⚪ Integrated'
    
    return {
        "merk": merk,
        "merk_icon": MERK_ICONS.get(merk.lower(), "💻"),
        "model": model,
        "cpu": cpu,
        "ram": ram,
        "storage": storage,
        "vga": vga,
        "gpu_type": gpu_type,
        "gpu_badge": gpu_badge,
        "harga_juta": harga,
        "harga_display": f"±{format_harga(harga)}",
        "display_name": f"{merk.capitalize()} {model}",
    }


def deduplicate_results(results: List[dict]) -> List[dict]:
    """Hapus duplikasi laptop."""
    seen = set()
    unique = []
    for r in results:
        key = (r['merk'], r['model'], r['harga_juta'])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def sort_results(results: List[dict], sort_by: str = 'harga') -> List[dict]:
    """Urutkan hasil rekomendasi."""
    if sort_by == 'harga':
        return sorted(results, key=lambda x: x['harga_juta'])
    elif sort_by == 'ram':
        return sorted(results, key=lambda x: x['ram'], reverse=True)
    return results


def format_query_info(kebutuhan: str, kelas: str, preferensi: List[str]) -> dict:
    """Format informasi query untuk ditampilkan di UI."""
    return {
        "kebutuhan": kebutuhan,
        "kebutuhan_label": KEBUTUHAN_LABELS.get(kebutuhan, kebutuhan),
        "kelas": kelas,
        "kelas_label": KELAS_LABELS.get(kelas, kelas),
        "preferensi": preferensi,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }


def add_to_history(
    kebutuhan: str,
    kelas: str,
    preferensi: List[str],
    results: List[dict],
    alasan: str = ""
) -> dict:
    """Buat entri riwayat rekomendasi."""
    return {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "kebutuhan_label": KEBUTUHAN_LABELS.get(kebutuhan, kebutuhan),
        "kelas_label": KELAS_LABELS.get(kelas, kelas),
        "preferensi": preferensi,
        "jumlah_hasil": len(results),
        "hasil_teratas": results[0]['display_name'] if results else "Tidak ada hasil",
    }

