import pandas as pd


def generate_report(df, missing_columns, duplicates, schema, alias_map=None):
    """
    Generate enriched validation report.
    """

    lines = []

    lines.append("Validation Summary")
    lines.append("=" * 30)
    lines.append("")

    # Dataset overview
    lines.append(f"Rows: {len(df)}")
    lines.append(f"Columns: {len(df.columns)}")
    lines.append("")

    # Required columns
    if not missing_columns:
        lines.append("Required columns: OK")
    else:
        lines.append(f"Missing required columns: {', '.join(missing_columns)}")

    lines.append("")

    # Duplicates
    if not duplicates:
        lines.append("Duplicates: none")
    else:
        lines.append(f"Duplicate sample IDs: {', '.join(duplicates)}")

    lines.append("")

    # Schema summary
    if schema:
        required = schema.get("required_columns", [])
        optional = schema.get("optional_columns", [])

        lines.append("Schema summary:")
        lines.append(f"- Required: {', '.join(required) if required else 'none'}")
        lines.append(f"- Optional: {', '.join(optional) if optional else 'none'}")
        lines.append("")

    # Column snapshot
    lines.append("Final columns:")
    lines.append(", ".join(df.columns))
    lines.append("")

    # Alias trace (required? )
    if alias_map:
    	lines.append("Applied alias mapping:")
    	for original, standardized in alias_map.items():
        	lines.append(f"- {original} -> {standardized}")
    return "\n".join(lines)


def save_report(report, output_path="validation_report.txt"):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
