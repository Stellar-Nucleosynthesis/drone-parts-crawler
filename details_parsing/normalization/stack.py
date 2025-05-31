from details_parsing.normalization import utils

def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "mount_size"] = df["mount_size"].apply(utils.get_size_mm)
    df.loc[:, "working_current"] = df["working_current"].apply(utils.get_current)
    df.loc[:, "max_current"] = df["max_current"].apply(utils.get_current)
    df.loc[:, "range_s"] = df["range_s"].apply(utils.get_num_serial_cells)
    df = df.dropna(subset=["model"])
    df = df.dropna(subset=["mount_size"])
    df = df.dropna(subset=["cable_connector"])
    df = df.dropna(subset=["working_current"])
    df = df.dropna(subset=["max_current"])
    df = df.dropna(subset=["range_s"])
    df = df[df["model"].str.contains("Stack", na=False)]
    df.reset_index(drop=True, inplace=True)
    return df