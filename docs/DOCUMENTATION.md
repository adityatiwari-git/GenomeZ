
# GenomeZ Documentation

> Complete conceptual and practical documentation for the Genomics and Proteomics workspaces.

## 1. What is GenomeZ?

GenomeZ is a browser-based bioinformatics platform for working with nucleotide and protein sequences. It combines sequence-analysis algorithms, file handling, authentication, and selected external biological database searches in one interface.

The basic workflow is:

**Enter or upload a biological sequence → validate it → choose an analysis → inspect the result → export or continue working.**

GenomeZ combines:

- Bioinformatics
- Python
- Django
- HTML/CSS/Bootstrap
- Sequence-analysis algorithms
- External biological databases and services
- Authentication
- Cloud deployment

It is intended as a practical learning and analysis platform rather than a replacement for specialist research software.

---

# 2. Why are Genomics and Proteomics separated?

GenomeZ separates the platform into two workspaces because DNA/RNA and proteins are different biological sequence types and are analyzed with different concepts.

## Genomics

Genomics focuses on nucleic-acid sequences:

- DNA
- RNA
- Nucleotides
- Genes
- Coding regions
- Motifs
- Reading frames
- Nucleotide composition

Typical questions include:

- What is the GC content?
- Where does a motif occur?
- What is the complementary sequence?
- What RNA sequence corresponds to this DNA sequence?
- Does the sequence contain an open reading frame?
- What protein could a coding sequence translate into?
- What known sequences resemble this DNA?

## Proteomics

Proteomics focuses on proteins:

- Amino acids
- Protein sequences
- Molecular weight
- Amino-acid composition
- Hydrophobicity
- Protein identification
- Protein similarity searching

Typical questions include:

- How long is this protein?
- What is its approximate molecular weight?
- What fraction is hydrophobic?
- What amino acids are present?
- Does the exact sequence occur in UniProt?
- What similar proteins can be found with BLASTP?

### Why not put everything in one analyzer?

The input alphabets, biological meaning, algorithms, and external databases are different.

A nucleotide analyzer expects symbols such as A, T, G and C for DNA, or A, U, G and C for RNA.

A protein analyzer expects the standard amino-acid one-letter alphabet.

Keeping the workspaces separate makes the interface easier to understand and prevents nucleotide operations from being applied to protein sequences.

---

# 3. Sequence Types

## DNA

DNA, or deoxyribonucleic acid, stores genetic information.

GenomeZ represents DNA using:

| Symbol | Base |
|---|---|
| A | Adenine |
| T | Thymine |
| G | Guanine |
| C | Cytosine |

Example:

    ATGCGTACCGTA

## RNA

RNA, or ribonucleic acid, uses U instead of T.

| Symbol | Base |
|---|---|
| A | Adenine |
| U | Uracil |
| G | Guanine |
| C | Cytosine |

Example:

    AUGCGUACCGUA

GenomeZ distinguishes DNA and RNA by the nucleotide alphabet and rejects sequences that contain both T and U.

## Protein

Proteins are chains of amino acids represented by one-letter symbols.

Example:

    MKWVTFISLLLLFSSAYSRGVFRRDTHKSEIAHRFKDLGE

Protein analysis belongs to the Proteomics workspace.

---

# 4. Input and Validation

GenomeZ accepts sequences in two main ways:

1. Paste a sequence into the input box.
2. Upload a FASTA or TXT file.

For nucleotide sequences, GenomeZ:

- Removes whitespace
- Converts input to uppercase
- Checks for unsupported characters
- Rejects mixed T/U input
- Determines DNA or RNA
- Calculates sequence length
- Calculates nucleotide counts
- Calculates GC percentage
- Calculates AT percentage for DNA or AU percentage for RNA

Validation is important because the analysis functions expect valid nucleotide input.

---

# 5. FASTA Files

FASTA is a common text format for biological sequences.

Example:

~~~text
>sample_sequence
ATGCGTACCGTAGCTAGC
~~~

The line beginning with > is the sequence identifier/header. The following lines contain the sequence.

GenomeZ can load FASTA/TXT input and clean the sequence before analysis.

