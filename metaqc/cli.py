
import typer

from metaqc.io import load_metadata, load_schema, save_metadata
from metaqc.parser import map_aliases
from metaqc.validator import validate_required_columns, check_duplicates
from metaqc.normalizer import normalize_values
from metaqc.report import generate_report, save_report
from metaqc.merger import merge_metadata

app = typer.Typer()


@app.command()
def validate(
    input_file: str,
    schema_file: str = "schemas/rnaseq.yaml"
):
    """
    Validate and normalize RNA-seq metadata.
    """
    df = load_metadata(input_file)
    schema = load_schema(schema_file)

    df = map_aliases(df, schema["aliases"])
    df = normalize_values(df, schema["normalization"])

    missing = validate_required_columns(
        df,
        schema["required_columns"]
    )
    duplicates = check_duplicates(df)

    report = generate_report(missing, duplicates)

    save_metadata(df, "metadata_clean.csv")
    save_report(report, "validation_report.txt")

    print(report)
    print("\nGenerated files:")
    print("- metadata_clean.csv")
    print("- validation_report.txt")

@app.command()
def merge(
    input_folder: str,
    schema_file: str = "schemas/rnaseq.yaml"
):
    """
    Merge multiple metadata files.
    """
    merged = merge_metadata(input_folder, schema_file)

    save_metadata(merged, "merged_metadata.csv")

    print("Merge completed successfully.")
    print("Generated file:")
    print("- merged_metadata.csv")

if __name__ == "__main__":
    app()
