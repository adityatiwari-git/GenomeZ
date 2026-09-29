# GenomeZ Documentation

## 1. What is GenomeZ?

GenomeZ is a web-based bioinformatics platform for working with biological sequences.

It is divided into two main workspaces:

- **Genomics** — DNA and RNA sequence analysis
- **Proteomics** — protein sequence analysis

The purpose of the platform is to bring common sequence-analysis tasks into one simple browser interface so that a user can paste a sequence, upload a FASTA/TXT file, choose the required tools, and view or export the results.

GenomeZ combines:

- local sequence-processing algorithms,
- biological sequence validation,
- database-backed identification/search,
- external biological resources,
- authentication,
- result export,
- and a web interface.

---

# 2. Why are Genomics and Proteomics separated?

DNA/RNA and proteins are different biological sequence types and are normally studied with different kinds of analysis.

### Genomics

Genomics deals primarily with **DNA and RNA**.

Typical questions include:

- What bases are present?
- What is the GC content?
- What is the complementary sequence?
- What RNA sequence can be produced from DNA?
- Where is a particular motif located?
- Are there possible open reading frames?
- What protein could a nucleotide sequence encode?
- What biological sequence is this DNA most similar to?

GenomeZ therefore places nucleotide-oriented tools in the **Genomics Analyzer**.

### Proteomics

Proteomics deals with **proteins and their amino-acid sequences**.

Typical questions include:

- How long is the protein?
- What is its approximate molecular weight?
- What is its amino-acid composition?
- How hydrophobic is the sequence?
- Does an exact sequence exist in UniProt?
- What protein-similarity search can be performed?

GenomeZ therefore provides a separate **Proteomics workspace**.

### Why not put everything into one analyzer?

A single analyzer could technically accept all sequence types, but separating the workspaces makes the workflow clearer.

The separation also prevents users from accidentally applying nucleotide-specific operations to protein sequences.

For example:

- GC content is meaningful for nucleotide sequences.
- DNA complement uses A/T/G/C pairing.
- Protein sequences use amino-acid symbols rather than nucleotide bases.
- Protein molecular weight is calculated from amino-acid residues.
- BLASTN and BLASTP are different search programs for different sequence types.

The separation is therefore both a **biological distinction** and a **software-design decision**.

---

# 3. GenomeZ Genomics Analyzer

The Genomics Analyzer accepts:

- pasted DNA sequences,
- pasted RNA sequences,
- FASTA files,
- TXT files.

The normal workflow is:

1. Enter or upload a sequence.
2. GenomeZ cleans the input.
3. GenomeZ validates the sequence.
4. The sequence is classified as DNA or RNA.
5. Select one or more analysis tools.
6. GenomeZ runs the selected algorithms.
7. Results are displayed as individual result cards.
8. Results can be copied or downloaded where supported.

---

# 4. DNA and RNA Validation

Before analysis, GenomeZ validates nucleotide input.

## Supported DNA bases

DNA uses:

- A — Adenine
- T — Thymine
- G — Guanine
- C — Cytosine

Example:

```
ATGCGTACG
```

## Supported RNA bases

RNA uses:

- A — Adenine
- U — Uracil
- G — Guanine
- C — Cytosine

Example:

```
AUGCGUACG
```

## Input cleaning

GenomeZ:

1. converts the sequence to uppercase,
2. removes whitespace,
3. checks every character,
4. rejects unsupported characters.

## Mixed DNA/RNA sequences

A sequence containing both **T** and **U** is rejected.

Example:

```
ATGCUA
```

This is treated as ambiguous because GenomeZ cannot safely classify it as standard DNA or standard RNA.

## Sequence type detection

- Presence of T without U → DNA
- Presence of U without T → RNA

The validator also calculates:

- sequence length,
- base counts,
- GC percentage,
- AT percentage for DNA,
- AU percentage for RNA.

---

# 5. Genomics Tools

## 5.1 DNA → RNA

### What does it do?

This tool converts a DNA sequence into an RNA-form sequence by replacing:

