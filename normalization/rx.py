from normalization import utils

def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "frequency"] = df["frequency"].apply(utils.get_frequency)
    df = df.dropna(subset=["frequency"])
    df.reset_index(drop=True, inplace=True)
    return df