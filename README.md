# 🧬 GenomeZ

> A modern, full-stack bioinformatics web platform for practical **Genomics and Proteomics sequence analysis**.

GenomeZ is a Django-based web application that brings common bioinformatics workflows into a clean, browser-based interface. It separates **Genomics** and **Proteomics** into dedicated workspaces, keeps common analysis accessible to guests, and adds authenticated access for database-backed sequence identification.

---

## 🌐 Overview

GenomeZ is organized around two primary workspaces:

| Workspace | Purpose |
|---|---|
| 🧬 **Genomics** | DNA/RNA sequence analysis and sequence-oriented tools |
| 🧪 **Proteomics** | Protein sequence analysis, properties, composition, and identification |

The core access model is intentionally simple:

> **Common analysis is public. Database-backed sequence identification requires an account.**

---

## ✨ Features

### 🧬 Genomics

- DNA → RNA conversion
- RNA → DNA conversion
- GC content
- nucleotide/base composition
- complement
- reverse complement
- protein translation
- motif finder
- ORF finder
- DNA/RNA validation
- FASTA/TXT upload
- TXT report generation
- FASTA export for sequence outputs
- copy/download individual results
- full report download

### 🔎 Sequence Identification

Authenticated users can use **Sequence Identification**.

The current implementation:

1. accepts a DNA sequence,
2. submits it to **NCBI BLASTN**,
3. uses the NCBI **nt** database,
4. receives a BLAST request ID (RID),
5. polls for a short period,
6. parses returned BLAST XML,
7. reports the number of matches found.

> This feature is currently implemented as **NCBI BLASTN against nt**. It is not an "all databases" search.

### 🧪 Proteomics

The separate Proteomics workspace currently supports:

- protein sequence input
- FASTA/TXT upload
- amino-acid validation
- protein length
- average molecular weight
- hydrophobic-residue percentage
- amino-acid composition
- exact-sequence UniProt search
- UniProt result links
- direct NCBI BLASTP launch

### 👤 Authentication

GenomeZ uses Django's built-in authentication system.

- Guests can open the Analyzer.
- Guests can use free Genomics tools.
- Premium sequence identification requires login.
- Registration creates a normal Django user account.
- Logged-in users get all currently implemented premium functionality.
- There is no payment/subscription tier in the current implementation.
- Logout is supported.

### 📥 Input & Export

Inputs:

- pasted sequence
- FASTA
- TXT

Outputs:

- on-page results
- clipboard copy
- TXT
- FASTA for sequence-type results
- full TXT report

---

# 🏗️ Architecture

GenomeZ uses a conventional Django structure.

```text
GenomeZ
│
├── accounts/                 # Authentication
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── analyzer/                 # Genomics workspace
│   ├── analysis/
│   │   ├── dna_to_rna.py
│   │   ├── rna_to_dna.py
│   │   ├── gc_content.py
│   │   ├── atgc_count.py
│   │   ├── complement.py
│   │   ├── reverse_complement.py
│   │   ├── translation.py
│   │   ├── motif.py
│   │   ├── orf.py
│   │   ├── identification.py
│   │   └── file_parser.py
│   │
│   ├── services.py
│   ├── validators.py
│   ├── views.py
│   ├── report_generator.py
│   ├── fasta_generator.py
│   └── tests.py
│
├── proteomics/              # Proteomics workspace
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── ...
│
├── core/                    # Public website
│
├── genomez/                 # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base/
│   ├── accounts/
│   ├── analyzer/
│   └── proteomics/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── videos/
│
├── build.sh
├── render.yaml
├── requirements.txt
├── manage.py
└── sample.fasta
```

---

# 🔬 Genomics Workflow

```text
User Input
   │
   ├── Paste DNA/RNA
   │
   └── Upload FASTA/TXT
          │
          ▼
   Sequence Parser
          │
          ▼
   Sequence Validator
          │
          ├── Invalid → display error
          │
          ▼
   DNA / RNA Detection
          │
          ▼
   Select Analysis Tools
          │
          ├── Free tools
          │
          └── Premium tools
                  │
                  └── Authentication check
          │
          ▼
   Analysis Service Layer
          │
          ▼
   Structured Results
          │
          ├── View
          ├── Copy
          ├── TXT
          └── FASTA
```

---

# 🧬 DNA/RNA Detection

GenomeZ currently identifies nucleotide type from the submitted sequence.

### DNA

A valid sequence containing **T** and no **U** is treated as DNA.

```text
A T G C
```

### RNA

A valid sequence containing **U** and no **T** is treated as RNA.

```text
A U G C
```

### Validation

The validator:

- removes whitespace,
- converts input to uppercase,
- checks for unsupported characters,
- rejects mixed T/U input,
- calculates sequence length,
- calculates nucleotide counts,
- calculates GC percentage,
- calculates AT percentage for DNA or AU percentage for RNA.

---

# 🧪 Analysis Algorithms

## DNA → RNA

Example:

```text
DNA: ATGC
RNA: AUGC
```

