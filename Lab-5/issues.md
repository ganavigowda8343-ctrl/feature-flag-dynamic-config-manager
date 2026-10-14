# Lab 5: Static Code Analysis — Identified Issues & Resolutions

This document catalogs the code quality, security vulnerabilities, and PEP 8 style violations detected in `hotel_booking_system.py` using **Bandit**, **Pylint**, and **Flake8**, along with their descriptions and applied fix strategies.

---

## Issue Table

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| **OS Command Injection** (`B605`) | Bandit (Security: High) | 58 | Executing shell processes using `os.system("echo ... " + filename)` allows shell injection if the filename contains special shell characters or command separators (CWE-78). | Replaced the shell process execution (`os.system`) with Python's built-in `print()` function, eliminating external process invocation and command injection vectors. |
| **Weak Cryptographic Hash Algorithm** (`B324`) | Bandit (Security: High) | 47 | Use of weak and collision-vulnerable `hashlib.md5()` for hashing guest IDs (CWE-327). | Upgraded hashing mechanism to modern, collision-resistant `hashlib.sha256()`. |
| **Arbitrary Code Execution via `eval`** (`B307`, `W0123`) | Bandit (Security: Medium) / Pylint | 42 | Using `eval(rate_expr)` to calculate seasonal rate dynamically exposes the application to arbitrary code execution if an untrusted rate string is provided. | Implemented a safe AST evaluator (`_safe_eval_ast`) using Python's `ast` module and `operator` mappings to evaluate arithmetic expressions strictly without executing arbitrary code. |
| **Cryptographically Insecure Pseudo-Random Generator** (`B311`) | Bandit (Security: Low) | 51 | Using `random.randint(1000, 9999)` for booking reference generation relies on Mersenne Twister PRNG, which is predictable and unsuitable for security/reference identifiers (CWE-330). | Replaced `random.randint` with Python's cryptographically secure standard library module `secrets` (`secrets.randbelow(9000) + 1000`). |
| **Hardcoded Secret Key / Token** (`B105`) | Bandit (Security: Low) | 62 | Hardcoded secret token string `HOTEL_ADMIN_RESERVATION_TOKEN_2026` stored directly in source code (CWE-259). | Configured token retrieval from environment variables using `os.getenv("HOTEL_SECRET_KEY", default)` to keep secrets out of hardcoded source code. |
| **Silent Exception Swallowing (`try-except-pass`)** (`B110`, `W0702`, `E722`) | Bandit (Security: Low) / Pylint / Flake8 | 26 | Bare `except:` catching all exceptions with `pass` hides legitimate bugs (such as `TypeError` or `NameError`) and swallows unexpected errors silently (CWE-703). | Replaced exception suppression with an explicit membership check (`if room_num in room_inventory:`) to handle unbooked/missing rooms safely and predictably. |
| **Mutable Default Argument** (`W0102`) | Pylint (Quality: Warning / Bug) | 15 | `booking_log=[]` is defined as a default parameter. In Python, mutable default arguments are evaluated only once at function definition time and shared across calls, creating unintended state retention. | Changed default parameter value to `booking_log=None` and initialized `booking_log = []` inside the function body when `booking_log is None`. |
| **Unclosed File & Unspecified Encoding** (`R1732`, `W1514`) | Pylint (Quality: Refactor) | 55 | `open(filename, "w")` without a context manager (`with`) risks resource leaks if an error occurs before `f.close()`; also lacks explicit UTF-8 encoding specification. | Refactored file operations to use `with open(filename, "w", encoding="utf-8") as ledger_file:` ensuring deterministic closure and cross-platform encoding compatibility. |
| **Invalid Function Naming Convention** (`C0103`) | Pylint (Style: Convention) | 15 | Function name `bookRoom` uses camelCase instead of the standard Python snake_case convention mandated by PEP 8. | Renamed `bookRoom` to `book_room` in snake_case format to adhere to PEP 8 naming standards. |
| **Unused Import & Unused Local Variables** (`W0611`, `W0612`, `F401`, `F841`) | Pylint / Flake8 | 6, 31, 41 | Unused import `math` and unused variables `cleaning_deposit` and `base_price` (the latter only read inside string eval) add dead code and clutter. | Removed unused `import math`, eliminated redundant `cleaning_deposit`, and correctly utilized `base_price` in the AST-based rate evaluator. |
| **Direct Comparison to Singleton `None`** (`C0121`, `E711`) | Pylint / Flake8 | 32 | Comparison `room_inventory.get(room_num) == None` uses equality operator `==` instead of identity comparison `is None`. | Changed comparison to idiomatic `room is None`. |
| **Redundant If-Else Boolean Logic** (`R1703`, `R1705`) | Pylint (Quality: Refactor) | 34 | `if not room_inventory[room_num]["is_booked"]: return True else: return False` contains redundant branching and unnecessary `else` after `return`. | Simplified the status check to return the boolean evaluation directly: `return not room["is_booked"]`. |
| **Missing Module and Function Docstrings** (`C0116`) | Pylint (Style: Convention) | Multiple | Functions lacked PEP 257 docstrings explaining their parameters, behavior, and return values. | Added docstrings to all functions and module components detailing their purpose and interface. |
| **Line Length Exceeds PEP 8 Limit** (`E501`) | Flake8 (Style: Error) | 19 | Line length of 80 characters exceeded the standard PEP 8 limit of 79 characters. | Rewrote string formatting using concise f-string syntax, bringing line length well below 79 characters. |
| **Missing Final Newline** (`C0304`, `W292`) | Pylint / Flake8 | 73 | Source file was missing a trailing POSIX newline at the end of the file. | Added terminating newline character `\n` to end of file. |

---

## Summary of Verification Results

- **Bandit Score:** 0 issues found across all severity levels (Clean).
- **Pylint Score:** **10.00 / 10.00** (Perfect score, surpassing the > 9.5 lab target).
- **Flake8 Score:** 0 violations (100% PEP 8 compliant).
