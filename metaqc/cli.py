import typer
from typing import Optional

from metaqc.io import load_metadata, load_schema, save_metadata
from metaqc.parser import map_aliases,load_parse_config, semantic_parse
from metaqc.validator import validate_required_columns, check_duplicates
from metaqc.normalizer import normalize_values
from metaqc.report import generate_report, save_report
from metaqc.merger import merge_metadata
from metaqc.scaffold import create_scaffold
#from metaqc.enrich import enrich

app = typer.Typer()


@app.command()
def validate(
    input_file: str,
    schema_file: str = "schemas/rnaseq.yaml",
    keep: Optional[str] = None,
    output: str = "metadata_clean.csv"

):
    """
    Validate and normalize RNA-seq metadata.
    """

    df = load_metadata(input_file)
    schema = load_schema(schema_file)

    df, applied_aliases = map_aliases(df, schema["aliases"])
    df = normalize_values(df, schema["normalization"])

    missing = validate_required_columns(
        df,
        schema["required_columns"]
    )
    duplicates = check_duplicates(df)

    report = generate_report(
    df=df,
    missing_columns=missing,
    duplicates=duplicates,
    schema=schema,
    alias_map=applied_aliases
)

    if keep:
        keep_columns = [col.strip() for col in keep.split(",")]

        existing_columns = [
            col for col in keep_columns
            if col in df.columns
        ]

        df = df[existing_columns]

    save_metadata(df, output)
    save_report(report, "validation_report.txt")

    print(report)
    print("\nGenerated files:")
    print(f"- {output}")
    print("- validation_report.txt")


@app.command()
def merge(
    input_folder: str,
    schema_file: str = "schemas/rnaseq.yaml",
    output: str = "merged_metadata.csv"

):
    """
    Validate and merge multiple metadata files.
    """

    merged = merge_metadata(input_folder, schema_file)

    save_metadata(merged, output)

    print("Merge completed successfully.")
    print("Generated file:")
    print(f"- {output}")

@app.command()
def scaffold(
    study_name: str,
    output: str = "metadata_scaffold.csv",
    samples_dir: Optional[str] = None
):
    """
    Generate metadata scaffold template. Optionally infer samples from directory.
    """

    create_scaffold(
        study_name=study_name,
        output_file=output,
        samples_dir=samples_dir
    )

    print("Scaffold created successfully.")
    print("Generated file:")
    print(f"- {output}")

@app.command()
def parse(
    input_file: str,
    config_file: str = typer.Option(..., "--config"),
    output: str = typer.Option("parsed_metadata.tsv", "--output")
):
    """
    Parse validated metadata into canonical schema.
    """

    df = load_metadata(input_file)
    config = load_parse_config(config_file)

    parsed = semantic_parse(df, config)
    save_metadata(parsed, output)

    print(f"Parsed metadata written to {output}")

@app.command()
def enrich(
    ena_file: str,
    author_file: str,
    config_file: str,
    output: str = "enriched_metadata.csv"
):
    """
    Join ENA metadata with author metadata to recover biological annotations.
    """

    from metaqc.io import load_metadata, save_metadata
    from metaqc.enrich import load_enrich_config, enrich_metadata

    ena_df = load_metadata(ena_file)
    author_df = load_metadata(author_file)
    config = load_enrich_config(config_file)

    enriched = enrich_metadata(ena_df, author_df, config)

    save_metadata(enriched, output)

    print("Enrichment completed successfully.")
    print(f"- {output}")

if __name__ == "__main__":
    app()
