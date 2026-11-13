"""
rsa_key_decryptor.py
--------------------
Decrypts an RSA-encrypted symmetric key using a private key file.
Reads d.key (private exponent + modulus) and EncryptedSharedKey,
then writes the plaintext integer to DecryptedSharedKey.

Usage:
    python3 rsa_key_decryptor.py [--private <d.key>] [--input <EncryptedSharedKey>] [--output <DecryptedSharedKey>]

Arguments:
    --private   Path to the private key file (format: d,n). Defaults to 'd.key'.
    --input     Path to the file containing the encrypted key integer. Defaults to 'EncryptedSharedKey'.
    --output    Path to write the decrypted key integer. Defaults to 'DecryptedSharedKey'.
"""

import os
import argparse


def decrypt_shared_key(private_path: str, input_path: str, output_path: str) -> None:
    for path in (private_path, input_path):
        if not os.path.exists(path):
            print(f"[-] File not found: {path}")
            return

    with open(private_path, "r") as f:
        d, n = map(int, f.read().split(","))

    with open(input_path, "r") as f:
        encrypted_k = int(f.read().strip())

    decrypted_k_int = pow(encrypted_k, d, n)

    with open(output_path, "w") as f:
        f.write(str(decrypted_k_int))

    print(f"[+] Decrypted key written to {output_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypt an RSA-encrypted symmetric key.")
    parser.add_argument("--private", default="d.key")
    parser.add_argument("--input",   default="EncryptedSharedKey")
    parser.add_argument("--output",  default="DecryptedSharedKey")
    args = parser.parse_args()
    decrypt_shared_key(args.private, args.input, args.output)
