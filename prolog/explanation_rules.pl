% ==========================================
% EXPLANATION RULES — LaptopExpert
% Aturan untuk menghasilkan penjelasan
% mengapa laptop direkomendasikan
% ==========================================

:- discontiguous alasan_rekomendasi/3.
:- discontiguous spesifikasi_minimum/2.
:- discontiguous spesifikasi_ideal/2.
:- discontiguous profil_penggunaan/2.
:- discontiguous tips_kebutuhan/2.

% ==========================================
% ALASAN REKOMENDASI PER KATEGORI
% alasan_rekomendasi(+ID, +Kebutuhan, -Alasan)
% ==========================================

alasan_rekomendasi(ID, office, Alasan) :-
    spesifikasi(ID, _, Model, _, RAM, Storage, _, _),
    format(atom(Alasan),
        '~w cocok untuk kuliah umum dengan RAM ~wGB dan storage ~wGB, cukup untuk dokumen, presentasi, dan browsing.',
        [Model, RAM, Storage]).

alasan_rekomendasi(ID, koding, Alasan) :-
    spesifikasi(ID, _, Model, CPU, RAM, Storage, _, _),
    format(atom(Alasan),
        '~w cocok untuk pemrograman dengan RAM ~wGB (memenuhi syarat min 8GB untuk IDE+browser+terminal) dan prosesor ~w. Storage ~wGB cukup untuk project dan tools.',
        [Model, RAM, CPU, Storage]).

alasan_rekomendasi(ID, editing_ringan, Alasan) :-
    spesifikasi(ID, _, Model, CPU, RAM, _, _, Harga),
    format(atom(Alasan),
        '~w cocok untuk editing ringan (Figma, Canva, Photoshop dasar) dengan RAM ~wGB dan CPU ~w. Laptop di kelas Rp~w juta sudah memadai untuk tugas desain grafis ringan.',
        [Model, RAM, CPU, Harga]).

alasan_rekomendasi(ID, editing_berat, Alasan) :-
    spesifikasi(ID, _, Model, CPU, RAM, _, VGA, _),
    format(atom(Alasan),
        '~w cocok untuk editing berat (video 4K, 3D render, After Effects) dengan RAM ~wGB, GPU ~w, dan CPU ~w. Kombinasi GPU dedicated + RAM besar krusial untuk render berat.',
        [Model, RAM, VGA, CPU]).

alasan_rekomendasi(ID, gaming, Alasan) :-
    spesifikasi(ID, _, Model, CPU, RAM, _, VGA, _),
    format(atom(Alasan),
        '~w cocok untuk gaming berkat GPU dedicated ~w yang menangani rendering grafis. CPU ~w dan RAM ~wGB mendukung performa gaming yang stabil.',
        [Model, VGA, CPU, RAM]).

alasan_rekomendasi(ID, streaming, Alasan) :-
    spesifikasi(ID, _, Model, CPU, RAM, _, VGA, _),
    format(atom(Alasan),
        '~w cocok untuk gaming + streaming dengan RAM ~wGB (cukup untuk game + OBS + browser) dan GPU ~w yang mendukung hardware encoding. CPU ~w menangani multitasking berat.',
        [Model, RAM, VGA, CPU]).

alasan_rekomendasi(ID, data_science, Alasan) :-
    spesifikasi(ID, _, Model, CPU, RAM, Storage, VGA, _),
    format(atom(Alasan),
        '~w cocok untuk data science dengan RAM ~wGB (memadai untuk Jupyter Notebook, pandas, scikit-learn), CPU ~w untuk komputasi, dan storage ~wGB untuk dataset. GPU ~w dapat mendukung training model ringan.',
        [Model, RAM, CPU, Storage, VGA]).

alasan_rekomendasi(ID, virtualisasi, Alasan) :-
    spesifikasi(ID, _, Model, CPU, RAM, _, _, _),
    format(atom(Alasan),
        '~w cocok untuk virtualisasi dengan RAM ~wGB yang dapat dialokasikan untuk VM (rekomendasi: sisakan min 4GB untuk host OS). CPU ~w mendukung instruksi virtualisasi (VT-x/AMD-V).',
        [Model, RAM, CPU]).

% ==========================================
% SPESIFIKASI MINIMUM PER KEBUTUHAN
% spesifikasi_minimum(+Kebutuhan, -SpesMin)
% ==========================================

spesifikasi_minimum(office,        'RAM: 8GB | Storage: 256GB SSD | CPU: Prosesor modern apapun').
spesifikasi_minimum(koding,        'RAM: 8GB (ideal 16GB) | Storage: 256GB SSD | CPU: Intel i3-Gen10+ / Ryzen 3 5000+').
spesifikasi_minimum(editing_ringan,'RAM: 8GB | Storage: 256GB SSD | CPU: Intel i5 / Ryzen 5').
spesifikasi_minimum(editing_berat, 'RAM: 16GB | Storage: 512GB SSD | GPU: RTX 3050+ / RX 6500M+ / Apple M2+').
spesifikasi_minimum(gaming,        'GPU: RTX 2050 / RTX 3050 / RX 6500M | RAM: 8GB | CPU: Intel i5-H / Ryzen 5-H').
spesifikasi_minimum(streaming,     'GPU: RTX 3050+ (dukung NVENC) | RAM: 16GB | CPU: Intel i7-H / Ryzen 7-HS').
spesifikasi_minimum(data_science,  'RAM: 16GB | Storage: 512GB SSD | CPU: Intel i5 Gen12+ / Ryzen 5 7000+').
spesifikasi_minimum(virtualisasi,  'RAM: 16GB (min untuk 1 VM) | Storage: 512GB SSD | CPU: dengan VT-x atau AMD-V').

