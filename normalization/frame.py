from normalization import utils

def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "propellers_inches"] = df["propellers_inches"].apply(utils.get_len_inches)
    df = df.dropna(subset=["propellers_inches"])
    df.reset_index(drop=True, inplace=True)
    df.loc[:, "cam_mount_size"] = df["cam_mount_size"].apply(utils.get_list_mm)
    return df