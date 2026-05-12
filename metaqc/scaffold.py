from pathlib import Path
import pandas as pd


DEFAULT_COLUMNS = [
    "sample_id",
    "study",
    "stage",
    "sex",
    "tissue",
    "condition",
    "batch",
    "replicate",
    "source",
    "curation_notes"
]


def extract_sample_ids(samples_dir: str):
    """
    Extract sample IDs from files in directory.
    Removes common FASTQ extensions.
    """
    folder = Path(samples_dir)

    sample_ids = []

    for file in folder.iterdir():
        if not file.is_file():
            continue

        name = file.name

        for suffix in [
            ".fastq.gz",
            ".fq.gz",
            ".fastq",
            ".fq",
            ".bam",
            ".sam"
        ]:
            if name.endswith(suffix):
                name = name.removesuffix(suffix)
                break

        sample_ids.append(name)

    return sorted(sample_ids)


def create_scaffold(
    study_name: str,
    output_file: str,
    samples_dir: str = None
):
    """
    Create metadata scaffold CSV.
    Optionally populate sample IDs from directory.
    """

    if samples_dir:
        sample_ids = extract_sample_ids(samples_dir)
        df = pd.DataFrame({"sample_id": sample_ids})
    else:
        df = pd.DataFrame(columns=DEFAULT_COLUMNS)
        df.loc[0, "sample_id"] = ""

    df["study"] = study_name

    for col in DEFAULT_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[DEFAULT_COLUMNS]

    if samples_dir:
        df["source"] = "local_files"

    df.to_csv(output_file, index=False)