FASTA is especially useful when sequences come from biological databases.

---

# 6. Genomics Workspace

The Genomics analyzer currently provides:

1. DNA → RNA
2. RNA → DNA
3. GC Content
4. Base Count
5. Complement
6. Reverse Complement
7. Protein Translation
8. Motif Finder
9. ORF Finder
10. Sequence Identification using NCBI BLASTN

The first nine are free analysis tools. Sequence Identification is protected behind authentication.

---

# 7. DNA → RNA

## What does it do?

This tool converts a DNA sequence into an RNA representation by replacing T with U.

Example:

~~~text
DNA
ATGCCGTA

RNA
AUGCCGUA
~~~

## Biological purpose

DNA and RNA use different nucleotide alphabets. During transcription, RNA uses U where DNA uses T.

This tool performs the sequence-level conversion.

## Important limitation

It does not simulate the complete biological transcription process, including promoter recognition, RNA polymerase activity, RNA processing, splicing, or regulation.

---

# 8. RNA → DNA

## What does it do?

This performs the reverse alphabet conversion:

U → T

Example:

~~~text
RNA
AUGCCGUA

DNA
ATGCCGTA
~~~

It is useful when RNA notation needs to be converted to DNA notation for another sequence operation.

This is a sequence conversion, not a simulation of biological reverse transcription.

---

# 9. GC Content

## What is GC content?

GC content is the percentage of nucleotides that are G or C.

Formula:

    GC% = ((G + C) / sequence length) × 100

Example:

For:

    ATGCGC

G = 2  
C = 2  
Length = 6

Therefore:

    GC% = (4 / 6) × 100 = 66.67%

## Why is it useful?

GC content is a basic sequence statistic useful for:

- Comparing nucleotide sequences
- Describing sequence composition
- Studying regions with different nucleotide characteristics
- Introductory genomic analysis

GC content alone does not identify a gene or determine biological function.

---

# 10. Base Count / Nucleotide Composition

The Base Count tool counts individual nucleotides.

For DNA:

- A
- T
- G
- C

For RNA:

- A
- U
- G
- C

Example:

    AATGCC

Results:

- A = 2
- T = 1
- G = 1
- C = 2

Base composition provides a quick description of a sequence and forms the basis of statistics such as GC content.

---

# 11. Complement

## What is a complementary sequence?

DNA base-pairing rules are:

| Base | Complement |
|---|---|
| A | T |
| T | A |
| G | C |
| C | G |

RNA uses U:

| Base | Complement |
|---|---|
| A | U |
| U | A |
| G | C |
| C | G |

Example:

~~~text
Original
ATGC

Complement
TACG
~~~

The complement tool changes each nucleotide to its paired base without reversing the sequence.

## Why is it useful?

Complementary sequences are fundamental to:

- Double-stranded DNA
- Base pairing
- Primer/oligonucleotide relationships
- Sequence orientation

---

# 12. Reverse Complement

The reverse complement performs two operations:

1. Generate the complement.
2. Reverse the resulting sequence.

Example:

~~~text
Original
ATGC

Complement
TACG

Reverse Complement
GCAT
~~~

## Why is it useful?

Reverse-complement representation is common in:

- Strand-aware sequence analysis
- Primer design
- Motif analysis
- Genome sequence processing

The reverse complement is different from the complement because the nucleotide order is reversed.

---

# 13. Protein Translation

## What is translation?

Translation converts a nucleotide coding sequence into an amino-acid sequence using the genetic code.

Three nucleotides form one codon.

Example:

~~~text
DNA: ATG GCT TTT
RNA: AUG GCU UUU
         ↓   ↓   ↓
         M   A   F
~~~

Protein:

    MAF

## How GenomeZ performs translation

The current workflow:

1. Accept DNA or RNA.
2. Convert DNA notation to RNA notation when required.
3. Search for the first supported start codon.
4. Start translation from that position.
5. Read the sequence in groups of three.
6. Translate codons into amino acids.
7. Stop at the first supported stop codon.

The result also reports related codon/start/stop information.

## Start codon