```
T → U
```

Example:

```
DNA: ATGCGT
RNA: AUGCGU
```

### Why is it useful?

RNA uses uracil (U) instead of thymine (T). Converting a nucleotide sequence into RNA notation is useful before RNA-oriented operations such as translation.

### Important note

This tool performs a sequence representation conversion. It does not simulate the complete biological process of transcription with promoter recognition, RNA processing, or regulation.

---

## 5.2 RNA → DNA

### What does it do?

This tool converts an RNA sequence into DNA-style notation:

```
U → T
```

Example:

```
RNA: AUGCGU
DNA: ATGCGT
```

### Why is it useful?

It is useful when a user needs to move between RNA and DNA sequence representations.

---

## 5.3 GC Content

### What is GC content?

GC content is the proportion of guanine (G) and cytosine (C) bases in a nucleotide sequence.

GenomeZ calculates:

```
GC% = (G + C) / sequence length × 100
```

Example:

For:

```
ATGCGC
```

there are 4 G/C bases out of 6:

```
GC% = 4/6 × 100 = 66.67%
```

### Why is GC content useful?

GC content is a basic sequence-composition statistic.

It can be useful for:

- comparing sequences,
- examining nucleotide composition,
- checking synthetic or experimental sequences,
- basic genome/region characterization.

### Important limitation

GC content alone does not identify a gene, organism, or biological function.

---

## 5.4 Base Count / Nucleotide Composition

### What does it do?

The Base Count tool counts the individual nucleotides.

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

```
ATGCGT
```

Result:

```
A: 1
T: 2
G: 1
C: 2
```

### Why is it useful?

It provides a direct view of the sequence composition and is useful when checking sequence statistics.

---

## 5.5 Complement

### What is a complementary sequence?

Nucleotides pair according to complementary base-pairing rules.

For DNA:

```
A ↔ T
G ↔ C
```

For RNA:

```
A ↔ U
G ↔ C
```

Example:

```
DNA
ATGC

Complement
TACG
```

### Why is it useful?

Complementary sequences are fundamental to understanding nucleotide pairing and double-stranded nucleic acids.

---

## 5.6 Reverse Complement

### What does it do?

The reverse complement first creates the complement and then reverses the resulting sequence.

Example:

```
DNA:
ATGC

Complement:
TACG

Reverse complement:
GCAT
```

### Why is it useful?

DNA sequences can be represented in opposite orientations. Reverse-complement analysis is therefore commonly needed when examining both strands.

It is particularly useful when:

- searching for motifs on the opposite strand,
- examining possible coding regions,
- comparing strand orientations,
- working with sequence annotations.

---

## 5.7 Protein Translation

### What is translation?

Translation is the process of interpreting a nucleotide sequence as codons that can encode a protein.

A codon consists of three nucleotides.

For example:

```
AUG → Methionine (M)
```

GenomeZ uses an RNA codon table internally.

### How GenomeZ performs translation

The current implementation:

1. accepts DNA or RNA,
2. converts DNA T bases to RNA U bases when required,
3. searches for the first start codon:
   - ATG in DNA notation,
   - AUG after RNA conversion,
4. begins translation from that position,
5. reads codons in the same reading frame,
6. stops at the first stop codon if one is encountered.

### Start codon

The standard start codon used by the implementation is:

```
AUG
```

For DNA input, the equivalent is:

```
ATG
```

### Stop codons

RNA stop codons are:

```
UAA
UAG
UGA
```

### Output

GenomeZ reports:

- translated protein sequence,
- number of codons processed,
- whether a start codon was found,
- whether a stop codon was found.

### Important limitation

This is a sequence translation utility. It does not determine whether the resulting ORF is biologically expressed or whether it is the correct gene in a real organism.

---

## 5.8 Motif Finder

### What is a motif?

A motif is a short sequence pattern that may occur within a larger biological sequence.

Example:

```
Sequence:
ATGCGATGCGTATG

Motif:
ATG
```

The tool searches for occurrences of the supplied motif.

