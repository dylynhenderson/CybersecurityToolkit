"""
rsa_keygen.py
-------------
Generates a textbook RSA key pair and writes it to e.key and d.key.
Intended for CTF challenges and learning. NOT suitable for real-world use —
the primes (p=61, q=53) are intentionally tiny.

Output files:
    e.key   Public key:  e,n
    d.key   Private key: d,n

Usage:
    python3 rsa_keygen.py
"""


def generate_keys() -> None:
    p, q = 61, 53
    n = p * q                              # modulus
    e = 17                                 # public exponent
    d = 2753                               # private exponent: d*e ≡ 1 (mod φ(n))

    with open("e.key", "w") as f:
        f.write(f"{e},{n}")

    with open("d.key", "w") as f:
        f.write(f"{d},{n}")

    print(f"[+] Keys generated.")
    print(f"    Public  (e.key): e={e}, n={n}")
    print(f"    Private (d.key): d={d}, n={n}")
    print("    Warning: these primes are intentionally weak — for learning only.")


if __name__ == "__main__":
    generate_keys()
