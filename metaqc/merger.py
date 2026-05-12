from pathlib import Path
import pandas as pd

from metaqc.io import load_metadata, load_schema
from metaqc.parser import map_aliases
from metaqc.normalizer import normalize_values
from metaqc.validator import validate_required_columns


def merge_metadata(folder_path: str, schema_file: str):
    """
    Validate and merge multiple metadata files.
    """
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    schema = load_schema(schema_file)
    merged_dfs = []

    for file in folder.iterdir():
        if file.suffix.lower() not in [".csv", ".tsv", ".xlsx", ".xls"]:
            continue

        df = load_metadata(str(file))
        df = map_aliases(df, schema["aliases"])
        df = normalize_values(df, schema["normalization"])

        missing = validate_required_columns(
            df,
            schema["required_columns"]
        )

        if missing:
            print(f"Skipping {file.name}: missing columns {missing}")
            continue

        merged_dfs.append(df)

    if not merged_dfs:
        raise ValueError("No valid metadata files found.")

    merged = pd.concat(merged_dfs, ignore_index=True)

    return merged
