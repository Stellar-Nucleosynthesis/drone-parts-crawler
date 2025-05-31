import re
import numpy as np
from details_parsing.normalization import utils

def __get_rotation_speed(s):
    if not s or s is None or s is np.nan:
        return None
    val = re.search(r'(\d+)(KV)?', s)
    if val:
        return int(val.group(1))
    return None

def __get_power(s):
    if not s or s is None or s is np.nan:
        return None
    tvl_matches = re.search(r'(\d+(?:\.\d+)?)(\s*(w|вт))', s.lower())
    if tvl_matches:
        return float(tvl_matches.group(1))
    return None

def __get_mount_size(s):
    if not s or s is None or s is np.nan:
        return None
    match = re.search(r'(\d{4})', s)
    if not match:
        return None

    stator = match.group(1)
    diameter = int(stator[:2])

    if diameter <= 11:
        return "6.6"
    elif diameter <= 16:
        return "9.0"
    elif diameter <= 18:
        return "12.0"
    elif diameter <= 27:
        return "16.0"
    elif diameter <= 28:
        return "19.0"
    else:
        return None


def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "rotation_speed"] = df["rotation_speed"].apply(__get_rotation_speed)
    df.loc[:, "range_s"] = df["range_s"].apply(utils.get_num_serial_cells)
    df.loc[:, "max_current"] = df["max_current"].apply(utils.get_current)
    df.loc[:, "max_power"] = df["max_power"].apply(__get_power)
    df.loc[:, "mount_size"] = df["model"].apply(__get_mount_size)
    df = df.dropna(subset=["model"])
    df = df.dropna(subset=["mount_size"])
    df = df.dropna(subset=["rotation_speed"])
    df = df.dropna(subset=["range_s"])
    df = df.dropna(subset=["max_current"])
    df = df.dropna(subset=["max_power"])
    df.reset_index(drop=True, inplace=True)
    return df