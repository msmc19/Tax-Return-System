# Tax‑Return Management System

> **Purpose**: CLI application that streamlines preparation and tracking of U.S. tax returns for an accounting firm.  
> **Stack**: Python 3 · PostgreSQL · psycopg2 (connection pooling)  
> **Domain Objects**: CPAs · Clients · Tax‑Filing Assistants · Tax Returns  

---

## 📌 Project Overview
Accountants juggle many clients, deadlines, and compliance steps.  
This project delivers a **menu‑driven back‑office tool** that:

* Persists data in a **normalized PostgreSQL schema** (see *Database Design*).  
* Uses a **connection‑pool layer** for efficient, thread‑safe queries.  
* Implements full **CRUD** via OOP models (`CPA`, `Client`, `TaxFilingAssistant`, `TaxReturn`).  
* Enforces business rules—e.g., *one tax return per client*—at both database and application layers.  
* Provides clear **error handling** and transaction rollback for reliability.  

---

## 🗺️ Repository Layout
tax‑return‑system/
├── db_connection.py             # connection pool (psycopg2)
├── database.py                  # SQL helpers + table creation + core CRUD
├── models/
│   ├── cpa.py
│   ├── client.py
│   ├── tax_filing_assistant.py
│   └── tax_return.py
├── main.py                      # CLI controller (menu interface)
├── docs/
│   ├── Tax Return System ‑ Software_Design.txt
│   └── Tax Return System ‑ Database_Design.txt
├── requirements.txt
└── README.md   ← you are here

### 🗄️ Database Design (summary)

| Table | Key Fields | Relationships |
|-------|------------|---------------|
| **CPAs** | `cpa_id` PK · `name` | — |
| **Clients** | `client_id` PK · **FK** `cpa_id` | many‑to‑1 → CPAs |
| **TaxFilingAssistants** | `assistant_id` PK · `name` | — |
| **TaxReturns** | `return_id` PK · **UNIQUE** `client_id` FK | 1‑to‑1 with Clients |

*Normalization & foreign keys guarantee data integrity; sequences are reset after deletions to keep IDs compact.*

---

### ⚙️ Environment Setup

#### Prerequisites
* Python 3.9+  
* PostgreSQL 14+ (local or cloud)  
* A database user with **CREATE** privileges  

#### Steps
# 1 – Clone repo
git clone https://github.com/<your‑org>/tax-return-system.git
cd tax-return-system

# 2 – Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt   # psycopg2‑binary, tabulate (optional)

# 3 – Configure DB URI
export DATABASE_URI="postgresql://user:password@localhost:5432/taxdb"
#   or place it in .env and tweak db_connection.py to read from os.getenv

# 4 – Initialize tables & launch CLI
python main.py

### 🔑 CLI Usage
*The program launches a numbered menu; navigate with digits + Enter.*

| Main Menu              | Sub‑actions                                                                        |
|------------------------|------------------------------------------------------------------------------------|
| **Manage CPAs**        | add · view · rename · delete                                                       |
| **Manage Clients**     | add · view · update (name / address / income / cpa) · delete                       |
| **Manage Assistants**  | add · view · rename · delete                                                       |
| **Manage Tax Returns** | add (enforces 1‑per‑client) · view · mark filed · mark checked by CPA · mark filed by assistant |

*All actions print success/failure messages; invalid IDs or duplicate returns raise friendly errors.*

---

### 📈 Features & Design Highlights
* **Connection Pooling** – `db_connection.py` maintains a `SimpleConnectionPool(1, 10)` for low‑latency reuse.  
* **Atomic Queries** – `execute_query()` commits on success, rolls back and logs on exceptions.  
* **Model Encapsulation** – Business logic lives in model classes; the controller just calls methods.  
* **Sequence Reset** – Deletions invoke `reset_sequence()` to keep SERIAL counters contiguous—handy for demos.  
* **Extensible Layering** – New entities (e.g., *Invoices*) drop into the same pattern without touching the controller.  

---

### 🛣️ Project Roadmap
1. **Unit Tests** – pytest coverage for model CRUD & edge cases  
2. **Role‑Based Auth** – restrict menus by staff role (CPA vs. assistant)  
3. **CSV/Excel Import** – bulk‑load clients from spreadsheet  
4. **Web UI** – Flask or FastAPI front‑end to replace CLI  
5. **Docker Compose** – containerize app + Postgres for one‑command startup  

---

### 🤝 Contributing
Pull requests are welcome! Please create an issue first if you plan a large change (e.g., schema migration or UI overhaul).