Standard start codon:

    AUG

For DNA:

    ATG

## Stop codons

RNA:

- UAA
- UAG
- UGA

DNA:

- TAA
- TAG
- TGA

## Why is translation useful?

It connects nucleotide analysis to protein analysis and is useful for:

- Learning the genetic code
- Inspecting coding sequences
- Checking candidate ORFs
- Understanding the relationship between genomics and proteomics

## Limitation

A translated sequence does not prove that a gene is expressed or that the resulting protein exists in an organism.

---

# 14. Motif Finder

## What is a motif?

A sequence motif is a short recurring pattern in a biological sequence.

A motif may represent a region of biological interest, such as a binding or regulatory pattern.

GenomeZ allows a user to provide a motif and search for occurrences in the sequence.

## What does it report?

The tool reports:

- Requested motif
- Number of matches
- Match positions

Example:

~~~text
Sequence
ATGCGATGAAATG

Motif
ATG
~~~

The tool reports the occurrences found by its sequence search.

## Why is motif finding useful?

Motif searches are useful for:

- Sequence inspection
- Finding repeated patterns
- Educational exercises
- Preliminary regulatory/coding sequence exploration

## Limitation

Finding a motif does not automatically establish biological function. Short sequences can occur by chance.

---

# 15. ORF Finder

## What is an ORF?

ORF means **Open Reading Frame**.

An ORF is a stretch of nucleotide sequence that can be read as codons in a particular reading frame, generally beginning with a start codon and ending at a stop codon.

Example:

~~~text
ATG | XXX | XXX | XXX | TAA
 ^                         ^
 start                     stop
~~~

## Why are reading frames important?

A nucleotide sequence can be divided into codons using different offsets.

For one strand there are three possible reading frames:

- Frame 1
- Frame 2
- Frame 3

The opposite strand can also be considered through its reverse complement.

## What GenomeZ does

The current ORF implementation scans supported reading frames and looks for start codons and appropriate stop codons.

The result reports:

- Frame
- Start position
- End position
- ORF length
- ORF sequence

## Why is ORF finding useful?

ORF detection is useful as an initial computational step when looking for possible protein-coding regions.

It can help with:

- Gene-sequence exercises
- Coding-region exploration
- Preparing candidate sequences for translation
- Introductory genome analysis

## Important limitation

An ORF is a computational sequence pattern, not proof that a functional gene exists.

Real gene annotation normally requires additional evidence such as homology, genomic context, expression evidence, and organism-specific annotation.

---

# 16. Sequence Identification with NCBI BLASTN

## What is sequence identification?

Sequence identification asks:

**What known biological sequences are similar to this sequence?**

GenomeZ provides this as its protected Sequence Identification feature.

The implementation uses **NCBI BLASTN**.

## What is BLAST?

BLAST stands for **Basic Local Alignment Search Tool**.

BLAST searches for regions of similarity between a query sequence and sequences in a database.

Similarity can provide clues about:

- Possible identity
- Evolutionary relationships
- Conserved regions
- Related sequences

## GenomeZ workflow

~~~text
DNA sequence
      ↓
NCBI BLASTN
      ↓
nt database
      ↓
RID
      ↓
Short polling cycle
      ↓
BLAST XML
      ↓
GenomeZ parses results
~~~

The current integration uses:

- Program: blastn
- Database: nt
- Result format: XML

The parser extracts information from returned BLAST XML, including top-hit information such as accession/title and reported alignment statistics where available.

## Why is it protected?

Sequence identification depends on an external biological database and network service. GenomeZ keeps common sequence calculations public while placing the database-backed workflow behind authentication.

## Limitation

The current implementation uses a short synchronous polling cycle. If NCBI has not completed the job within that window, GenomeZ can report that the job is still processing.

A future version could use background processing and persistent BLAST job state.

---

# 17. Free vs Authenticated Genomics Tools

