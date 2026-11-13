# Cybersecurity Toolkit

A collection of simple network security monitoring (NSM) and cybersecurity tools I have worked on and created.

> **Use responsibly.** These tools are for learning, CTFs, and testing systems you own or have explicit written permission to test. You are responsible for how you use them.

## Tools at a Glance

| Tool | File / Folder | Type | Language | Purpose |
|------|---------------|------|----------|---------|
| [File Extension Counter](#file-extension-counter) | `fileExtension.py` | Utility | Python 3 | Counts files per extension from a list of filenames |
| [Simple Port Scanner](#simple-port-scanner) | `simplePortScanner.py` | Recon / NSM | Python 3 | Multithreaded TCP connect scan of a target |
| [RSA Cracker](#rsa-cracker) | `rsaCracker.py` | Cryptography / CTF | Python 3 | Decrypts textbook RSA messages given `d` and `n` |
| [Hash Matcher](#hash-matcher) | `hash_matcher.py` | Forensics / CTF | Python 3 | Finds a file matching a target SHA-256 hash |
| [Signature Verifier](#signature-verifier) | `signature_verifier.py` | Cryptography | Python 3 | Verifies RSA-signed files against a PEM public key |
| [RSA Key Generator](#rsa-key-generator) | `rsa_keygen.py` | Cryptography / CTF | Python 3 | Generates a textbook RSA key pair for learning and CTFs |
| [RSA Key Decryptor](#rsa-key-decryptor) | `rsa_key_decryptor.py` | Cryptography / CTF | Python 3 | Decrypts an RSA-encrypted symmetric key using a private key file |
| [AES Decryptor](#aes-decryptor) | `aes_decryptor.py` | Cryptography / CTF | Python 3 | Decrypts AES-CBC encrypted files with a hex or file-derived key |
| [Smart History Guard](#smart-history-guard) | `smartHistoryGuard/` | Browser defense | JavaScript (Chrome MV3) | Blocks back-button hijacking and history flooding |

---

## File Extension Counter

**File:** `fileExtension.py`

**Description:** Reads a list of filenames and reports how many files exist for each extension. Useful for quickly profiling a set of files, for example when triaging a directory listing.

**Requirements:** Python 3 (standard library only).

**Usage:**
```bash
python3 fileExtension.py
```

**Input (stdin):**
1. A number `N`, the count of filenames that follow.
2. `N` lines, each containing one filename.

**Example:**
```
3
report.pdf
notes.txt
summary.pdf
```
Output:
```
pdf 2
txt 1
```
Extensions are printed in the order they were first seen.

**Limitations:**
- Takes the text after the first `.`, so `archive.tar.gz` is counted as `tar`.
- A filename with no `.` will raise an error.

---

## Simple Port Scanner

**File:** `simplePortScanner.py`

**Description:** A multithreaded TCP connect scanner. It spreads the work across 100 threads and reports which ports accept a connection.

**Requirements:** Python 3 (standard library only).

**Usage:**
```bash
python3 simplePortScanner.py
```

**Prompts:**
- `Target IP:` the IPv4 address or hostname to scan.
- `How many ports do you want to scan?:` scans ports `1` up to, but not including, this number.

**Example output:**
```
Port Open:  22
Port Open:  80
Open Ports are:  [22, 80]
```

**Notes and limitations:**
- Full TCP connect scan only (no SYN or UDP scanning), so it is easy to detect in logs.
- Sockets have no timeout set, so filtered ports can make scans slow.
- Results are printed in the order threads finish, not sorted.
- **Only scan hosts you own or are authorized to test.**

---

## RSA Cracker

**File:** `rsaCracker.py`

**Description:** Decrypts messages encrypted with textbook RSA, one character per number. Built for CTF-style challenges where the private exponent `d` can be worked out from the given values.

**Requirements:** Python 3 (standard library only).

**Usage:**
```bash
python3 rsaCracker.py
```

**Prompts:**
- `Message to Decrypt:` the ciphertext numbers separated by spaces.
- `D Value:` the private exponent `d`. The script links a Wolfram Alpha widget for calculating it.
- `N Value (Given):` the modulus `n`.

**How it works:** Each ciphertext number `c` is decrypted as `c^d mod n`, and the result is converted to a character with `chr()`. The characters are joined into the plaintext.

**Notes and limitations:**
- Only works for small, textbook RSA (no padding, one character per block). It is not a tool for breaking real-world RSA.
- You must already know or derive `d`.
- The calculation `int(x)**d % n` builds a very large number first. Python's built-in `pow(x, d, n)` is much faster for large exponents.
- For learning and CTFs only.

---

## Hash Matcher

**File:** `hash_matcher.py`

**Description:** Scans a directory for the file whose SHA-256 hash matches a target hash. Accepts both raw binary digests and hex-encoded digests. Useful for file integrity checks and CTF challenges where you are given a hash and need to identify which file it belongs to.

**Requirements:** Python 3 (standard library only).

**Usage:**
```bash
python3 hash_matcher.py --hash <hash_file> --dir <search_dir>
```

**Arguments:**
- `--hash` Path to a file containing the target SHA-256 hash (binary or hex). Defaults to `target_hash.txt`.
- `--dir` Directory to search. Defaults to `files/`.

**Example:**
```bash
python3 hash_matcher.py --hash target_hash.txt --dir ./samples
```
Output:
```
[+] Matching file found: document_b.pdf
```

**Limitations:**
- SHA-256 only.
- Stops at the first match; does not report duplicates.

---

## Signature Verifier

**File:** `signature_verifier.py`

**Description:** Verifies RSA-signed files against a PEM public key using PKCS#1 v1.5 / SHA-256. For each `.exe` in the target directory it looks for a matching `.exe.sign` file and reports whether the signature is valid or invalid.

**Requirements:** Python 3, `cryptography` library.
```bash
pip install cryptography
```

**Usage:**
```bash
python3 signature_verifier.py --key <public_key.pem> --dir <files_dir>
```

**Arguments:**
- `--key` Path to the PEM-encoded public key. Defaults to `public.pem`.
- `--dir` Directory containing the files and `.sign` pairs. Defaults to `files/`.

**Example:**
```bash
python3 signature_verifier.py --key public.pem --dir ./binaries
```
Output:
```
[+] Valid signature: installer.exe
[-] Invalid signature: patch.exe
```

**Limitations:**
- Only processes `.exe` files; the companion signature file must be named `<filename>.exe.sign`.
- PKCS#1 v1.5 with SHA-256 only.

---

## RSA Key Generator

**File:** `rsa_keygen.py`

**Description:** Generates a textbook RSA key pair and writes it to `e.key` and `d.key`. Intended for CTF challenges and paired learning with `rsaCracker.py` and `rsa_key_decryptor.py`.

**Requirements:** Python 3 (standard library only).

**Usage:**
```bash
python3 rsa_keygen.py
```

**Output files:**
- `e.key` — Public key in the format `e,n`.
- `d.key` — Private key in the format `d,n`.

**Example output:**
```
[+] Keys generated.
    Public  (e.key): e=17, n=3233
    Private (d.key): d=2753, n=3233
    Warning: these primes are intentionally weak — for learning only.
```

**Limitations:**
- Uses fixed primes `p=61, q=53`. The resulting modulus is tiny and trivially factorable.
- **Not suitable for any real-world use.** For learning and CTFs only.

---

## RSA Key Decryptor

**File:** `rsa_key_decryptor.py`

**Description:** Decrypts an RSA-encrypted symmetric key integer using a private key file. Reads the private exponent and modulus from a key file, applies `pow(c, d, n)`, and writes the plaintext integer out. Pairs naturally with `rsa_keygen.py`.

**Requirements:** Python 3 (standard library only).

**Usage:**
```bash
python3 rsa_key_decryptor.py [--private d.key] [--input EncryptedSharedKey] [--output DecryptedSharedKey]
```

**Arguments:**
- `--private` Path to the private key file (format: `d,n`). Defaults to `d.key`.
- `--input` File containing the encrypted key integer. Defaults to `EncryptedSharedKey`.
- `--output` File to write the decrypted key integer to. Defaults to `DecryptedSharedKey`.

**Example:**
```bash
python3 rsa_key_decryptor.py --private d.key --input EncryptedSharedKey --output DecryptedSharedKey
```
Output:
```
[+] Decrypted key written to DecryptedSharedKey.
```

**Limitations:**
- Operates on integer values only; not a general-purpose RSA decryption tool.
- For learning and CTFs only.

---

## AES Decryptor

**File:** `aes_decryptor.py`

**Description:** Decrypts AES-CBC encrypted files with PKCS7 padding. Supports two key sources: a literal hex string or a file whose MD5 hash is used as the key. The expected file format is 16 bytes of IV followed by the ciphertext.

**Requirements:** Python 3, `cryptography` library.
```bash
pip install cryptography
```

**Usage:**
```bash
# Literal hex key:
python3 aes_decryptor.py --input <encrypted_file> --key-hex <32_char_hex>

# File-derived MD5 key:
python3 aes_decryptor.py --input <encrypted_file> --key-file <key_source_file>

# Write to file instead of stdout:
python3 aes_decryptor.py --input <encrypted_file> --key-hex <hex> --output plaintext.txt
```

**Arguments:**
- `--input` The encrypted input file (required).
- `--key-hex` A 32-character hex string representing a 16-byte AES key.
- `--key-file` A file whose MD5 hash is used as the AES key.
- `--output` Write plaintext to this file instead of printing to stdout.

**Example:**
```bash
python3 aes_decryptor.py --input Encrypted4 --key-hex d005a7d2470ea8c1818bead3fc239d64
python3 aes_decryptor.py --input Encrypted5 --key-file keySource.py
```

**Limitations:**
- AES-CBC with PKCS7 padding only.
- File-derived keys use MD5, which produces a fixed 16-byte (AES-128) key.
- Encrypted file must begin with a 16-byte IV.

---

## Smart History Guard

**Folder:** `smartHistoryGuard/`

**Description:** A Chrome (Manifest V3) extension that stops malicious back-button hijacking and history flooding while leaving legitimate single-page-app (SPA) navigation alone.

**How it works:**
- Wraps `history.pushState` in the page's main world.
- Converts identical-URL pushes and gesture-less bursts into `replaceState`.
- Allows hash changes, modal or tab state changes, and pushes that follow a real user click or keypress.
- Detects instant same-origin redirects after the Back button and skips back an extra step.
- Includes a popup with a global on/off toggle and a per-site "omit" list.

**Install (unpacked):**
1. Open `chrome://extensions` and enable **Developer mode**.
2. Click **Load unpacked** and select the `smartHistoryGuard/` folder.
3. To test on local files, also enable **Allow access to file URLs** for the extension.

**Testing:** Open `smartHistoryGuard/test.html` in Chrome (serving it with `python3 -m http.server` works best), click the buttons with a real mouse, and compare each result against its expected value.

**Files:**

| File | Role |
|------|------|
| `manifest.json` | Extension configuration and permissions |
| `injector.js` | Page-level guard that intercepts `pushState` |
| `content.js` | Passes stored settings to the injector |
| `background.js` | Detects redirect traps through navigation events |
| `popup.html`, `popup.js` | Toggle UI |
| `test.html` | Manual test bench |

**Privacy:** No data is collected or sent anywhere. Settings stay in `chrome.storage.local`, and the extension makes no network requests.

**Disclaimer:** The extension changes how the History API behaves, so some sites may not work as expected. Use the per-site omit toggle if one breaks. Provided as is, with no warranty.

---

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Dylan Henderson and contributors.