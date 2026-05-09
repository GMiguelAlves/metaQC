def normalize_values(df, normalization_rules):
    """
    Normalize categorical values according to schema rules.
    """
    for column, rules in normalization_rules.items():
        if column in df.columns:
            df[column] = df[column].replace(rules)

    return df
