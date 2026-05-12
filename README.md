# metaQC

A lightweight CLI tool for RNA-seq metadata validation, normalization, harmonization, and scaffold generation.

`metaQC` was designed to simplify the preprocessing of heterogeneous metadata obtained from public repositories and collaborators, especially in large-scale transcriptomic and meta-analysis workflows.

It helps standardize inconsistent metadata formats, validate required fields, merge multiple studies, and generate metadata templates for manual curation.

---

## Features

- Validate metadata files (`csv`, `tsv`, `xlsx`, `xls`)
- Normalize column names using alias mapping
- Normalize categorical values (e.g. `M` → `male`, `F` → `female`)
- Detect duplicated sample IDs
- Validate required schema fields
- Merge multiple metadata files into a single table
- Automatically assign study names during merge
- Generate scaffold templates for missing metadata
- Infer sample IDs directly from sequencing files
- Generate human-readable validation reports

---

## Installation

Clone repository:

```bash
git clone https://github.com/GMiguelAlves/metaQC.git
cd metaQC
```

Install locally:

```bash
pip install -e .
```

After installation, the CLI command becomes available:

```bash
metaqc --help
```

---

## Commands

### Validate metadata

Validate and normalize a metadata file:

```bash
metaqc validate metadata.tsv
```

Outputs:

- `metadata_clean.csv`
- `validation_report.txt`

Custom output:

```bash
metaqc validate metadata.tsv --output cleaned_metadata.csv
```

Keep only selected columns:

```bash
metaqc validate metadata.tsv \
    --keep sample_id,stage,sex \
    --output minimal_metadata.csv
```

---

### Merge metadata

Merge multiple metadata files from a folder:

```bash
metaqc merge metadata_folder/
```

Custom output:

```bash
metaqc merge metadata_folder/ --output merged_metadata.csv
```

During merge:
- each file is validated
- aliases are standardized
- invalid files are skipped
- `study` column is automatically added using filename if missing

---

### Generate scaffold template

Create empty metadata template:

```bash
metaqc scaffold PRJNA12345
```

Output:

- `metadata_scaffold.csv`

Example:

```csv
sample_id,study,stage,sex,tissue,condition,batch,replicate,source,curation_notes
,PRJNA12345,,,,,,,
```

---

### Scaffold from sample directory

Automatically infer sample IDs from sequencing files:

```bash
metaqc scaffold PRJNA12345 --samples-dir data/
```

Supported file extensions:

- `.fastq.gz`
- `.fq.gz`
- `.fastq`
- `.fq`
- `.bam`
- `.sam`

Example directory:

```text
data/
├── SRR001.fastq.gz
├── SRR002.fastq.gz
├── SRR003.bam
```

Generated scaffold:

```csv
sample_id,study,stage,sex,tissue,condition,batch,replicate,source,curation_notes
SRR001,PRJNA12345,,,,,,,local_files,
SRR002,PRJNA12345,,,,,,,local_files,
SRR003,PRJNA12345,,,,,,,local_files,
```

---

## Schema system

metaQC uses YAML schemas for metadata standardization.

Example schema:

```yaml
required_columns:
  - sample_id

optional_columns:
  - study
  - stage
  - sex
  - tissue
  - condition
  - batch
  - replicate
  - platform
  - layout
  - strandedness
  - source
  - curation_notes
```

Aliases:

```yaml
aliases:
  sample_id:
    - sample
    - sampleid
    - sample_name
    - sample name

  stage:
    - location
    - lifecycle_stage
```

Normalization:

```yaml
normalization:
  sex:
    M: male
    F: female
```

Use custom schema:

```bash
metaqc validate metadata.tsv --schema-file custom_schema.yaml
```

---

## Validation report

Example generated report:

```text
Validation Summary
==============================

Rows: 75
Columns: 21

Required columns: OK

Duplicates: none

Schema summary:
- Required: sample_id
- Optional: study, stage, sex, tissue, condition

Final columns:
sample_id, stage, sex

Applied alias mapping:
- Sample Name -> sample_id
- Location -> stage
- Sex -> sex
```

---

## Example workflow

Generate scaffold from raw files:

```bash
metaqc scaffold PRJNA12345 --samples-dir raw_data/
```

Curate metadata manually, then validate:

```bash
metaqc validate curated_metadata.csv \
    --keep sample_id,stage,sex \
    --output clean_metadata.csv
```

Merge multiple studies:

```bash
metaqc merge studies/ --output merged_metadata.csv
```

---

## Project structure

```text
metaQC/
├── metaqc/
│   ├── cli.py
│   ├── io.py
│   ├── parser.py
│   ├── validator.py
│   ├── normalizer.py
│   ├── merger.py
│   ├── scaffold.py
│   ├── report.py
│   └── __init__.py
├── schemas/
│   └── rnaseq.yaml
├── tests/
├── pyproject.toml
└── README.md
```

---

## Roadmap

Planned improvements:

- JSON report export
- ontology-aware metadata validation
- automatic ENA/SRA metadata retrieval
- regex-based sample annotation inference
- pipeline integration modules

---

## License

MIT License
