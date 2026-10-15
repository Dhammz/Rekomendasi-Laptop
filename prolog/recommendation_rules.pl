% ==========================================
% RECOMMENDATION RULES — LaptopExpert
% Aturan utama menghasilkan rekomendasi
% berdasarkan kebutuhan + kelas anggaran
% ==========================================

:- use_module(library(aggregate)).
:- discontiguous rekomendasi_ideal/7.
:- discontiguous rekomendasi_kompleks/6.
:- discontiguous rekomendasi_dengan_ram/8.
:- discontiguous rekomendasi_dengan_gpu/8.

% ==========================================
% REKOMENDASI STANDAR
% rekomendasi_ideal(+Kebutuhan, +Kelas, -Merk, -Model, -RAM, -VGA, -Harga)
% ==========================================
rekomendasi_ideal(Kebutuhan, Kelas, Merk, Model, RAM, VGA, Harga) :-
    cocok_untuk(ID, Kebutuhan),
    kelas_laptop(ID, Kelas),
    spesifikasi(ID, Merk, Model, _, RAM, _, VGA, Harga).

% ==========================================
% REKOMENDASI KOMBINASI DUA KEBUTUHAN
% rekomendasi_kompleks(+K1, +K2, +Kelas, -Merk, -Model, -Harga)
% ==========================================
rekomendasi_kompleks(Kebutuhan1, Kebutuhan2, Kelas, Merk, Model, Harga) :-
    Kebutuhan1 \= Kebutuhan2,
    cocok_untuk(ID, Kebutuhan1),
    cocok_untuk(ID, Kebutuhan2),
    kelas_laptop(ID, Kelas),
    spesifikasi(ID, Merk, Model, _, _, _, _, Harga).

% ==========================================
% REKOMENDASI DENGAN PRIORITAS RAM BESAR (>= 16GB)
% rekomendasi_dengan_ram(+Kebutuhan, +Kelas, -Merk, -Model, -RAM, -Storage, -VGA, -Harga)
% ==========================================
rekomendasi_dengan_ram(Kebutuhan, Kelas, Merk, Model, RAM, Storage, VGA, Harga) :-
    cocok_untuk(ID, Kebutuhan),
    kelas_laptop(ID, Kelas),
    spesifikasi(ID, Merk, Model, _, RAM, Storage, VGA, Harga),
    RAM >= 16.

% ==========================================
% REKOMENDASI DENGAN GPU DEDICATED
% rekomendasi_dengan_gpu(+Kebutuhan, +Kelas, -Merk, -Model, -RAM, -VGA, -Harga, -TipeGPU)
% ==========================================
rekomendasi_dengan_gpu(Kebutuhan, Kelas, Merk, Model, RAM, VGA, Harga, TipeGPU) :-
    cocok_untuk(ID, Kebutuhan),
    kelas_laptop(ID, Kelas),
    spesifikasi(ID, Merk, Model, _, RAM, _, VGA, Harga),
    (
        sub_atom(VGA, _, _, _, 'RTX') -> TipeGPU = 'NVIDIA RTX'
        ; sub_atom(VGA, _, _, _, 'GTX') -> TipeGPU = 'NVIDIA GTX'
        ; sub_atom(VGA, _, _, _, 'RX') -> TipeGPU = 'AMD RX'
        ; sub_atom(VGA, _, _, _, 'Apple') -> TipeGPU = 'Apple GPU'
        ; TipeGPU = 'GPU Lain'
    ),
    TipeGPU \= 'GPU Lain'.

% ==========================================
% REKOMENDASI LENGKAP (semua detail)
% rekomendasi_lengkap(+Kebutuhan, +Kelas, -ID, -Merk, -Model, -CPU, -RAM, -Storage, -VGA, -Harga)
% ==========================================
rekomendasi_lengkap(Kebutuhan, Kelas, ID, Merk, Model, CPU, RAM, Storage, VGA, Harga) :-
    cocok_untuk(ID, Kebutuhan),
    kelas_laptop(ID, Kelas),
    spesifikasi(ID, Merk, Model, CPU, RAM, Storage, VGA, Harga).

% ==========================================
% STATISTIK UNTUK DASHBOARD
% ==========================================

% Hitung total laptop dalam database
jumlah_laptop(N) :-
    aggregate_all(count, spesifikasi(_, _, _, _, _, _, _, _), N).

% Hitung jumlah kategori kebutuhan yang tersedia
jumlah_kategori(8). % office, koding, editing_ringan, editing_berat, gaming, streaming, data_science, virtualisasi

% Hitung jumlah laptop per kelas
jumlah_per_kelas(Kelas, N) :-
    aggregate_all(count, kelas_laptop(_, Kelas), N).

% Cek apakah ada hasil untuk kombinasi kebutuhan + kelas
ada_hasil(Kebutuhan, Kelas) :-
    once(rekomendasi_ideal(Kebutuhan, Kelas, _, _, _, _, _)).
