"""
hash_matcher.py
---------------
Scans a directory for the file whose SHA-256 hash matches a target hash.
Accepts both raw binary digests and hex-encoded digests.

Usage:
    python3 hash_matcher.py --hash <hash_file> --dir <search_dir>

Arguments:
    --hash  Path to a file containing the target SHA-256 hash (binary or hex).
            Defaults to 'target_hash.txt'.
    --dir   Directory to search. Defaults to 'files/'.
"""

import os
import hashlib
import argparse


def find_matching_file(hash_path: str, search_dir: str) -> None:
    if not os.path.isfile(hash_path):
        print(f"[-] Hash file not found: {hash_path}")
        return
    if not os.path.isdir(search_dir):
        print(f"[-] Search directory not found: {search_dir}")
        return

    with open(hash_path, "rb") as f:
        target_hash = f.read().strip()

    for filename in os.listdir(search_dir):
        filepath = os.path.join(search_dir, filename)
        if not os.path.isfile(filepath):
            continue

        with open(filepath, "rb") as f:
            content = f.read()

        digest_bin = hashlib.sha256(content).digest()
        digest_hex = hashlib.sha256(content).hexdigest().encode("utf-8")

        if target_hash in (digest_bin, digest_hex):
            print(f"[+] Matching file found: {filename}")
            return

    print("[-] No matching file found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find a file by SHA-256 hash.")
    parser.add_argument("--hash", default="target_hash.txt",
                        help="File containing the target SHA-256 hash.")
    parser.add_argument("--dir", default="files/",
                        help="Directory to search.")
    args = parser.parse_args()
    find_matching_file(args.hash, args.dir)
