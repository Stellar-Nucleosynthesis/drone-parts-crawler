from details_parsing.normalization import utils

def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "propellers_inches"] = df["propellers_inches"].apply(utils.get_len_inches)
    df.loc[:, "cam_mount_size"] = df["cam_mount_size"].apply(utils.get_list_mm)
    df.loc[:, "motor_mount_size"] = df["motor_mount_size"].apply(utils.get_list_mm)
    df = df.dropna(subset=["model"])
    df = df.dropna(subset=["propellers_inches"])
    df = df.dropna(subset=["cam_mount_size"])
    df = df.dropna(subset=["motor_mount_size"])
    df.reset_index(drop=True, inplace=True)
    return df