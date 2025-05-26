import re
import numpy as np
from normalization import utils

def __get_discharge_current(s):
    if not s or s is None or s is np.nan:
        return None
    val = re.findall(r'\d+C', s)
    if val:
        return int(val[0][:-1])
    return None

def __get_battery_capacity(s):
    if not s or s is None or s is np.nan:
        return None
    val = re.search(r'(\d+)(маг|mah)', s.lower().replace(' ', ''))
    if val:
        return int(val.group(1))
    return None

def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "num_s"] = df["num_s"].apply(utils.get_num_serial_cells)
    df.loc[:, "discharge_current"] = df["discharge_current"].apply(__get_discharge_current)
    df.loc[:, "capacity"] = df["capacity"].apply(__get_battery_capacity)
    return df