### What does GenomeZ report?

- the motif,
- number of matches,
- positions of matches.

Positions are reported using **1-based indexing**.

### Overlapping matches

GenomeZ checks one base at a time, so overlapping motif occurrences can also be detected.

### Why is it useful?

Motif searches can help with:

- finding known sequence patterns,
- locating short regulatory or structural patterns,
- examining candidate regions,
- basic sequence annotation workflows.

### Important limitation

Finding a motif does not prove that it has a particular biological function. Context and experimental evidence are still required.

---

## 5.9 ORF Finder

### What is an ORF?

ORF stands for **Open Reading Frame**.

An ORF is a nucleotide region that can be read as codons beginning with a start codon and ending at a compatible stop codon in the same reading frame.

A simplified structure is:

```
Start → codons → Stop
```

For DNA:

- Start: ATG
- Stops: TAA, TAG, TGA

For RNA:

- Start: AUG
- Stops: UAA, UAG, UGA

### What does GenomeZ do?

GenomeZ checks all three possible reading frames:

```
Frame 1
Frame 2
Frame 3
```

For each frame it searches for a start codon and then looks for a stop codon in the same frame.

### Output

For each detected ORF, GenomeZ reports:

- ORF number,
- frame,
- start position,
- end position,
- length,
- nucleotide sequence.

### Why is ORF finding useful?

ORF detection is a basic step in identifying possible protein-coding regions in nucleotide sequences.

It can help with:

- teaching gene structure,
- inspecting candidate coding regions,
- exploring unknown sequences,
- preparing sequences for translation.

### Important limitation

An ORF is only a **candidate coding region**.

The presence of an ORF does not by itself prove that the region is a real gene or that it is expressed.

---

# 6. Sequence Identification

## What is sequence identification?

Sequence identification attempts to determine what a nucleotide sequence may correspond to by comparing it against known biological sequences.

GenomeZ currently provides this through **NCBI BLASTN**.

## Access

Sequence Identification is the current authenticated/premium Genomics tool.

Guests can use the other public Genomics tools, but an account is required to submit this database-backed identification request.

There is currently **no paid subscription system**. Premium means authenticated access, not a payment tier.

## Current workflow

```
DNA sequence
      ↓
NCBI BLASTN
      ↓
NCBI nt database
      ↓
BLAST request ID (RID)
      ↓
short polling period
      ↓
BLAST XML
      ↓
GenomeZ results
```

The current implementation requests:

- Program: BLASTN
- Database: nt
- Output: XML

GenomeZ parses returned BLAST information and can report up to five parsed matches with information such as:

- accession,
- sequence description,
- percentage identity,
- E-value.

### What is BLASTN?

BLASTN compares a nucleotide query against nucleotide sequences in a database.

### Why is it useful?

It can help answer questions such as:

- What known sequence does this DNA resemble?
- Which database records have similar nucleotide regions?
- What organisms or annotated sequences may contain a similar sequence?

### Important limitation

BLAST similarity is not the same as definitive biological identification.

Results depend on:

- sequence quality,
- query length,
- database contents,
- similarity,
- alignment statistics,
- and the interpretation of the returned hits.

The current GenomeZ implementation also uses a short synchronous polling window. A BLAST job that has not completed during that period may be reported as still processing.

---

# 7. Proteomics Analyzer

The Proteomics workspace works with protein sequences.

It accepts:

- pasted protein sequences,
- FASTA files,
- TXT files.

The workflow is:

```
Protein input
     ↓
Sequence cleaning
     ↓
Amino-acid validation
     ↓
Protein properties
     ↓
UniProt search
     ↓
Optional external BLASTP search
```

---

# 8. Protein Sequence Validation

GenomeZ supports the standard one-letter amino-acid symbols:

```
A C D E F G H I K L M N P Q R S T V W Y
```

The protein validator:

- removes FASTA headers,
- removes formatting characters,
- converts the sequence to uppercase,
- checks that every remaining character is a supported amino-acid symbol.

