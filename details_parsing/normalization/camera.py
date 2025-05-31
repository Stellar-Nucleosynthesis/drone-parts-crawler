import re
import numpy as np
from details_parsing.normalization import utils

def __get_tvl(s):
    if not s or s is None or s is np.nan:
        return None
    tvl_matches = re.search(r'(\d+)(\s*TVL)', s)
    if tvl_matches:
        return int(tvl_matches.group(1))
    return None

def __get_camera_mount(s):
    return utils.get_size_mm(s, 2, 2)

def __get_aspect_ratio(s):
    if not s or s is None or s is np.nan:
        return None
    ratios = re.findall(r'\d+:\d+', s)
    if ratios:
        return ",".join(ratios)
    return None

def normalize(df):
    utils.normalize_mass_size(df)
    df.loc[:, "tvl"] = df["tvl"].apply(__get_tvl)
    df.loc[:, "mount_size"] = df["size_mm"].apply(__get_camera_mount)
    df.loc[:, "aspect_ratio"] = df["aspect_ratio"].apply(__get_aspect_ratio)
    df.loc[:, "video_format"] = df["video_format"].apply(utils.get_video_format)
    df = df.dropna(subset=["model"])
    df = df.dropna(subset=["mount_size"])
    df = df.dropna(subset=["aspect_ratio"])
    df = df.dropna(subset=["video_format"])
    df.reset_index(drop=True, inplace=True)
    return df