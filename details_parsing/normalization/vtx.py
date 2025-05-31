from details_parsing.normalization import utils

def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "max_power"] = df["max_power"].apply(utils.get_max_power)
    df.loc[:, "video_format"] = df["video_format"].apply(utils.get_video_format)
    df.loc[:, "frequency"] = df["frequency"].apply(utils.get_frequency)
    df = df.dropna(subset=["model"])
    df = df.dropna(subset=["max_power"])
    df = df.dropna(subset=["frequency"])
    df = df[~df["model"].str.contains("Цифрова Система", na=False)]
    df.reset_index(drop=True, inplace=True)
    return df