Invalid symbols are reported instead of being silently treated as amino acids.

---

# 9. Protein Length

Protein length is the number of amino-acid residues in the sequence.

Example:

```
MKWVTF
```

Length:

```
6 amino acids
```

### Why is it useful?

Protein length is one of the simplest properties used when comparing proteins or checking whether a sequence is plausible for a particular protein.

---

# 10. Average Molecular Weight

GenomeZ calculates an approximate protein molecular weight from average amino-acid residue masses.

The calculation accounts for peptide-bond formation by subtracting the mass of water for each peptide bond.

The current implementation uses:

```
sum(residue masses) - (length - 1) × water mass
```

The result is reported in approximately **Daltons (Da)**.

### Important limitation

This is an estimated molecular weight based on average residue masses. Real proteins can differ because of:

- post-translational modifications,
- processing,
- sequence variants,
- experimental conditions,
- and other molecular effects.

---

# 11. Hydrophobic Percentage

### What is hydrophobicity?

Hydrophobic amino acids tend to interact less favorably with water.

GenomeZ currently counts these residues as hydrophobic for its basic percentage calculation:

```
A, I, L, M, F, W, Y, V
```

The calculation is:

```
Hydrophobic % =
hydrophobic residues / total residues × 100
```

### Why is it useful?

A simple hydrophobicity percentage can provide a first look at protein composition.

Hydrophobic regions are especially relevant when studying:

- membrane-associated proteins,
- protein folding,
- structural properties,
- sequence composition.

### Important limitation

This is a simple composition statistic, not a full hydropathy analysis. It does not calculate a residue-by-residue hydropathy profile or predict membrane topology.

---

# 12. Amino-Acid Composition

GenomeZ counts the occurrence of each supported amino acid.

Example:

```
MKWV
```

Composition includes counts for:

- A
- C
- D
- E
- F
- G
- H
- I
- K
- L
- M
- N
- P
- Q
- R
- S
- T
- V
- W
- Y

### Why is it useful?

Composition helps describe the basic chemical character of a protein sequence and provides a simple basis for comparing sequences.

---

# 13. UniProt Search

GenomeZ can send the protein sequence to the UniProt REST service for an exact-sequence search.

The current implementation requests up to five results.

Returned information can include:

- accession,
- protein ID,
- protein name,
- gene names,
- organism,
- length.

### Why use UniProt?

UniProt is a major protein sequence and annotation resource.

It can provide information associated with known protein records.

### Important distinction

GenomeZ's current UniProt workflow is an **exact-sequence search**, not a complete protein-function prediction system.

---

# 14. NCBI BLASTP

Proteomics also provides a direct link for launching an NCBI BLASTP search.

### What is BLASTP?

BLASTP compares a protein sequence against protein sequences in a selected NCBI database through the external BLAST interface.

### Why is BLASTP separate from BLASTN?

Because:

- BLASTN compares nucleotide sequences.
- BLASTP compares protein sequences.

This is another reason Genomics and Proteomics are separated in GenomeZ.

### Current implementation

GenomeZ currently generates a BLASTP launch URL containing the protein sequence.

The full BLASTP workflow is handled by the external NCBI interface rather than being synchronously rendered inside GenomeZ.

---

# 15. FASTA Files

FASTA is a common biological sequence format.

A simple FASTA record looks like:

```
>Example sequence
ATGCGTACG
```

The first line beginning with `>` is the header.

The following lines contain the sequence.

GenomeZ can accept FASTA/TXT input and removes FASTA headers before sequence analysis.

---

# 16. Sample Sequences

GenomeZ includes ready-to-use sample files:

- `sample.fasta` — DNA sample
- `sample_rna.fasta` — RNA sample
- `sample_protein.fasta` — protein sample

The sample controls are provided so users can test the platform without first finding a biological sequence.

Loading a sample fills the input area. The user can then select tools and run the analysis.

---

# 17. Results and Exports

After analysis, GenomeZ displays results in separate result cards.

Depending on the tool, results can be:

