from normalization import utils

def normalize(df):
    df.loc[:, "propeller_size"] = df["propeller_size"].apply(utils.get_len_inches)
    df = df.dropna(subset=["propeller_size"])
    df.reset_index(drop=True, inplace=True)
    return df