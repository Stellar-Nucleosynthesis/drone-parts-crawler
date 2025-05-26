from normalization import utils

def normalize(df):
    df.loc[:, "size_inches"] = df["size_inches"].apply(utils.get_len_inches)
    df = df.dropna(subset=["model"])
    df = df.dropna(subset=["material"])
    df = df.dropna(subset=["size_inches"])
    df.reset_index(drop=True, inplace=True)
    return df