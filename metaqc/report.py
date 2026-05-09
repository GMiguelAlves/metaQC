def generate_report(missing_columns, duplicates):
    """
    Generate validation report as string.
    """
    lines = []
    lines.append("Validation Summary")
    lines.append("=" * 20)
    lines.append("")

    if not missing_columns:
        lines.append("Required columns: OK")
    else:
        lines.append(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    if not duplicates:
        lines.append("Duplicates: none")
    else:
        lines.append(
            f"Duplicate sample IDs found: {', '.join(duplicates)}"
        )

    return "\n".join(lines)


def save_report(report, output_path="validation_report.txt"):
    """
    Save validation report to file.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report)