- viewed on the page,
- copied to the clipboard,
- downloaded as TXT,
- downloaded as FASTA when the result is a sequence,
- included in the full analysis report.

Examples of sequence-type results include:

- DNA → RNA,
- RNA → DNA,
- Complement,
- Reverse Complement,
- Protein Translation.

Statistical/text results such as GC Content and Motif Finder are displayed as text results.

---

# 18. Authentication

GenomeZ uses Django's built-in authentication system.

## Guest access

Guests can:

- open the website,
- open the Genomics Analyzer,
- use free Genomics tools,
- use sequence input/upload,
- use the Proteomics workspace.

## Logged-in access

Logged-in users can also access the authenticated Sequence Identification tool.

### Current access model

| Feature | Guest | Logged in |
|---|---:|---:|
| Website | Yes | Yes |
| Genomics | Yes | Yes |
| Free Genomics tools | Yes | Yes |
| Proteomics | Yes | Yes |
| Sequence Identification / BLASTN | No | Yes |

There is no subscription or payment mechanism in the current project.

---

# 19. Local Algorithms vs External Services

GenomeZ uses two different categories of functionality.

## Local computation

These operations run inside GenomeZ:

- validation,
- DNA → RNA,
- RNA → DNA,
- GC content,
- base counting,
- complement,
- reverse complement,
- translation,
- motif finding,
- ORF finding,
- protein composition,
- protein length,
- molecular-weight calculation,
- hydrophobic percentage.

These calculations do not require a biological database.

## External resources

GenomeZ also connects to external resources:

- **NCBI BLASTN** for nucleotide sequence identification,
- **NCBI BLASTP** for protein similarity searching,
- **UniProt** for protein sequence searching.

This distinction is important because local calculations can be performed immediately, while external searches depend on network connectivity and third-party services.

---

# 20. What GenomeZ Does Not Claim

GenomeZ is a practical sequence-analysis platform. Its results should be interpreted according to what each tool actually calculates.

For example:

- A high GC percentage does not identify an organism.
- A motif match does not prove biological function.
- An ORF does not automatically mean a functional gene exists.
- A translated protein sequence does not prove expression.
- A BLAST hit does not automatically establish definitive biological identity.
- A hydrophobic percentage does not by itself prove that a protein is membrane-bound.
- An exact UniProt match provides a database record match, not a complete independent biological interpretation.

The platform is therefore best understood as a **bioinformatics analysis and exploration tool**, not a replacement for biological annotation, experimental validation, or expert interpretation.

---

# 21. Typical Genomics Workflow

A user can follow this workflow:

### Step 1 — Obtain a sequence

Paste a DNA/RNA sequence or upload FASTA/TXT.

### Step 2 — Validate

GenomeZ checks:

- valid characters,
- sequence type,
- length,
- nucleotide composition.

### Step 3 — Choose tools

Examples:

- GC Content
- Base Count
- Complement
- Reverse Complement
- Translation
- Motif Finder
- ORF Finder

### Step 4 — Run

GenomeZ executes the selected algorithms.

### Step 5 — Interpret

Read the generated results and sequence statistics.

### Step 6 — Export

Copy or download the results where supported.

### Step 7 — Identify when needed

If the sequence is DNA and the user needs database-backed identification, an authenticated user can use Sequence Identification through NCBI BLASTN.

---

# 22. Typical Proteomics Workflow

### Step 1 — Obtain a protein sequence

Paste or upload a FASTA/TXT protein sequence.

### Step 2 — Validate

GenomeZ checks the amino-acid alphabet.

### Step 3 — Calculate properties

GenomeZ calculates:

- length,
- molecular weight,
- hydrophobic percentage,
- amino-acid composition.

### Step 4 — Search known records

Use the UniProt search for exact sequence matches.

### Step 5 — Compare externally

Launch NCBI BLASTP when broader protein similarity searching is required.

---

# 23. Project Architecture

The major Django applications are:

## `core/`

Handles the public website.

## `analyzer/`

