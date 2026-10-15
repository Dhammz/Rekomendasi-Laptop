"""
generate_hash.py — Script bantu untuk membuat hash password SHA-256
Jalankan: python generate_hash.py
"""
import hashlib

def generate_hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    print("=" * 50)
    print("LaptopExpert — Password Hash Generator")
    print("=" * 50)
    
    while True:
        password = input("\nMasukkan password (atau 'exit' untuk keluar): ").strip()
        if password.lower() == 'exit':
            break
        if not password:
            print("Password tidak boleh kosong.")
            continue
        
        hashed = generate_hash(password)
        print(f"Hash SHA-256: {hashed}")
        print(f"Salin hash ini ke secrets.toml")
