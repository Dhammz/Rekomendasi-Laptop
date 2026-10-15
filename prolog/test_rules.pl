% ==========================================
% TEST RULES — LaptopExpert
% Pengujian aturan Prolog secara mandiri
% Jalankan: swipl -g 'run_tests' -t halt test_rules.pl
% ==========================================

:- use_module(library(plunit)).
:- consult('knowledge_base.pl').
:- consult('classification_rules.pl').
:- consult('recommendation_rules.pl').
:- consult('explanation_rules.pl').

% --- Uji Kelas Laptop ---
:- begin_tests(kelas_laptop).

test(entry_class) :-
    kelas_laptop(lenovo_ip_1, entry).

test(midrange_class) :-
    kelas_laptop(lenovo_ip_5, midrange).

test(high_end_class) :-
    kelas_laptop(mac_air_m2_16, high_end).

test(flagship_class) :-
    kelas_laptop(asus_rog_scar_18, flagship).

test(no_overlap, [forall(member(ID, [lenovo_ip_1, lenovo_ip_5, mac_air_m2_16, asus_rog_scar_18]))]) :-
    aggregate_all(count, kelas_laptop(ID, _), 1).

:- end_tests(kelas_laptop).

% --- Uji cocok_untuk ---
:- begin_tests(cocok_untuk).

test(gaming_gpu_rtx) :-
    cocok_untuk(asus_tuf_a15_4050, gaming).

test(gaming_gpu_rx) :-
    cocok_untuk(msi_bravo_15, gaming).

test(koding_8gb) :-
    cocok_untuk(asus_vivo_14, koding).

test(editing_berat_apple) :-
    cocok_untuk(mac_air_m2_16, editing_berat).

test(editing_berat_rtx) :-
    cocok_untuk(asus_tuf_a15_4050, editing_berat).

test(data_science_16gb) :-
    cocok_untuk(lenovo_ip_5, data_science).

test(virtualisasi_16gb) :-
    cocok_untuk(mac_air_m2_16, virtualisasi).

test(celeron_not_data_science) :-
    \+ cocok_untuk(lenovo_ip_1, data_science).

test(no_gpu_not_gaming) :-
    \+ cocok_untuk(lenovo_ip_5, gaming).

test(editing_berat_needs_gpu) :-
    \+ cocok_untuk(lenovo_ip_1, editing_berat).

:- end_tests(cocok_untuk).

% --- Uji Rekomendasi ---
:- begin_tests(rekomendasi).

test(koding_midrange_has_results) :-
    aggregate_all(count, rekomendasi_ideal(koding, midrange, _, _, _, _, _), N),
    N > 0.

test(gaming_entry_no_result) :-
    \+ rekomendasi_ideal(gaming, entry, _, _, _, _, _).

test(editing_berat_entry_no_result) :-
    \+ rekomendasi_ideal(editing_berat, entry, _, _, _, _, _).

test(gaming_midrange_has_gpu) :-
    rekomendasi_ideal(gaming, midrange, _, _, _, VGA, _),
    (sub_atom(VGA, _, _, _, 'RTX') ; sub_atom(VGA, _, _, _, 'RX')), !.

test(ram_filter_works) :-
    aggregate_all(count, rekomendasi_dengan_ram(koding, midrange, _, _, _, _, _, _), N),
    N > 0.

:- end_tests(rekomendasi).

:- run_tests.