## RNA → DNA

Example:

```text
RNA: AUGC
DNA: ATGC
```

## GC Content

```text
GC% = (G + C) / sequence_length × 100
```

The corresponding non-GC percentage is also reported.

## Base Composition

DNA:

```text
A
T
G
C
```

RNA:

```text
A
U
G
C
```

## Complement

GenomeZ generates a DNA- or RNA-specific complementary sequence.

## Reverse Complement

The complementary sequence is reversed to produce the reverse complement.

## Protein Translation

The translation workflow:

1. detects DNA/RNA input,
2. searches for the first supported start codon,
3. starts translation from that position,
4. translates in-frame,
5. stops at the first supported stop codon.

The output includes the translated protein and related codon/start/stop information.

## Motif Finder

Reports:

- requested motif
- number of matches
- match positions

## ORF Finder

Scans reading frames and reports:

- frame
- start
- end
- length
- sequence

---

# 🔎 NCBI BLASTN

The premium sequence-identification module lives at:

```text
analyzer/analysis/identification.py
```

Current flow:

```text
DNA sequence
    │
    ▼
NCBI BLAST
    │
    ├── PROGRAM = blastn
    ├── DATABASE = nt
    └── FORMAT_TYPE = XML
    │
    ▼
RID
    │
    ▼
Short polling cycle
    │
    ▼
BLAST XML
    │
    ▼
GenomeZ result message
```

The integration uses Python `requests`.

### Current limitation

The present implementation performs synchronous submission and a short polling cycle. A BLAST job that has not completed within that window is reported as still processing.

A larger production implementation could move this work to background processing and persist BLAST job state.

---

# 🧪 Proteomics Workflow

```text
Protein Input
   │
   ├── Paste sequence
   └── Upload FASTA/TXT
          │
          ▼
       Cleaning
          │
          ▼
   Amino-acid validation
          │
          ▼
   Protein analysis
          │
          ├── Length
          ├── Molecular weight
          ├── Hydrophobic %
          └── Composition
          │
          ├── UniProt exact-sequence search
          │
          └── NCBI BLASTP launch
```

The Proteomics workspace is intentionally separate from the nucleotide analyzer.

---

# 🌐 External Biological Resources

| Service | GenomeZ use |
|---|---|
| **NCBI BLASTN** | DNA sequence identification |
| **NCBI BLASTP** | External protein similarity search |
| **UniProt REST API** | Protein exact-sequence search |

GenomeZ's local algorithms and external database searches are distinct parts of the workflow.

---

# 👤 Authentication Model

### Guest

```text
Homepage
   │
   ▼
Analyzer
   │
   ├── Free tools → available
   │
   └── Sequence Identification
             │
             ▼
        Login / Register
```

### Logged in

```text
Login
  │
  ▼
Authenticated session
  │
  ├── Free tools
  └── Premium tools
```

Django's built-in `User` model is used for accounts and sessions.

---

# 🎨 User Interface

The public site includes:

- responsive navigation
- hero section
- feature section
- workflow section
- project overview
- contact section
- footer navigation
- workspace selection

The Genomics workspace includes:

- sequence input
- file upload
- tool selection
- sequence summary
- result cards
- copy/export controls

The design uses a clean scientific interface with blue/green visual accents.

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Backend | **Django 6.1.x** |
| Language | **Python** |
| Frontend | **HTML, CSS, Bootstrap, JavaScript** |
| Icons | **Bootstrap Icons** |
| Local DB | **SQLite** |
| Production DB | **PostgreSQL** |
| HTTP/API | **Requests** |
| DB configuration | **dj-database-url** |
| Static files | **WhiteNoise** |
| Production server | **Gunicorn** |
| Hosting | **Render** |
| Source control | **Git + GitHub** |

---

# 📦 Dependencies

```text
Django>=6.1,<6.2
requests>=2.32,<3
dj-database-url>=2.2,<3
psycopg2-binary>=2.9,<3
whitenoise>=6.9,<7
gunicorn>=23,<24
```

---

# 🚀 Local Development

## Clone

```bash
git clone https://github.com/adityatiwari-git/GenomeZ.git
cd GenomeZ
```

## Create virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the interpreter directly:

```powershell
.\.venv\Scripts\python.exe
```

## Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Migrate

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

## Run

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🔐 Environment Configuration

GenomeZ supports environment-based production configuration.

Key settings include:

```text
SECRET_KEY
DEBUG
ALLOWED_HOSTS
DATABASE_URL
CSRF_TRUSTED_ORIGINS
```

Local development falls back to SQLite when `DATABASE_URL` is not defined.

---

# ☁️ Deployment

The repository contains Render deployment configuration through:

```text
render.yaml
build.sh
requirements.txt
```

### Build process

```text
Install dependencies
        │
        ▼
Collect static files
        │
        ▼
Run migrations
        │
        ▼
Start Gunicorn
```

The Render configuration provisions:

- Python web service
- PostgreSQL database
- generated secret key
- `DEBUG=False`
- `DATABASE_URL`

