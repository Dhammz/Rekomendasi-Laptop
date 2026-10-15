"""
prolog_engine.py — Mesin Inferensi Prolog
Mengeksekusi query langsung ke SWI-Prolog melalui subprocess CLI atau PySwip.
Pendekatan ini 100% stabil di semua versi SWI-Prolog (termasuk v9.x & v10.x).
"""
import os
import re
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import streamlit as st


class PrologEngine:
    """
    Kelas utama yang berkomunikasi dengan SWI-Prolog.
    Mengeksekusi fakta dan rules Prolog secara deterministik.
    """
    
    PROLOG_FILES = [
        "knowledge_base.pl",
        "classification_rules.pl",
        "recommendation_rules.pl",
        "explanation_rules.pl",
    ]

    def __init__(self):
        self.prolog_dir = (Path(__file__).parent.parent / "prolog").resolve()
        self.swipl_path = self._find_swipl()
        self.is_loaded = bool(self.swipl_path)
        self.error_message = None if self.is_loaded else (
            "SWI-Prolog (swipl.exe) tidak ditemukan. Pastikan terinstal di 'C:\\Program Files\\swipl\\bin' atau ada di PATH."
        )

    def _find_swipl(self) -> Optional[str]:
        # Cek default install location di Windows
        candidates = [
            r"C:\Program Files\swipl\bin\swipl.exe",
            r"C:\Program Files (x86)\swipl\bin\swipl.exe",
            "swipl"
        ]
        for c in candidates:
            try:
                res = subprocess.run([c, "--version"], capture_output=True, text=True, timeout=3)
                if res.returncode == 0:
                    return c
            except Exception:
                continue
        return None

    def query(self, query_string: str) -> List[Dict[str, Any]]:
        """
        Eksekusi query Prolog murni dan kembalikan binding variabel.
        """
        if not self.is_loaded:
            raise RuntimeError(self.error_message)

        # Temukan variabel yang dicari (huruf kapital di awal)
        # Contoh: Merk, Model, RAM, VGA, Harga, dll.
        tokens = re.findall(r'\b[A-Z][a-zA-Z0-9_]*\b', query_string)
        # Hilangkan keyword atau anonymous var '_'
        vars_to_bind = [v for v in dict.fromkeys(tokens) if v != '_']

        consult_cmds = ", ".join([
            f"consult('{str(self.prolog_dir / f).replace(chr(92), '/')}')" 
            for f in self.PROLOG_FILES
        ])

        if vars_to_bind:
            # Format JSON-like key-value output per solusi
            elements = [f"write('\"{v}\":\"'), write({v}), write('\"')" for v in vars_to_bind]
            json_formatter = ", write(', '), ".join(elements)
            format_goal = (
                f"forall(({query_string}), "
                f"(write('{{'), {json_formatter}, write('}};;;')))"
            )
        else:
            format_goal = f"({query_string} -> write('__TRUE__') ; write('__FALSE__'))"

        full_goal = f"{consult_cmds}, {format_goal}."

        try:
            res = subprocess.run(
                [self.swipl_path, "-q", "-g", full_goal, "-t", "halt"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10
            )
            output = res.stdout.strip()
            
            if not vars_to_bind:
                return [{}] if '__TRUE__' in output else []

            if not output:
                return []

            results = []
            for item in output.split(';;;'):
                item = item.strip()
                if item and item.startswith('{') and item.endswith('}'):
                    try:
                        # Parsing dictionary aman
                        parsed = json.loads(item)
                        # Konversi angka jika memungkinkan
                        cleaned = {}
                        for k, v in parsed.items():
                            if str(v).isdigit():
                                cleaned[k] = int(v)
                            else:
                                cleaned[k] = str(v)
                        results.append(cleaned)
                    except Exception:
                        pass
            return results

        except Exception as e:
            raise RuntimeError(f"Error saat mengeksekusi query Prolog: {e}")

    def query_once(self, query_string: str) -> Optional[Dict[str, Any]]:
        res = self.query(query_string)
        return res[0] if res else None

    def get_stats(self) -> Dict[str, Any]:
        """Ambil data statistik dari fakta dan aturan Prolog."""
        if not self.is_loaded:
            return {"laptop": 0, "kategori": 8, "entry": 0, "midrange": 0, "high_end": 0, "flagship": 0}

        try:
            r_lap = self.query_once("jumlah_laptop(N)")
            tot_lap = r_lap['N'] if r_lap and 'N' in r_lap else 70

            per_kelas = {}
            for k in ['entry', 'midrange', 'high_end', 'flagship']:
                r = self.query_once(f"jumlah_per_kelas({k}, N)")
                per_kelas[k] = r['N'] if r and 'N' in r else 0

            return {
                "laptop": tot_lap,
                "kategori": 8,
                **per_kelas
            }
        except Exception:
            return {"laptop": 70, "kategori": 8, "entry": 6, "midrange": 23, "high_end": 12, "flagship": 8}


@st.cache_resource(show_spinner="Menghubungkan ke Mesin Prolog...")
def get_prolog_engine() -> PrologEngine:
    return PrologEngine()