| Tool | Guest | Logged in |
|---|---:|---:|
| DNA → RNA | Yes | Yes |
| RNA → DNA | Yes | Yes |
| GC Content | Yes | Yes |
| Base Count | Yes | Yes |
| Complement | Yes | Yes |
| Reverse Complement | Yes | Yes |
| Translation | Yes | Yes |
| Motif Finder | Yes | Yes |
| ORF Finder | Yes | Yes |
| Sequence Identification / BLASTN | No | Yes |

There is currently **no paid subscription system**.

Authentication uses Django's built-in user system.

---

# 18. Proteomics Workspace

The Proteomics workspace accepts protein sequences rather than DNA/RNA.

Current functions include:

- Protein sequence validation
- FASTA/TXT upload
- Sequence cleaning
- Protein length
- Average molecular weight
- Hydrophobic-residue percentage
- Amino-acid composition
- Exact-sequence UniProt search
- UniProt result links
- NCBI BLASTP launch

---

# 19. Protein Sequence Validation

A protein sequence uses amino-acid symbols rather than nucleotide symbols.

The Proteomics workflow cleans the input and checks that it contains standard amino-acid symbols supported by the application.

A protein sequence should not be sent through DNA-specific tools such as GC Content or Reverse Complement.

This is another reason for keeping the two workspaces separate.

---

# 20. Protein Length

Protein length is the number of amino-acid residues in the sequence.

Example:

    MKWV

Length:

    4 amino acids

Protein length is a basic property used in many downstream analyses.

---

# 21. Average Molecular Weight

GenomeZ calculates an approximate sequence-derived average molecular weight from the amino-acid composition.

It is an estimated property based on the supplied sequence.

It should not be interpreted as an experimental mass measurement.

---

# 22. Hydrophobic Percentage

Hydrophobic amino acids tend to have non-polar side chains.

GenomeZ calculates the percentage of residues belonging to its implemented hydrophobic residue set:

    A, I, L, M, F, W, Y, V

## Why is hydrophobicity useful?

Hydrophobicity is important in protein biology because hydrophobic residues can contribute to:

- Protein folding
- Internal hydrophobic cores
- Membrane-associated regions
- Interactions with non-polar environments

The GenomeZ value is a simple composition-based percentage, not a full hydropathy-profile prediction.

---

# 23. Amino-Acid Composition

The composition tool counts amino acids in the protein sequence.

Example:

~~~text
Sequence: MAAK

A = 2
M = 1
K = 1
~~~

## Why is composition useful?

Composition gives a basic description of a protein and can help compare sequences or inspect unusual amino-acid distributions.

---

# 24. UniProt Exact-Sequence Search

## What is UniProt?

UniProt is a major biological resource for protein sequence and annotation information.

GenomeZ can use UniProt for an exact-sequence search.

The purpose is different from a broad similarity search.

An exact-sequence lookup asks whether the supplied protein sequence matches a sequence represented in the UniProt resource.

## Why is this useful?

It can provide a starting point for connecting a protein sequence with an existing biological record.

## Limitation

An exact-sequence lookup is not the same as a full similarity search or complete functional annotation.

---

# 25. NCBI BLASTP

## What is BLASTP?

BLASTP searches a protein query against protein sequence databases to find similar sequences.

It is the protein counterpart to nucleotide BLAST workflows such as BLASTN.

GenomeZ currently provides a direct NCBI BLASTP launch from the Proteomics workspace rather than rendering the complete BLASTP result internally.

---

# 26. Genomics vs Proteomics Tool Map

| Biological question | Workspace | Tool |
|---|---|---|
| Convert DNA to RNA | Genomics | DNA → RNA |
| Convert RNA to DNA notation | Genomics | RNA → DNA |
| Measure GC percentage | Genomics | GC Content |
| Count nucleotides | Genomics | Base Count |
| Find complementary strand | Genomics | Complement |
| Find reverse complement | Genomics | Reverse Complement |
| Convert coding sequence to protein | Genomics | Translation |
| Find short nucleotide patterns | Genomics | Motif Finder |
| Find candidate coding regions | Genomics | ORF Finder |
| Identify similar DNA sequences | Genomics | NCBI BLASTN |
| Calculate protein length | Proteomics | Protein analysis |
| Estimate sequence-derived molecular weight | Proteomics | Protein analysis |
| Calculate hydrophobic percentage | Proteomics | Protein analysis |
| Count amino acids | Proteomics | Composition |
| Find exact protein sequence records | Proteomics | UniProt |
| Search similar protein sequences | Proteomics | NCBI BLASTP |

