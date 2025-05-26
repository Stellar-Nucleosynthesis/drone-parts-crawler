import re
import numpy as np
from normalization import utils

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

def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "rotation_speed"] = df["rotation_speed"].apply(__get_rotation_speed)
    df.loc[:, "num_s"] = df["num_s"].apply(utils.get_num_serial_cells)
    df.loc[:, "max_current"] = df["max_current"].apply(utils.get_current)
    df.loc[:, "max_power"] = df["max_power"].apply(__get_power)
    return df