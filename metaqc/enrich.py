import pandas as pd
import yaml


def load_enrich_config(config_file):
    """
    Load enrich YAML config.
    """
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


def standardize_columns(df):
    """
    Strip whitespace from column names.
    """
    df.columns = [col.strip() for col in df.columns]
    return df


def explode_lanes(author_df, config):
    """
    Convert wide lane metadata into long format.

    Example:
        Lane 1 ENA Run Accession
        Lane 2 ENA Run Accession

    becomes:

        lane | run_accession
    """
    lane_cfg = config.get("lane_columns")

    if not lane_cfg:
        return author_df

    id_vars = lane_cfg["id_vars"]
    value_vars = lane_cfg["value_vars"]

    author_long = author_df.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="lane",
        value_name="run_accession"
    )

    author_long = author_long.dropna(
        subset=["run_accession"]
    )

    return author_long


def enrich_metadata(ena_df, author_df, config):
    """
    Enrich ENA metadata with author metadata.
    """

    ena_df = standardize_columns(ena_df)
    author_df = standardize_columns(author_df)

    # optional wide -> long transformation
    author_df = explode_lanes(author_df, config)

    join_cfg = config["join"]

    left_key = join_cfg["left_key"]
    right_key = join_cfg["right_key"]
    how = join_cfg.get("how", "left")

    merged = ena_df.merge(
        author_df,
        left_on=left_key,
        right_on=right_key,
        how=how,
        suffixes=("_ena", "_author")
    )

    # create canonical columns from mappings
    mappings = config.get("mappings", {})

    for target_col, source_col in mappings.items():
        if source_col in merged.columns:
            merged[target_col] = merged[source_col]

    # optional removal of unmatched rows
    if config.get("drop_unmatched", False):
        if "sample_id" in merged.columns:
            merged = merged.dropna(
                subset=["sample_id"]
            )

    # optional cleanup
    drop_cols = config.get("drop", [])

    existing_drop = [
        col for col in drop_cols
        if col in merged.columns
    ]

    merged = merged.drop(
        columns=existing_drop
    )

    return merged
