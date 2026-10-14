# Lab 5: Static Code Analysis — Hotel Booking System

**Course**: Software Engineering Lab (SE Lab) — PES University  
**Assigned System**: Problem Statement #43 — Hotel Room Reservation & Inventory Manager  
**File Analyzed**: `hotel_booking_system.py`  
**GitHub Repository**: [ganavigowda8343-ctrl/feature-flag-dynamic-config-manager](https://github.com/ganavigowda8343-ctrl/feature-flag-dynamic-config-manager)  

---

## 🎯 Executive Summary & Verification Results

All static analysis issues across **Bandit**, **Pylint**, and **Flake8** have been rectified. The program's core reservation, cancellation, surge rate calculation, guest hashing, and ledger export capabilities remain fully operational while meeting strict enterprise code quality and security standards.

| Static Analysis Tool | Category / Scope | Target Score | Final Score / Result | Status |
|---|---|---|---|---|
| **Bandit** | Security & Vulnerabilities (SAST) | 0 High/Medium Issues | **0 issues identified** (0 High, 0 Medium, 0 Low) | ✅ **PASSED** |
| **Pylint** | Code Quality, Smells & Design | $> 9.50 / 10.00$ | **10.00 / 10.00** (Perfect Score) | ✅ **PASSED** |
| **Flake8** | PEP 8 Formatting & Style Guide | 0 Violations | **0 violations** (100% Compliant) | ✅ **PASSED** |

---

## 📦 Required Deliverables

| Deliverable | File Link | Description |
|---|---|---|
| **Cleaned & Fixed Python Script** | [hotel_booking_system.py](hotel_booking_system.py) | Fully refactored script with 15+ issues resolved (10.00/10 rating). |
| **Documented Issue Table** | [issues.md](issues.md) | Exhaustive table cataloging all 15 findings (Type, Line, Description, Fix Approach). |
| **Lab Reflection Report** | [reflection.md](reflection.md) | In-depth answers to all four static code analysis reflection questions. |
| **Pylint Report** | [pylint_report.txt](pylint_report.txt) | Official Pylint evaluation log confirming **10.00/10**. |
| **Bandit Security Report** | [bandit_report.txt](bandit_report.txt) | Official Bandit security scan report confirming **0 vulnerabilities**. |
| **Flake8 Style Report** | [flake8_report.txt](flake8_report.txt) | Official Flake8 report confirming **0 PEP 8 violations**. |

---

## 🛠️ Step-by-Step Commit History (3-Tool Progression)

Per the lab requirement to make **3 commits** corresponding to the fixes raised by the three static analysis tools:

1. **Commit 1 (Bandit Fixes)**: `fix(security): resolve security vulnerabilities identified by Bandit`
   - Eliminated code injection via `eval()` by implementing a safe AST mathematical evaluator (`_safe_eval_ast`).
   - Eliminated OS shell injection (`B605`) by replacing `os.system()` with Python's built-in `print()`.
   - Upgraded weak MD5 hash (`B324`) to cryptographically secure `hashlib.sha256()`.
   - Replaced predictable pseudo-random generator (`B311`) with standard library `secrets`.
   - Secured administrative token string (`B105`) via `os.getenv()`.
   - Eliminated silent `try-except-pass` block (`B110`).

2. **Commit 2 (Pylint Fixes)**: `fix(quality): resolve mutable default arguments, naming, docstrings, and Pylint code smells (10.00/10)`
   - Fixed mutable default argument `booking_log=[]` (`W0102`) using sentinel `None` pattern.
   - Refactored function name `bookRoom` to PEP 8 snake_case `book_room` (`C0103`).
   - Added comprehensive PEP 257 docstrings to all functions and module (`C0116`).
   - Eliminated resource leaks using `with open(..., encoding="utf-8")` (`R1732`, `W1514`).
   - Fixed singleton comparison to `is None` (`C0121`).
   - Simplified redundant boolean returns (`R1703`, `R1705`).
   - Removed dead import `math` and dead local variable `cleaning_deposit`.

3. **Commit 3 (Flake8 Style & Deliverables)**: `style(pep8): enforce Flake8 compliance, add analysis reports, issues table, and reflection`
   - Enforced maximum line length $\le 79$ characters across the codebase (`E501`).
   - Ensured POSIX compliant trailing newline (`W292`, `C0304`).
   - Generated final static analysis reports: `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`.
   - Compiled `issues.md` and `reflection.md`.

---

## 🚀 How to Run and Verify

```bash
# 1. Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install analysis tools
pip install pylint bandit flake8

# 3. Run the application
python hotel_booking_system.py

# 4. Generate/verify static analysis reports
pylint hotel_booking_system.py > pylint_report.txt
bandit -r hotel_booking_system.py > bandit_report.txt
flake8 hotel_booking_system.py > flake8_report.txt
```
