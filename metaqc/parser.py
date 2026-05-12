def map_aliases(df, aliases):
    """
    Rename columns based on alias mapping.
    Returns transformed dataframe and applied mappings.
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
