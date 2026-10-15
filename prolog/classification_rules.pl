% ==========================================
% CLASSIFICATION RULES — LaptopExpert
% Berisi aturan klasifikasi kelas laptop
% dan kecocokan penggunaan (cocok_untuk/2)
% ==========================================

:- discontiguous kelas_laptop/2.
:- discontiguous cocok_untuk/2.

% ==========================================
% KELAS LAPTOP BERDASARKAN HARGA
% ==========================================

% ENTRY: Di bawah Rp10 juta
kelas_laptop(ID, entry) :-
    spesifikasi(ID, _, _, _, _, _, _, Harga),
    Harga < 10.

% MIDRANGE: Rp10 juta - Rp19 juta
kelas_laptop(ID, midrange) :-
    spesifikasi(ID, _, _, _, _, _, _, Harga),
    Harga >= 10, Harga < 20.

% HIGH-END: Rp20 juta - Rp34 juta
kelas_laptop(ID, high_end) :-
    spesifikasi(ID, _, _, _, _, _, _, Harga),
    Harga >= 20, Harga < 35.

% FLAGSHIP: Rp35 juta ke atas
kelas_laptop(ID, flagship) :-
    spesifikasi(ID, _, _, _, _, _, _, Harga),
    Harga >= 35.


% ==========================================
% ATURAN KECOCOKAN PENGGUNAAN
% cocok_untuk(+ID, +Kebutuhan)
% ==========================================

% 1. OFFICE: Semua laptop cocok untuk kuliah umum
cocok_untuk(ID, office) :-
    spesifikasi(ID, _, _, _, _, _, _, _).

% 2. KODING: RAM minimal 8GB untuk IDE + browser + terminal
cocok_untuk(ID, koding) :-
    spesifikasi(ID, _, _, _, RAM, _, _, _),
    RAM >= 8.

% 3. EDITING RINGAN: RAM min 8GB, bukan laptop termurah
cocok_untuk(ID, editing_ringan) :-
    spesifikasi(ID, _, _, _, RAM, _, _, Harga),
    RAM >= 8,
    Harga >= 7.

% 4. EDITING BERAT: RAM min 16GB + GPU dedicated atau Apple Silicon
cocok_untuk(ID, editing_berat) :-
    spesifikasi(ID, _, _, _, RAM, _, VGA, _),
    RAM >= 16,
    (sub_atom(VGA, _, _, _, 'RTX') ;
     sub_atom(VGA, _, _, _, 'Apple') ;
     sub_atom(VGA, _, _, _, 'RX 6') ;
     sub_atom(VGA, _, _, _, 'Arc')).

% 5. GAMING: Butuh GPU dedicated (RTX, GTX, atau AMD RX)
cocok_untuk(ID, gaming) :-
    spesifikasi(ID, _, _, _, _, _, VGA, _),
    (sub_atom(VGA, _, _, _, 'RTX') ;
     sub_atom(VGA, _, _, _, 'GTX') ;
     sub_atom(VGA, _, _, _, 'RX')).

% 6. STREAMING: RAM min 16GB + GPU dedicated RTX atau RX
cocok_untuk(ID, streaming) :-
    spesifikasi(ID, _, _, _, RAM, _, VGA, _),
    RAM >= 16,
    (sub_atom(VGA, _, _, _, 'RTX') ;
     sub_atom(VGA, _, _, _, 'RX')).

% 7. DATA SCIENCE: RAM min 16GB + CPU modern (bukan Celeron)
cocok_untuk(ID, data_science) :-
    spesifikasi(ID, _, _, CPU, RAM, _, _, _),
    RAM >= 16,
    \+ sub_atom(CPU, _, _, _, 'Celeron'),
    \+ sub_atom(CPU, _, _, _, 'N40').

% 8. VIRTUALISASI: RAM min 16GB untuk alokasi memori VM
cocok_untuk(ID, virtualisasi) :-
    spesifikasi(ID, _, _, _, RAM, _, _, _),
    RAM >= 16.
