"""
Basis Pengetahuan — LaptopExpert (Admin Only)
Halaman untuk meninjau fakta dan aturan Prolog.
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ui_helpers import setup_page
from services.prolog_engine import get_prolog_engine
from services.result_formatter import parse_prolog_atom

setup_page("Basis Pengetahuan", icon="📚", admin_only=True)

engine = get_prolog_engine()

if not engine.is_loaded:
    st.error(f"❌ Knowledge Base tidak tersedia: {engine.error_message}")
    st.stop()

# ============================================================
# HEADER
# ============================================================

st.markdown("## 📚 Basis Pengetahuan")
st.markdown("Halaman ini menampilkan seluruh fakta dan aturan yang aktif dalam sistem. *(Hanya dapat dilihat oleh Admin)*")
st.divider()

# ============================================================
# TABS
# ============================================================

tab_laptop, tab_aturan, tab_prolog = st.tabs([
    "💾 Data Laptop",
    "⚙️ Aturan Kecocokan",
    "🔍 Query Langsung"
])

# ----- TAB 1: DATA LAPTOP -----
with tab_laptop:
    st.markdown("### 💾 Daftar Laptop dalam Knowledge Base")
    st.caption("Data diambil langsung dari fakta `spesifikasi/8` di `knowledge_base.pl`")
    
    # Filter merek
    merks = ['Semua', 'apple', 'asus', 'lenovo', 'acer', 'hp', 'msi']
    filter_merk = st.selectbox("Filter Merek:", merks)
    
    try:
        if filter_merk == 'Semua':
            query = "spesifikasi(ID, Merk, Model, CPU, RAM, Storage, VGA, Harga)"
        else:
            query = f"spesifikasi(ID, {filter_merk}, Model, CPU, RAM, Storage, VGA, Harga)"
        
        results = engine.query(query)
        
        if results:
            data = []
            for r in results:
                data.append({
                    "ID": str(r['ID']),
                    "Merek": parse_prolog_atom(r.get('Merk', '')).capitalize() if filter_merk == 'Semua' else filter_merk.capitalize(),
                    "Model": parse_prolog_atom(r['Model']),
                    "CPU": parse_prolog_atom(r['CPU']),
                    "RAM (GB)": r['RAM'],
                    "Storage (GB)": r['Storage'],
                    "GPU/VGA": parse_prolog_atom(r['VGA']),
                    "Harga (Juta Rp)": r['Harga'],
                })
            
            df = pd.DataFrame(data)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Harga (Juta Rp)": st.column_config.NumberColumn(
                        format="Rp %d jt"
                    ),
                    "RAM (GB)": st.column_config.NumberColumn(format="%d GB"),
                    "Storage (GB)": st.column_config.NumberColumn(format="%d GB"),
                }
            )
            st.caption(f"Total: {len(data)} laptop")
        else:
            st.warning("Tidak ada data ditemukan.")
    
    except Exception as e:
        st.error(f"Error mengambil data: {e}")

# ----- TAB 2: ATURAN KECOCOKAN -----
with tab_aturan:
    st.markdown("### ⚙️ Aturan yang Aktif dalam Sistem")
    
    kategori_info = [
        {
            "Kategori": "office",
            "Label": "Kuliah Umum & Produktivitas",
            "Predikat": "cocok_untuk(ID, office)",
            "Kondisi": "Semua laptop memenuhi syarat (tidak ada filter tambahan)",
            "Basis Aturan": "spesifikasi(ID, _, _, _, _, _, _, _)"
        },
        {
            "Kategori": "koding",
            "Label": "Pemrograman",
            "Predikat": "cocok_untuk(ID, koding)",
            "Kondisi": "RAM >= 8GB",
            "Basis Aturan": "spesifikasi(ID, _, _, _, RAM, _, _, _), RAM >= 8"
        },
        {
            "Kategori": "editing_ringan",
            "Label": "Desain Ringan",
            "Predikat": "cocok_untuk(ID, editing_ringan)",
            "Kondisi": "RAM >= 8GB dan Harga >= 7 juta",
            "Basis Aturan": "RAM >= 8, Harga >= 7"
        },
        {
            "Kategori": "editing_berat",
            "Label": "Desain & Multimedia Berat",
            "Predikat": "cocok_untuk(ID, editing_berat)",
            "Kondisi": "RAM >= 16GB dan GPU dedicated (RTX/RX/Apple/Arc)",
            "Basis Aturan": "RAM >= 16, GPU berisi 'RTX' atau 'Apple' atau 'RX 6' atau 'Arc'"
        },
        {
            "Kategori": "gaming",
            "Label": "Gaming",
            "Predikat": "cocok_untuk(ID, gaming)",
            "Kondisi": "GPU dedicated (RTX, GTX, atau AMD RX)",
            "Basis Aturan": "GPU berisi 'RTX' atau 'GTX' atau 'RX'"
        },
        {
            "Kategori": "streaming",
            "Label": "Gaming + Streaming",
            "Predikat": "cocok_untuk(ID, streaming)",
            "Kondisi": "RAM >= 16GB dan GPU RTX atau RX",
            "Basis Aturan": "RAM >= 16, GPU berisi 'RTX' atau 'RX'"
        },
        {
            "Kategori": "data_science",
            "Label": "Data Science & ML",
            "Predikat": "cocok_untuk(ID, data_science)",
            "Kondisi": "RAM >= 16GB dan CPU bukan Celeron/N40",
            "Basis Aturan": "RAM >= 16, tidak mengandung 'Celeron' atau 'N40' dalam nama CPU"
        },
        {
            "Kategori": "virtualisasi",
            "Label": "Jaringan & Virtualisasi",
            "Predikat": "cocok_untuk(ID, virtualisasi)",
            "Kondisi": "RAM >= 16GB",
            "Basis Aturan": "spesifikasi(ID, _, _, _, RAM, _, _, _), RAM >= 16"
        },
    ]
    
    for info in kategori_info:
        with st.expander(f"**{info['Label']}** (`{info['Kategori']}`)"):
            st.markdown(f"**Predikat:** `{info['Predikat']}`")
            st.markdown(f"**Kondisi:** {info['Kondisi']}")
            st.code(f"cocok_untuk(ID, {info['Kategori']}) :-\n    {info['Basis Aturan']}.", language="prolog")
            
            # Hitung laptop yang memenuhi
            try:
                count_query = f"findall(ID, cocok_untuk(ID, {info['Kategori']}), IDs), length(IDs, N)"
                r = engine.query_once(count_query)
                if r:
                    st.metric("Laptop yang memenuhi aturan ini:", r['N'])
            except Exception:
                pass
    
    st.markdown("")
    st.markdown("### 🏷️ Aturan Klasifikasi Kelas")
    st.code("""