---

# 27. Local Algorithms vs External Resources

GenomeZ contains two broad categories of analysis.

## Local computation

Performed directly by the application:

- Nucleotide validation
- Nucleotide counting
- GC content
- DNA/RNA conversion
- Complement
- Reverse complement
- Translation
- Motif search
- ORF search
- Protein composition
- Protein length
- Sequence-derived molecular-weight calculation
- Hydrophobic percentage

## External biological resources

These workflows depend on external services:

- NCBI BLASTN
- NCBI BLASTP
- UniProt

External workflows depend on network connectivity, provider availability, response time, database contents, and provider policies.

---

# 28. General Analysis Workflow

Genomics:

~~~text
Sequence input
      ↓
Clean / parse
      ↓
Validate
      ↓
Determine DNA or RNA
      ↓
Select tool
      ↓
Authentication check when required
      ↓
Run analysis
      ↓
Generate structured result
      ↓
Display result
      ↓
Copy / export
~~~

Proteomics:

~~~text
Protein input
      ↓
Clean / parse
      ↓
Validate amino acids
      ↓
Calculate sequence properties
      ↓
Optional external search
      ↓
Display results
~~~

---

# 29. Reports and Exports

GenomeZ supports working with analysis results through its result/export workflow.

Sequence-type results can be represented as FASTA.

Textual analysis results can be exported as TXT.

The interface also provides copy/download controls.

The exact active export options should always be checked against the current deployed version.

---

# 30. Sample Sequences

The repository contains sample sequence files for testing:

- sample.fasta
- sample_rna.fasta
- sample_protein.fasta

These allow the Genomics and Proteomics workflows to be tested without preparing an input sequence manually.

---

# 31. Application Architecture

GenomeZ follows a conventional Django structure.

### accounts/

Handles:

- Signup
- Login
- Logout
- Authentication-related URLs and views

### analyzer/

Handles the Genomics workspace.

Important areas include:

- Request handling
- Validation
- Analysis services
- Individual analysis modules
- Reports
- FASTA generation

### analyzer/analysis/

Contains individual sequence-analysis algorithms, including:

- gc_content.py
- atgc_count.py
- translation.py
- motif.py
- orf.py
- identification.py
- file_parser.py

### proteomics/

Handles protein sequence analysis and protein-related external resources.

### core/

Handles the public website/home experience.

### genomez/

Contains Django project configuration, settings, WSGI/ASGI configuration, and top-level routing.

### templates/

Contains the HTML interface.

### static/

Contains CSS, images, videos, and other static assets.

---

# 32. Why GenomeZ Uses Django

Django provides:

- URL routing
- Request/response handling
- Authentication
- Sessions
- Database support
- Templates
- Security features
- Deployment-friendly project structure

This allows GenomeZ to combine a scientific analysis backend with a browser-based interface.

---

# 33. Authentication Architecture

## Guest

Guests can:

- Open the homepage
- Open the Genomics Analyzer
- Run free nucleotide tools
- Use supported sequence input/export functionality

A guest attempting the protected Sequence Identification feature is redirected to authentication.

## Logged in

Authenticated users can use the free tools plus the currently protected Sequence Identification workflow.

There is no payment gateway or subscription tier.

---

# 34. Biological Interpretation

GenomeZ performs sequence-level analysis.

Examples:

- GC content is a composition statistic.
- An ORF is a computationally detected coding pattern.
- A motif is a sequence pattern.
- A BLAST hit is a sequence-similarity relationship.
- Molecular weight is a sequence-derived estimate.
- Hydrophobic percentage is a composition statistic.

These outputs should not automatically be treated as definitive biological conclusions.

For research use, computational results normally need to be considered together with sequence quality, organism/context, database annotations, alignment quality, statistical significance, literature, and experimental evidence.

---

# 35. Important Limitations

