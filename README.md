# 💻 LaptopExpert — Sistem Pakar Rekomendasi Laptop

> **Judul Akademik:** Pengembangan Sistem Pakar Rekomendasi Laptop untuk Mahasiswa Menggunakan Prolog Berbasis Rule-Based Reasoning

LaptopExpert adalah aplikasi web sistem pakar yang membantu mahasiswa memilih laptop sesuai kebutuhan dan anggaran menggunakan **rule-based reasoning** dengan **SWI-Prolog**.

## 🛠️ Teknologi

| Komponen | Teknologi | Versi |
|---|---|---|
| Antarmuka Web | Streamlit | ≥ 1.28.0 |
| Backend | Python | 3.10 / 3.11 |
| Mesin Inferensi | SWI-Prolog | 9.x |
| Jembatan Prolog | PySwip | 0.2.10 |

## 📋 Prasyarat

### 1. Instal SWI-Prolog

**Windows:**
- Unduh installer dari [swi-prolog.org/download/stable](https://www.swi-prolog.org/download/stable)
- Pilih versi **64-bit Windows**
- Centang opsi **"Add SWI-Prolog to PATH"** saat instalasi
- Verifikasi: buka PowerShell, ketik `swipl --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install swi-prolog
```

### 2. Instal Python (3.10 atau 3.11)
Unduh dari [python.org](https://www.python.org/downloads/)

## 🚀 Setup dan Menjalankan Aplikasi

### Langkah 1: Clone/Download Proyek
```bash
# Jika menggunakan Git
git clone <url-repositori>
cd laptop-expert

# Atau extract ZIP dan buka folder proyek
```

### Langkah 2: Buat Virtual Environment
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Langkah 3: Instal Dependensi
```bash
pip install -r requirements.txt
```

### Langkah 4: Setup Kredensial
```bash
# Windows
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

# Linux/macOS
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

File `secrets.toml` sudah berisi kredensial default untuk development:

| Role | Username | Password Default |
|---|---|---|
| Admin | `admin` | `admin123` |
| Pengguna | `mahasiswa` | `user123` |

### Langkah 5: Jalankan Aplikasi
```bash
streamlit run app.py
```

Buka browser di `http://localhost:8501`

## 🧪 Pengujian

### Uji Aturan Prolog (Mandiri)
```bash
cd prolog
swipl -g "run_tests" -t halt test_rules.pl
```

### Uji Integrasi Python-Prolog
```bash
pip install pytest
pytest tests/test_integration.py -v
```

## 📁 Struktur Proyek

```
laptop-expert/
├── app.py                    # Entry point (halaman login)
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml           # Konfigurasi tema
│   └── secrets.toml.example  # Template kredensial
├── prolog/
│   ├── knowledge_base.pl     # 70+ fakta spesifikasi laptop
│   ├── classification_rules.pl  # kelas_laptop/2, cocok_untuk/2
│   ├── recommendation_rules.pl  # rekomendasi_ideal/7
│   ├── explanation_rules.pl     # alasan_rekomendasi/3
│   └── test_rules.pl            # Pengujian Prolog mandiri
├── services/
│   ├── auth_service.py       # Autentikasi
│   ├── prolog_engine.py      # Integrasi PySwip
│   ├── input_validator.py    # Validasi input
│   └── result_formatter.py   # Format hasil
├── pages/
│   ├── 1_🏠_Dashboard.py
│   ├── 2_🔍_Rekomendasi.py
│   ├── 3_📚_Basis_Pengetahuan.py
│   └── 4_📜_Riwayat.py
├── utils/
│   └── ui_helpers.py
└── tests/
    └── test_integration.py
```

## 🔑 Akun Demo

| Peran | Username | Password | Akses |
|---|---|---|---|
| Admin | `admin` | `admin123` | Semua halaman + Basis Pengetahuan |
| Mahasiswa | `mahasiswa` | `user123` | Dashboard + Rekomendasi + Riwayat |

## ⚠️ Troubleshooting

**Error: `libswipl` tidak ditemukan**
→ SWI-Prolog tidak terinstal atau tidak ada di PATH. Reinstall SWI-Prolog dan pastikan PATH sudah diatur.

**Error: `PySwip` tidak dapat import**
→ Jalankan `pip install pyswip==0.2.10` di dalam virtual environment yang aktif.

**Error: File Prolog tidak ditemukan**
→ Pastikan folder `prolog/` ada di direktori proyek dan berisi semua file `.pl`.

**PySwip berhasil import tapi query gagal di Windows**
→ Pastikan versi Python dan SWI-Prolog keduanya **64-bit**. Versi 32-bit tidak kompatibel satu sama lain.