% ==========================================
% SPESIFIKASI IDEAL PER KEBUTUHAN
% spesifikasi_ideal(+Kebutuhan, -SpesIdeal)
% ==========================================

spesifikasi_ideal(office,        'RAM: 16GB | Storage: 512GB SSD | CPU: Intel i5 / Ryzen 5 | Baterai: 10+ jam').
spesifikasi_ideal(koding,        'RAM: 16GB | Storage: 512GB SSD | CPU: Intel i5-H / Ryzen 7 | Display: 14\'+').
spesifikasi_ideal(editing_ringan,'RAM: 16GB | Storage: 512GB SSD | GPU: Dedicated entry-mid | Display: IPS/OLED').
spesifikasi_ideal(editing_berat, 'RAM: 32GB | Storage: 1TB SSD | GPU: RTX 4060+ / Apple M3 Pro+ | Display: 4K / DCI-P3').
spesifikasi_ideal(gaming,        'GPU: RTX 4060+ | RAM: 16GB | Storage: 1TB SSD | Display: 144Hz+ | CPU: i7-H / R9-HS').
spesifikasi_ideal(streaming,     'GPU: RTX 4060+ | RAM: 32GB | CPU: i7-HX / R9-HS | Storage: 1TB SSD').
spesifikasi_ideal(data_science,  'RAM: 32GB | GPU: RTX (CUDA) | Storage: 1TB SSD | CPU: i7-H / R9-HS').
spesifikasi_ideal(virtualisasi,  'RAM: 32GB+ | Storage: 512GB+ SSD | CPU: multi-core tinggi (i7-H / R9-HS)').

% ==========================================
% PROFIL PENGGUNAAN PER KEBUTUHAN
% profil_penggunaan(+Kebutuhan, -Profil)
% ==========================================

profil_penggunaan(office,        'Mahasiswa yang membutuhkan laptop untuk kuliah umum: dokumen Word/Excel, presentasi PowerPoint, browsing, video call, dan tugas sehari-hari.').
profil_penggunaan(koding,        'Mahasiswa atau developer yang membutuhkan laptop untuk coding: menjalankan IDE (VSCode, IntelliJ, dll.), terminal/CLI, browser testing, dan version control.').
profil_penggunaan(editing_ringan,'Mahasiswa desain atau kreator konten yang menggunakan Figma, Canva, Adobe Photoshop (dasar), dan video editing 1080p ringan.').
profil_penggunaan(editing_berat, 'Desainer grafis atau videografer profesional yang mengerjakan editing video 4K, 3D rendering (Blender, Cinema 4D), dan Adobe After Effects.').
profil_penggunaan(gaming,        'Gamer yang ingin bermain game AAA atau game kompetitif dengan frame rate yang memadai. GPU dedicated adalah komponen paling kritis.').
profil_penggunaan(streaming,     'Gamer yang sekaligus melakukan live streaming, membutuhkan CPU dan GPU kuat untuk menjalankan game + OBS secara bersamaan.').
profil_penggunaan(data_science,  'Mahasiswa data science atau ML yang menjalankan Jupyter Notebook, library Python (pandas, numpy, scikit-learn, TensorFlow ringan), dan analisis dataset.').
profil_penggunaan(virtualisasi,  'Mahasiswa jaringan komputer atau DevOps yang menjalankan virtual machine (VirtualBox, VMware), Docker, atau lab jaringan virtual (GNS3, EVE-NG).').

% ==========================================
% TIPS PER KEBUTUHAN
% tips_kebutuhan(+Kebutuhan, -Tips)
% ==========================================

tips_kebutuhan(office,        'Prioritaskan baterai tahan lama dan bobot ringan. RAM 8GB sudah cukup, tapi 16GB lebih nyaman untuk multitasking.').
tips_kebutuhan(koding,        'RAM adalah prioritas utama. 8GB minimum, 16GB sangat direkomendasikan jika berencana menjalankan Docker atau VM ringan.').
tips_kebutuhan(editing_ringan,'Layar dengan color accuracy baik (IPS atau OLED) lebih penting dari GPU. RAM 16GB membuat pekerjaan lebih lancar.').
tips_kebutuhan(editing_berat, 'GPU VRAM minimal 6GB untuk editing 4K. Display dengan coverage warna tinggi (sRGB 100% atau DCI-P3 90%+) sangat membantu.').
tips_kebutuhan(gaming,        'GPU adalah penentu utama. RTX 4050 6GB sudah cukup untuk game 1080p. Perhatikan juga sistem pendingin laptop gaming.').
tips_kebutuhan(streaming,     'RTX series memiliki NVENC encoder yang jauh lebih efisien dari CPU encoding. RAM 16GB minimum untuk stream tanpa lag.').
tips_kebutuhan(data_science,  'RAM 16GB minimum, 32GB lebih nyaman untuk dataset besar. GPU CUDA (RTX) memberi keuntungan besar untuk training model.').
tips_kebutuhan(virtualisasi,  'Semakin besar RAM semakin baik. Setiap VM butuh ~2-4GB. SSD NVMe mempercepat boot VM secara signifikan.').