kelas_laptop(ID, entry)    :- Harga < 10.
kelas_laptop(ID, midrange) :- Harga >= 10, Harga < 20.
kelas_laptop(ID, high_end) :- Harga >= 20, Harga < 35.
kelas_laptop(ID, flagship) :- Harga >= 35.
    """, language="prolog")

# ----- TAB 3: QUERY LANGSUNG -----
with tab_prolog:
    st.markdown("### 🔍 Eksekusi Query Prolog Langsung")
    st.warning(
        "⚠️ Fitur ini hanya untuk pengujian dan verifikasi oleh Admin. "
        "Hanya query berbentuk pencarian yang diizinkan (tidak ada assert/retract)."
    )
    
    contoh_queries = [
        "Pilih contoh query...",
        "jumlah_laptop(N)",
        "jumlah_per_kelas(midrange, N)",
        "rekomendasi_ideal(koding, midrange, Merk, Model, RAM, VGA, Harga)",
        "rekomendasi_ideal(gaming, entry, Merk, Model, RAM, VGA, Harga)",
        "rekomendasi_ideal(editing_berat, high_end, Merk, Model, RAM, VGA, Harga)",
        "rekomendasi_ideal(data_science, midrange, Merk, Model, RAM, VGA, Harga)",
        "cocok_untuk(asus_tuf_a15_4050, gaming)",
        "kelas_laptop(lenovo_ip_1, Kelas)",
        "spesifikasi_minimum(koding, SpesMin)",
        "alasan_rekomendasi(lenovo_ip_5, koding, Alasan)",
    ]
    
    selected_example = st.selectbox("Contoh Query:", contoh_queries)
    
    query_input = st.text_area(
        "Query Prolog:",
        value=selected_example if selected_example != contoh_queries[0] else "",
        height=80,
        placeholder="Contoh: rekomendasi_ideal(koding, midrange, Merk, Model, RAM, VGA, Harga)"
    )
    
    # Validasi keamanan query
    FORBIDDEN_TERMS = ['assert', 'retract', 'abolish', 'halt', 'shell', 'process_create']
    
    if st.button("▶️ Jalankan Query", type="primary"):
        if not query_input.strip():
            st.warning("Masukkan query terlebih dahulu.")
        elif any(term in query_input.lower() for term in FORBIDDEN_TERMS):
            st.error("❌ Query mengandung perintah yang tidak diizinkan.")
        else:
            with st.spinner("Menjalankan query..."):
                try:
                    results = engine.query(query_input.strip())
                    
                    if not results:
                        st.info("Query berhasil dijalankan namun tidak menghasilkan solusi (false).")
                    else:
                        st.success(f"✅ Ditemukan {len(results)} solusi.")
                        
                        for i, r in enumerate(results[:20], 1):
                            if r:
                                st.json({
                                    k: str(v) if hasattr(v, 'decode') else v
                                    for k, v in r.items()
                                })
                            else:
                                st.write(f"Solusi {i}: true")
                        
                        if len(results) > 20:
                            st.info(f"Menampilkan 20 dari {len(results)} solusi.")
                
                except Exception as e:
                    st.error(f"❌ Query gagal: {e}")
