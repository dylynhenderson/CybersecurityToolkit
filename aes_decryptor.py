"""
aes_decryptor.py
----------------
Decrypts AES-CBC encrypted files with PKCS7 padding.
Supports two key sources:

  --key-hex   A literal 32-character hex string (16-byte key).
  --key-file  A file whose MD5 hash is used as the key (file-derived key).

The encrypted file format expected: first 16 bytes are the IV, remainder is ciphertext.

Usage:
    # Literal hex key (equivalent to old D4.py):
    python3 aes_decryptor.py --input Encrypted4 --key-hex d005a7d2470ea8c1818bead3fc239d64

    # File-derived MD5 key (equivalent to old D5.py):
    python3 aes_decryptor.py --input Encrypted5 --key-file R5.py

    # Write output to a file instead of stdout:
    python3 aes_decryptor.py --input Encrypted4 --key-hex d005a7d2470ea8c1818bead3fc239d64 --output plaintext.txt

Requirements:
    pip install cryptography
"""

import sys
import hashlib
import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def build_key(key_hex: str | None, key_file: str | None) -> bytes:
    if key_hex:
        raw = bytes.fromhex(key_hex)
        if len(raw) not in (16, 24, 32):
            sys.exit("[-] Key must be 16, 24 or 32 bytes (32, 48 or 64 hex chars).")
        return raw
    if key_file:
        h = hashlib.md5()
        with open(key_file, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.digest()   # always 16 bytes
    sys.exit("[-] Provide either --key-hex or --key-file.")


def decrypt(input_path: str, key: bytes, output_path: str | None) -> None:
    with open(input_path, "rb") as f:
        data = f.read()

    if len(data) < 32:
        sys.exit("[-] File too short to contain IV + at least one cipher block.")

    iv, ciphertext = data[:16], data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()

    if output_path:
        with open(output_path, "wb") as f:
            f.write(plaintext)
        print(f"[+] Decrypted output written to {output_path}.")
    else:
        print(plaintext.decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AES-CBC file decryptor.")
    parser.add_argument("--input",   required=True, help="Encrypted input file.")
    parser.add_argument("--key-hex", help="16-byte key as a 32-char hex string.")
    parser.add_argument("--key-file",help="File whose MD5 hash is used as the key.")
    parser.add_argument("--output",  help="Write plaintext here instead of stdout.")
    args = parser.parse_args()

    key = build_key(args.key_hex, args.key_file)
    decrypt(args.input, key, args.output)