Handles Genomics.

Important areas include:

- `analysis/` — individual algorithms
- `validators.py` — sequence validation
- `services.py` — analysis orchestration
- `views.py` — request handling
- `report_generator.py` — text reports
- `fasta_generator.py` — FASTA exports

## `proteomics/`

Handles protein-specific workflows.

## `accounts/`

Handles:

- signup,
- login,
- logout,
- authenticated access.

## `genomez/`

Contains the main Django project configuration.

---

# 24. Important Genomics Modules

| Module | Purpose |
|---|---|
| `dna_to_rna.py` | DNA → RNA conversion |
| `rna_to_dna.py` | RNA → DNA conversion |
| `gc_content.py` | GC percentage |
| `atgc_count.py` | nucleotide counts |
| `complement.py` | DNA/RNA complement |
| `reverse_complement.py` | reverse complement |
| `translation.py` | nucleotide → protein translation |
| `motif.py` | motif position search |
| `orf.py` | ORF detection |
| `identification.py` | NCBI BLASTN integration |
| `file_parser.py` | uploaded sequence parsing |
| `validators.py` | DNA/RNA validation |
| `services.py` | selected-tool orchestration |

---

# 25. Important Proteomics Functions

The Proteomics workspace contains logic for:

- sequence cleaning,
- amino-acid validation,
- protein property calculation,
- amino-acid composition,
- UniProt searching,
- BLASTP URL generation,
- sample protein loading.

---

# 26. Deployment

GenomeZ is configured for Render deployment.

The deployment configuration uses:

- Django,
- Gunicorn,
- WhiteNoise,
- PostgreSQL,
- environment variables.

The build process:

```
Install dependencies
        ↓
Collect static files
        ↓
Run migrations
        ↓
Start Gunicorn
```

---

# 27. External Resources

### NCBI BLAST

Used for nucleotide and protein similarity/identification workflows.

https://blast.ncbi.nlm.nih.gov/

### UniProt

Used for protein sequence searching and biological protein records.

https://www.uniprot.org/

These services are external to GenomeZ and their availability, databases, and results can change independently of the application.

---

# 28. Current Limitations

The current implementation has several deliberate limitations:

1. BLASTN uses a short synchronous polling cycle.
2. BLASTN jobs that take longer may still be processing after the current request ends.
3. BLASTP is currently launched through the external NCBI interface.
4. UniProt integration currently focuses on exact-sequence search.
5. Protein hydrophobicity is a simple percentage rather than a full hydropathy profile.
6. ORF detection is a basic reading-frame scan rather than complete gene prediction.
7. Motif finding is literal sequence matching rather than a probabilistic motif model.
8. The platform does not provide a payment/subscription system.
9. Biological results require appropriate scientific interpretation.

---

# 29. Educational and Practical Use

GenomeZ can be used for learning and demonstrating concepts such as:

- nucleotide sequence structure,
- DNA/RNA relationships,
- base composition,
- complementary strands,
- reverse complements,
- codons and translation,
- reading frames,
- ORFs,
- sequence motifs,
- protein composition,
- molecular-weight estimation,
- hydrophobicity,
- database sequence searching,
- API integration,
- Django web development.

It also demonstrates how a bioinformatics workflow can be turned into a usable web application.

---

# 30. Summary

GenomeZ connects several layers of bioinformatics into one application:

```
Biological sequence
       ↓
Validation
       ↓
Sequence classification
       ↓
Local analysis
       ↓
Results / exports
       ↓
Optional external database search
```

The project is intentionally organized around the biological difference between:

```
DNA / RNA  → Genomics
Protein     → Proteomics
```

The Genomics Analyzer focuses on nucleotide-level operations such as conversion, composition, complements, translation, motif finding, ORF detection, and authenticated BLASTN identification.

The Proteomics Analyzer focuses on amino-acid sequences, protein properties, composition, UniProt search, and BLASTP.

Together, these workspaces provide a practical foundation for sequence analysis while keeping each biological domain and its tools clearly separated.