## BLASTN

The current GenomeZ implementation uses a short synchronous polling cycle.

A BLAST request may still be processing when GenomeZ stops polling.

## BLASTP

The current Proteomics workflow launches NCBI BLASTP externally rather than rendering the complete result inside GenomeZ.

## UniProt

UniProt results depend on the external service and its current database contents.

## ORF Finder

An ORF is not automatically a confirmed gene.

## Motif Finder

A motif occurrence does not automatically establish biological function.

## Translation

A translated sequence does not automatically establish protein expression.

## Protein properties

Calculated protein properties are sequence-derived estimates, not experimental measurements.

---

# 36. Example End-to-End Genomics Exercise

Input:

    ATGAAAGGCTAA

A learning workflow can be:

### Step 1 — Validation

GenomeZ identifies the sequence as DNA.

### Step 2 — Base Count

The application counts A, T, G and C.

### Step 3 — GC Content

The application calculates the percentage of G and C.

### Step 4 — Complement

GenomeZ produces the complementary DNA strand.

### Step 5 — Reverse Complement

GenomeZ reverses the complementary sequence.

### Step 6 — Translation

The sequence can be interpreted as a coding sequence and translated from the supported start codon until a stop codon is encountered.

### Step 7 — ORF Finder

The sequence can be inspected for an open reading frame.

### Step 8 — Motif Finder

A user can search for a short nucleotide pattern.

### Step 9 — Sequence Identification

An authenticated user can submit the DNA sequence to NCBI BLASTN through GenomeZ.

---

# 37. Example Proteomics Exercise

Suppose the input is:

    MKWVTFISLL

GenomeZ can:

1. Validate the amino-acid sequence.
2. Calculate its length.
3. Calculate amino-acid composition.
4. Estimate average molecular weight.
5. Calculate hydrophobic-residue percentage.
6. Search for an exact sequence through UniProt.
7. Provide a route to NCBI BLASTP.

This demonstrates the difference between sequence properties and database-backed identification/search.

---

# 38. Intended Users

GenomeZ is particularly useful for:

- Bioinformatics students
- Biology students learning sequence analysis
- Educators demonstrating sequence concepts
- Beginners learning Python/Django through a scientific project
- Researchers performing quick preliminary sequence checks

It is not intended to replace complete professional bioinformatics pipelines.

---

# 39. Quick Reference

## Genomics

**DNA/RNA in → nucleotide analysis out**

Tools:

- DNA → RNA
- RNA → DNA
- GC Content
- Base Count
- Complement
- Reverse Complement
- Translation
- Motif Finder
- ORF Finder
- BLASTN Sequence Identification

## Proteomics

**Protein sequence in → protein properties/search out**

Tools:

- Protein validation
- Length
- Molecular weight
- Hydrophobic percentage
- Amino-acid composition
- UniProt exact-sequence search
- NCBI BLASTP

---

# 40. Project Philosophy

GenomeZ is built around four principles:

### 1. Keep common analysis accessible

Basic sequence calculations should not require an account.

### 2. Separate biological domains

Nucleotide and protein workflows should have their own interfaces and logic.

### 3. Combine computation with biological databases

Local algorithms provide immediate sequence-level analysis, while NCBI and UniProt provide access to external biological resources.

### 4. Keep the architecture understandable

The project uses normal Django applications, views, services, templates, and focused analysis modules instead of unnecessary abstraction.

---

# 41. Summary

GenomeZ provides a practical bridge between biological sequence concepts and software engineering.

The **Genomics** workspace focuses on DNA/RNA operations such as:

- Composition
- GC content
- Strand operations
- DNA/RNA conversion
- Translation
- Motifs
- ORFs
- Nucleotide sequence identification

The **Proteomics** workspace focuses on protein-specific properties and resources such as:

- Amino-acid composition
- Molecular weight
- Hydrophobicity
- UniProt lookup
- BLASTP

The separation exists because nucleotide and protein sequences use different alphabets, biological concepts, algorithms, and search resources.

GenomeZ therefore provides a single platform while keeping the underlying biological workflows clearly separated.
