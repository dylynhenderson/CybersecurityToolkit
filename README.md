# Cybersecurity Toolkit

A collection of simple network security monitoring (NSM) and cybersecurity tools I have worked on and created.

> **Use responsibly.** These tools are for learning, CTFs, and testing systems you own or have explicit written permission to test. You are responsible for how you use them.

## Tools at a Glance

| Tool | File / Folder | Type | Language | Purpose |
|------|---------------|------|----------|---------|
| [File Extension Counter](#file-extension-counter) | `fileExtension.py` | Utility | Python 3 | Counts files per extension from a list of filenames |
| [Simple Port Scanner](#simple-port-scanner) | `simplePortScanner.py` | Recon / NSM | Python 3 | Multithreaded TCP connect scan of a target |
| [RSA Cracker](#rsa-cracker) | `rsaCracker.py` | Cryptography / CTF | Python 3 | Decrypts textbook RSA messages given `d` and `n` |
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

## Adding a New Tool (Template)

Copy this block for each new tool, delete the guidance in parentheses, and add a row to the table at the top.

```markdown
## Tool Name

**File / Folder:** `filename.py`

**Description:** (One or two sentences: what the tool does and why it is useful.)

**Requirements:** (Language version, third-party libraries, OS or permissions needed.)

**Usage:**
(Command to run, plus any arguments or prompts.)

**Input / Output:** (What the tool reads and what it prints or produces.)

**Example:**
(A short sample run with real-looking input and output.)

**Notes and limitations:** (Known issues, assumptions, speed or accuracy caveats, and legal or ethical notes such as "only use on systems you own".)
```

**Description guide**
- Start with what the tool *does*, then why it matters.
- Keep each section to roughly 10 to 20 lines. Put long write-ups in a separate file inside the tool's folder.
- Always include one runnable example.
- State clearly what the tool does *not* do.
- Add an authorization note for anything that probes networks, systems, or accounts.

---

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Dylan Henderson and contributors.
