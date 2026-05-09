```markdown
# metaQc

Lightweight CLI tool for validation, normalization, and quality control of RNA-seq metadata.

`metaQc` was developed to help standardize heterogeneous metadata tables commonly obtained from public repositories, supplementary materials, and collaborative projects before downstream transcriptomic analysis.

The tool focuses on validating metadata integrity, harmonizing column names and categorical values, and generating clean standardized tables for RNA-seq workflows.

---

## Why metaQc?

RNA-seq metadata is often inconsistent across studies and sources.

Common issues include:

- inconsistent column names (`sample`, `sample_id`, `SampleID`)
- categorical variation (`Male`, `M`, `male`)
- duplicated samples
- missing required fields
- unbalanced experimental design
- manually curated metadata from publications

`metaQc` provides a simple CLI workflow to detect and correct these issues before analysis.

---

## Features

Current features:

- Load metadata from:
  - CSV
  - TSV
  - XLSX

- Column alias mapping
- Required column validation
- Duplicate sample detection
- Categorical normalization
- Metadata merging
- Validation report generation
- Manual metadata scaffold generation

Planned features:

- replicate balance checks
- batch confounding detection
- missingness summaries
- HTML reports
- schema customization
- MultiQC/FastQC integration

---

## Installation

Clone repository:

```bash
git clone https://github.com/your_username/metaQc.git
cd metaQc
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas typer pyyaml openpyxl rich
```

---

## Quick Start

Validate metadata:

```bash
python metaqc/cli.py run metadata.csv
```

Output:

```text
All required columns present.
No duplicate sample IDs found.
```

Generated files:

- `metadata_clean.csv`

---

## Expected Schema

Minimum required columns:

- `sample_id`
- `condition`

Optional columns:

- `study`
- `sex`
- `stage`
- `batch`
- `replicate`
- `platform`
- `layout`
- `strandedness`
- `source`
- `curation_notes`

Example:

```csv
sample_id,study,condition,sex,stage,batch,replicate
SRR001,StudyA,treated,male,adult,1,1
SRR002,StudyA,control,female,adult,1,1
```

---

## Alias Mapping

metaQc automatically standardizes common aliases.

Example:

| Input Column | Standardized Column |
| ------------ | ------------------- |
| sample       | sample_id           |
| SampleID     | sample_id           |
| gender       | sex                 |
| group        | condition           |

Aliases are defined in:

```bash
schemas/rnaseq.yaml
```

Users can customize schemas and aliases.

---

## Merge Multiple Metadata Files

Merge multiple standardized metadata files:

```bash
metaqc merge parsed_metadata/
```

Output:

- merged metadata table
- merge summary report

---

## Manual Scaffold

Generate metadata template for datasets lacking metadata:

```bash
metaqc scaffold PRJNA999999
```

Output:

```csv
sample_id,condition,sex,stage,batch,replicate,source,curation_notes
```

This is useful for manually curating metadata from publications or supplementary materials.

---

## Example Workflow

Typical usage:

```text
raw metadata
   ↓
custom parser
   ↓
standardized metadata
   ↓
metaQc validate
   ↓
normalized metadata
   ↓
merge
   ↓
downstream RNA-seq analysis
```

---

## Project Structure

```text
metaQc/
├── metaqc/
│   ├── cli.py
│   ├── io.py
│   ├── parser.py
│   ├── validator.py
│   ├── normalizer.py
│   └── report.py
├── schemas/
│   └── rnaseq.yaml
├── tests/
├── requirements.txt
└── README.md
```


## Contributing

Contributions, suggestions, and issue reports are welcome.

Feel free to open pull requests or submit feature requests.
```
