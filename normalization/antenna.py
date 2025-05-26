import re
import numpy as np
from normalization import utils

def __get_dbi(s):
    if not s or s is None or s is np.nan:
        return None
    tvl_matches = re.search(r'(\d+(?:\.\d+)?)(\s*(dbi|дбі))', s.lower())
    if tvl_matches:
        return float(tvl_matches.group(1))
    return None

def __get_polarization(s):
    if not s or s is None or s is np.nan:
        return None
    dirs = re.findall(r'RHCP|LHCP', s)
    if dirs:
        return ",".join(dirs)
    return None

def __get_swr(s):
    if not s or s is None or s is np.nan:
        return None
    tvl_matches = re.search(r'(\d+(?:\.\d+)?)', s.lower())
    if tvl_matches:
        return float(tvl_matches.group(1))
    return None

def __get_antenna_type(freq):
    if not freq or freq is None or freq is np.nan:
        return None
    frequencies = freq.split(',')
    res = []
    for f in frequencies:
        if f in ["5.65G", "5.8G", "6.0G", "6.13G", "5.85G", "5.9G", "5.6G"]:
            res.append("VTX")
        elif f in ["868.0M", "915.0M", "2.4G"]:
            res.append("RX")
    if res:
        return ','.join(set(res))
    return None

def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "frequency"] = df["frequency"].apply(utils.get_frequency)
    df.loc[:, "dbi"] = df["dbi"].apply(__get_dbi)
    df.loc[:, "polarization"] = df["polarization"].apply(__get_polarization)
    df.loc[:, "swr"] = df["swr"].apply(__get_swr)
    df.loc[:, "antenna_type"] = df["frequency"].apply(__get_antenna_type)
    df = df.dropna(subset=["model"])
    df = df.dropna(subset=["connector"])
    df = df.dropna(subset=["frequency"])
    df = df.dropna(subset=["antenna_type"])
    df.reset_index(drop=True, inplace=True)
    return df