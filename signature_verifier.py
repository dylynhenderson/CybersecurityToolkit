"""
signature_verifier.py
---------------------
Verifies RSA-signed files using a PEM public key.
For each .exe in the target directory it looks for a matching .exe.sign file
and verifies the signature with PKCS#1 v1.5 / SHA-256.

Usage:
    python3 signature_verifier.py --key <public_key.pem> --dir <files_dir>

Arguments:
    --key   Path to the PEM-encoded public key. Defaults to 'public.pem'.
    --dir   Directory containing the files and .sign pairs. Defaults to 'files/'.

Requirements:
    pip install cryptography
"""

import os
import argparse
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


def verify_signatures(key_path: str, files_dir: str) -> None:
    if not os.path.isfile(key_path):
        print(f"[-] Public key not found: {key_path}")
        return
    if not os.path.isdir(files_dir):
        print(f"[-] Directory not found: {files_dir}")
        return

    with open(key_path, "rb") as f:
        public_key = load_pem_public_key(f.read())

    for filename in os.listdir(files_dir):
        if not filename.endswith(".exe"):
            continue

        exe_path = os.path.join(files_dir, filename)
        sig_path = exe_path + ".sign"

        if not os.path.exists(sig_path):
            continue

        with open(exe_path, "rb") as f:
            data = f.read()
        with open(sig_path, "rb") as f:
            signature = f.read()

        try:
            public_key.verify(signature, data, padding.PKCS1v15(), hashes.SHA256())
            print(f"[+] Valid signature: {filename}")
        except Exception:
            print(f"[-] Invalid signature: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify RSA-signed files.")
    parser.add_argument("--key", default="public.pem",
                        help="Path to the PEM public key.")
    parser.add_argument("--dir", default="files/",
                        help="Directory containing files and .sign pairs.")
    args = parser.parse_args()
    verify_signatures(args.key, args.dir)
