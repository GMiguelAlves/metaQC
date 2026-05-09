def map_aliases(df, aliases):
    """
    Rename columns according to alias mapping defined in schema.
    """
    rename_dict = {}

    for standard_name, alias_list in aliases.items():
        for col in df.columns:
            if col.lower() in [alias.lower() for alias in alias_list]:
                rename_dict[col] = standard_name

    df = df.rename(columns=rename_dict)

    return df