---

# 🗃️ Data & Sessions

### Accounts

Django authentication tables store user account data.

### Local development

SQLite is used as the database fallback.

### Production

PostgreSQL is configured through `DATABASE_URL`.

### Analysis sessions

The Analyzer stores the latest sequence, sequence type, and generated results in the Django session to support report/export actions.

---

# 🧪 Testing

The project contains Django tests for the main application areas.

Genomics tests cover:

- DNA validation
- RNA validation
- invalid input
- DNA/RNA conversion
- GC content
- base counting
- complement
- reverse complement
- translation
- motif finder
- ORF finder
- public analyzer access
- guest use of free tools
- premium authentication gating

Authentication tests cover:

- signup
- login
- logout

Proteomics tests cover its implemented protein-analysis workflows.

Run:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

---

# 🔒 Access Matrix

| Capability | Guest | Logged in |
|---|:---:|:---:|
| Homepage | ✅ | ✅ |
| Genomics Analyzer | ✅ | ✅ |
| DNA/RNA tools | ✅ | ✅ |
| Sequence upload | ✅ | ✅ |
| Result export | ✅ | ✅ |
| Sequence Identification | ❌ | ✅ |
| Account management | ❌ | ✅ |

Premium access is enforced by the backend as well as reflected in the UI.

---

# 📁 Important Files

| File | Responsibility |
|---|---|
| `genomez/settings.py` | Django configuration |
| `genomez/urls.py` | URL routing |
| `analyzer/views.py` | Genomics request flow |
| `analyzer/services.py` | Analysis orchestration |
| `analyzer/validators.py` | DNA/RNA validation |
| `analyzer/analysis/` | Individual analysis algorithms |
| `analyzer/analysis/identification.py` | NCBI BLASTN integration |
| `proteomics/views.py` | Protein analysis + external services |
| `accounts/views.py` | Authentication |
| `templates/analyzer/analyzer.html` | Genomics UI |
| `templates/proteomics/proteomics.html` | Proteomics UI |
| `templates/base/home.html` | Public homepage |
| `static/css/style.css` | Public-site styles |
| `static/css/analyzer.css` | Workspace/auth styles |
| `requirements.txt` | Python dependencies |
| `build.sh` | Render build process |
| `render.yaml` | Render infrastructure |

---

# 🧭 Roadmap

Potential next steps include:

### Genomics
- asynchronous BLAST processing
- persistent BLAST job state
- richer BLAST result cards
- sequence history
- additional sequence statistics
- visualization
- multi-sequence comparison
- annotation workflows

### Proteomics
- richer similarity-search presentation
- feature and annotation views
- domain-oriented workflows
- expanded UniProt handling
- additional protein properties

### Platform
- user dashboards
- saved analyses
- project/workspace management
- API endpoints
- administrative workflows
- background task processing
- improved monitoring/logging

---

# 🧠 Design Principles

### Separation of domains

Genomics and Proteomics use separate workspaces and application logic.

### Public-first analysis

Common analysis remains usable without registration.

### Authenticated external search

Database-backed sequence identification is protected behind authentication.

### Local computation vs external knowledge

Deterministic calculations are performed by GenomeZ's own modules. Identification/search workflows rely on external resources such as NCBI and UniProt.

### Simple Django architecture

The project favors normal Django apps, views, templates, services, and analysis modules without unnecessary abstraction.

---

# ⚠️ Current Limitations

GenomeZ is still an evolving project.

- BLASTN polling is currently synchronous and short-lived.
- External API workflows depend on network availability and provider response times.
- Protein BLAST is currently launched through the external NCBI BLASTP interface rather than fully rendered inside GenomeZ.
- TXT/FASTA are the active export paths; PDF generation is not currently the primary active report workflow.
- Sequence identification represents database similarity searching, not a guaranteed biological diagnosis or definitive annotation.
- There is no payment/subscription system.
- No open-source license is currently declared.

---

# 🤝 Contributing

A typical development workflow is:

```text
Create / update branch
       │
       ▼
Implement feature
       │
       ▼
Run tests
       │
       ▼
Commit
       │
       ▼
Open Pull Request
```

Before submitting changes:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

---

# 📜 License

No open-source license is currently declared in this repository.

Until a license is added, the code should be treated as **all rights reserved** rather than assuming permission to reuse, modify, or redistribute it.

---

# 👨‍💻 Author

**Aditya Tiwari**

GenomeZ is a practical bioinformatics engineering project combining:

- Bioinformatics
- Python
- Django
- Web development
- API integration
- Database systems
- Scientific computing
- Cloud deployment

---

# 🔗 Links

- **Repository:** https://github.com/adityatiwari-git/GenomeZ
- **NCBI BLAST:** https://blast.ncbi.nlm.nih.gov/
- **UniProt:** https://www.uniprot.org/
- **Deployment:** Render

---

## ⭐ GenomeZ

**Analyze sequences. Explore biology. Build better workflows.**
