def validate_required_columns(df, required_columns):
    """
    Check if all required columns are present.
    Returns a list of missing columns.
    """
    missing = [col for col in required_columns if col not in df.columns]
    return missing


def check_duplicates(df, id_column="sample_id"):
    """
    Check duplicated sample IDs.
    Returns a list of duplicated IDs.
    """
    if id_column not in df.columns:
        return []

    duplicates = df[df[id_column].duplicated()][id_column].tolist()
    return duplicates
