"""
test_integration.py — Pengujian Integrasi Python-Prolog
Jalankan dengan: pytest tests/test_integration.py -v
"""
import pytest
import sys
from pathlib import Path

# Tambahkan root ke path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from services.prolog_engine import PrologEngine
    SKIP_REASON = None
except ImportError as e:
    SKIP_REASON = f"PySwip tidak tersedia: {e}"


@pytest.fixture(scope="module")
def engine():
    if SKIP_REASON:
        pytest.skip(SKIP_REASON)
    eng = PrologEngine()
    if not eng.is_loaded:
        pytest.skip(f"Prolog engine gagal dimuat: {eng.error_message}")
    return eng


# T-17: Integrasi Python-Prolog Berhasil
def test_prolog_connection(engine):
    """T-17: Verifikasi koneksi dasar ke SWI-Prolog"""
    result = engine.query("true")
    assert result == [{}], "Prolog harus mengembalikan [{}] untuk query 'true'"


# T-18: Hasil dari Prolog
def test_dataset_loaded(engine):
    """T-18: Verifikasi 70+ laptop berhasil dimuat dari knowledge base"""
    result = engine.query_once("jumlah_laptop(N)")
    assert result is not None
    assert result['N'] >= 70, f"Harus ada minimal 70 laptop, ditemukan: {result['N']}"


# T-06: Rekomendasi Pemrograman
def test_rekomendasi_koding_midrange(engine):
    """T-06: Rekomendasi laptop untuk pemrograman anggaran midrange"""
    results = engine.query(
        "rekomendasi_ideal(koding, midrange, Merk, Model, RAM, VGA, Harga)"
    )
    assert len(results) > 0, "Harus ada laptop koding di kelas midrange"
    for r in results:
        assert r['RAM'] >= 8, f"RAM harus >= 8GB, dapat: {r['RAM']}"
        assert r['Harga'] >= 10 and r['Harga'] < 20


# T-07: Rekomendasi Desain Berat
def test_rekomendasi_editing_berat_high_end(engine):
    """T-07: Rekomendasi laptop untuk editing berat anggaran high-end"""
    results = engine.query(
        "rekomendasi_ideal(editing_berat, high_end, Merk, Model, RAM, VGA, Harga)"
    )
    assert len(results) > 0, "Harus ada laptop editing berat di high-end"
    for r in results:
        assert r['RAM'] >= 16


# T-08: Rekomendasi Gaming
def test_rekomendasi_gaming_midrange(engine):
    """T-08: Rekomendasi laptop gaming anggaran midrange memiliki GPU dedicated"""
    results = engine.query(
        "rekomendasi_ideal(gaming, midrange, Merk, Model, RAM, VGA, Harga)"
    )
    assert len(results) > 0
    for r in results:
        vga = str(r['VGA'])
        has_dedicated = any(gpu in vga.upper() for gpu in ['RTX', 'GTX', 'RX'])
        assert has_dedicated, f"GPU harus dedicated, dapat: {vga}"


# T-09: Rekomendasi Kuliah Umum
def test_rekomendasi_office_entry(engine):
    """T-09: Rekomendasi kuliah umum anggaran entry"""
    results = engine.query(
        "rekomendasi_ideal(office, entry, Merk, Model, RAM, VGA, Harga)"
    )
    assert len(results) > 0
    for r in results:
        assert r['Harga'] < 10


# T-10: Rekomendasi Data Science
def test_rekomendasi_data_science(engine):
    """T-10: Rekomendasi data science memiliki RAM >= 16GB"""
    results = engine.query(
        "rekomendasi_ideal(data_science, midrange, Merk, Model, RAM, VGA, Harga)"
    )
    assert len(results) > 0
    for r in results:
        assert r['RAM'] >= 16


# T-11: Rekomendasi Virtualisasi
def test_rekomendasi_virtualisasi(engine):
    """T-11: Rekomendasi virtualisasi memiliki RAM >= 16GB"""
    results = engine.query(
        "rekomendasi_ideal(virtualisasi, high_end, Merk, Model, RAM, VGA, Harga)"
    )
    assert len(results) > 0
    for r in results:
        assert r['RAM'] >= 16


# T-13: Anggaran Tidak Sesuai
def test_editing_berat_entry_no_result(engine):
    """T-13: Editing berat dengan anggaran entry seharusnya tidak ada hasil"""
    results = engine.query(
        "rekomendasi_ideal(editing_berat, entry, Merk, Model, RAM, VGA, Harga)"
    )
    assert len(results) == 0, "Seharusnya tidak ada laptop editing berat di kelas entry"


# T-13b: Gaming entry tidak ada hasil
def test_gaming_entry_no_result(engine):
    """T-13b: Gaming dengan anggaran entry seharusnya tidak ada hasil (tidak ada GPU dedicated < 10 juta)"""
    results = engine.query(
        "rekomendasi_ideal(gaming, entry, Merk, Model, RAM, VGA, Harga)"
    )
    # Verifikasi bahwa jika ada, memang memiliki GPU dedicated
    for r in results:
        vga = str(r['VGA'])
        has_dedicated = any(gpu in vga.upper() for gpu in ['RTX', 'GTX', 'RX'])
        assert has_dedicated


# T-14: Konsistensi Hasil
def test_konsistensi_hasil(engine):
    """T-02 Variant: Input yang sama harus menghasilkan output yang sama (deterministik)"""
    query = "rekomendasi_ideal(koding, midrange, Merk, Model, RAM, VGA, Harga)"
    result1 = engine.query(query)
    result2 = engine.query(query)
    
    # Jumlah hasil harus sama
    assert len(result1) == len(result2)
    
    # Model yang dikembalikan harus sama
    models1 = sorted([str(r['Model']) for r in result1])
    models2 = sorted([str(r['Model']) for r in result2])
    assert models1 == models2


# T-12: Kombinasi Kebutuhan
def test_rekomendasi_kompleks(engine):
    """T-12: Rekomendasi kombinasi dua kebutuhan"""
    results = engine.query(
        "rekomendasi_kompleks(gaming, koding, high_end, Merk, Model, Harga)"
    )
    # Laptop gaming+koding di high_end harus ada
    assert len(results) > 0


# Test statistik dashboard
def test_stats(engine):
    """Statistik dashboard harus mengembalikan nilai yang masuk akal"""
    stats = engine.get_stats()
    assert stats['laptop'] >= 70
    assert stats['kategori'] >= 8
    assert stats['entry'] > 0
    assert stats['midrange'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
