from pathlib import Path
import pandas as pd
import yaml


SUPPORTED_EXTENSIONS = [".csv", ".tsv", ".xlsx", ".xls"]


def load_metadata(file_path: str) -> pd.DataFrame:
    """
    Load metadata file into pandas DataFrame.

    Supported formats:
    - .csv
    - .tsv
    - .xlsx
    - .xls
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported format: {suffix}. "
            f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    if suffix == ".csv":
        return pd.read_csv(path)

    if suffix == ".tsv":
        return pd.read_csv(path, sep="\t")

    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)

    raise ValueError(f"Could not load file: {file_path}")


def save_metadata(df: pd.DataFrame, output_path: str = "metadata_clean.csv") -> None:
    """
    Save cleaned metadata as CSV.
    """
    df.to_csv(output_path, index=False)


def load_schema(schema_path: str) -> dict:
    """
    Load YAML schema configuration.
    """
    path = Path(schema_path)

    if not path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    with open(path, "r", encoding="utf-8") as file:
        schema = yaml.safe_load(file)

    return schema
