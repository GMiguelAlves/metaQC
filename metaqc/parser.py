import re
import yaml
import pandas as pd


def map_aliases(df, aliases):
    """
    Rename columns based on alias mapping.
    """
    rename_dict = {}
    applied = {}

    normalized_columns = {
        col.lower().strip(): col for col in df.columns
    }

    for standard_name, alias_list in aliases.items():
        for alias in alias_list:
            alias_norm = alias.lower().strip()

            if alias_norm in normalized_columns:
                original_col = normalized_columns[alias_norm]
                rename_dict[original_col] = standard_name
                applied[original_col] = standard_name
                break

    df = df.rename(columns=rename_dict)
    return df, applied


def load_parse_config(config_file):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


def apply_regex_map(value, mapping):
    for pattern, result in mapping.items():
        if re.search(pattern, str(value), re.IGNORECASE):
            return result
    return None


def apply_regex_extract(value, pattern):
    match = re.search(pattern, str(value))
    if match:
        return match.group(1)
    return None


def build_sample_id(row):
    """
    Canonical sample_id generator.
    Always recomputed, never inherited.
    """

    def clean(x):
        if pd.isna(x):
            return None
        return str(x).strip()

    stage = clean(row.get("stage"))
    sex = clean(row.get("sex"))
    condition = clean(row.get("condition"))
    replicate = row.get("replicate")
    batch = clean(row.get("batch"))

    stage = stage[:4].upper() if stage else "UNKN"
    sex = sex[:3].upper() if sex else "UNK"
    condition = condition[:4].upper() if condition else "UNKN"

    if pd.notna(replicate):
        try:
            replicate = f"R{int(replicate)}"
        except Exception:
            replicate = "R0"
    else:
        replicate = "R0"

    batch = batch if batch else "B0"

    return f"SM_{stage}_{sex}_{condition}_{replicate}_{batch}"


def semantic_parse(df, config):
    """
    Transform metadata into canonical RNA-seq schema.
    """

    output = pd.DataFrame()

    columns = config["columns"]

    run_field = columns["run_field"]
    sample_field = columns["sample_field"]

    # run accession is always preserved
    output["run_accession"] = df[run_field]

    # defaults
    defaults = config.get("defaults", {})
    for key, value in defaults.items():
        output[key] = value

    # parsing rules
    parsing = config.get("parsing", {})

    for field, rules in parsing.items():
        source = rules["source"]

        if "regex_map" in rules:
            output[field] = df[source].apply(
                lambda x: apply_regex_map(x, rules["regex_map"])
            )

        elif "regex_extract" in rules:
            output[field] = df[source].apply(
                lambda x: apply_regex_extract(x, rules["regex_extract"])
            )

        elif rules.get("copy", False):
            output[field] = df[source]

    # ensure required columns exist before sample_id build
    for col in ["stage", "sex", "condition", "replicate", "batch"]:
        if col not in output.columns:
            output[col] = None

    # ALWAYS rebuild sample_id (canonical logic)
    output["sample_id"] = output.apply(build_sample_id, axis=1)

    # fallback safety (rare cases)
    if output["sample_id"].isna().all():
        output["sample_id"] = df[sample_field]

    # ensure final schema
    final_cols = [
        "sample_id",
        "stage",
        "sex",
        "condition",
        "replicate",
        "batch",
        "dataset",
        "lane",
        "run_accession"
    ]

    for col in final_cols:
        if col not in output.columns:
            output[col] = None

    output = output[final_cols]

    return output
