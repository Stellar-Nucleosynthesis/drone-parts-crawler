import re
import numpy as np

def get_len_inches(s):
    if not s or s is None or s is np.nan:
        return None
    s = s.lower().replace(',', '.').strip()

    inch_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:дюйм(?:ів|и)?|")', s)
    mm_matches = re.findall(r'(\d+(?:\.\d+)?)\s*мм', s)

    range_match = re.findall(r'(\d+(?:\.\d+)?)\s*~\s*(\d+(?:\.\d+)?)', s)

    or_match = re.findall(r'(\d+(?:\.\d+)?)\s*(?:мм|"?)\s*або\s*(\d+(?:\.\d+)?)', s)

    if range_match:
        start, end = map(float, range_match[0])
        return start

    if or_match:
        return None #undefined

    if inch_matches:
        nums = list(map(float, inch_matches))
        return sum(nums) / len(nums)

    if mm_matches:
        nums = list(map(float, mm_matches))
        return round((nums[0] / 25.4) * 10) / 10

    lone_inch = re.match(r'^(\d+(?:\.\d+)?)"$', s)
    if lone_inch:
        return float(lone_inch.group(1))

    return None

def get_mass(s):
    if not s or s is None or s is np.nan:
        return None
    s = s.lower().replace(',', '.').strip()

    mass_matches = re.findall(r'(\d+(?:\.\d+)?)\s*г', s)
    if mass_matches:
        return float(mass_matches[0])
    return None

def get_size_mm(s, max_values=2, max_axis=3):
    if not s or s is None or s is np.nan:
        return None
    s = s.lower().replace(',', '.').strip()

    pattern = re.compile(
        r'(\d+(?:\.\d+)?)\s*(?:мм)?\s*[*xX×]\s*'
        r'(\d+(?:\.\d+)?)\s*(?:мм)?'
        r'(?:\s*[*xX×]\s*(\d+(?:\.\d+)?))?'
    )
    all_matches = pattern.findall(s)
    dimensions = []
    for match in all_matches:
        group = [float(x) for x in match if x]
        dimensions.append(group)
    if dimensions:
        return ",".join(["*".join(map(str, vals[:max_axis])) for vals in dimensions[:max_values]])
    return None

def normalize_mass_size(df):
    df.loc[:, "mass"] = df["mass"].apply(get_mass)
    df.loc[:, "size_mm"] = df["size_mm"].apply(get_size_mm)

def get_list_mm(s):
    if not s or s is None or s is np.nan:
        return None
    s = s.lower().replace(',', '.').strip()

    mm_matches = re.findall(r'(\d+(?:\.\d+)?)\s*мм', s)
    mm_matches = list(set(map(float, mm_matches)))
    if mm_matches:
        return ",".join(map(str, mm_matches))
    return None

def get_video_format(s):
    if not s or s is None or s is np.nan:
        return None
    formats = re.findall(r'PAL|NTSC', s)
    if formats:
        return ",".join(formats)
    return None

def get_frequency(s):
    if not s or s is None or s is np.nan:
        return None
    matches = re.findall(r'(\d+(?:\.\d+)?)\s*(ггц|ghz|g|мгц|mhz|m)', s.lower())
    frequencies = []
    for value, unit in matches:
        value = float(value)
        if unit in ["мгц", "mhz", "m"]:
            if value > 1000:
                value /= 1000
                frequencies.append(str(value) + "G")
            else:
                frequencies.append(str(value) + "M")
        else:
            frequencies.append(str(value) + "G")
    if frequencies:
        return ",".join(set(frequencies))
    return None

def get_max_power(s):
    if not s or s is None or s is np.nan:
        return None
    matches = re.findall(r'(\d+(?:\.\d+)?)\s*(мвт|вт|mw|w)', s.lower())
    powers_mw = []
    for value, unit in matches:
        value = float(value)
        if unit == 'вт' or unit == 'w':
            value *= 1000
        powers_mw.append(value)
    return max(powers_mw) if powers_mw else None

def get_num_serial_cells(s):
    if not s or s is None or s is np.nan:
        return None
    range_match = re.search(r'(\d+)\s*-\s*(\d+)\s*s', s.lower())
    if range_match:
        return "%s-%s" % (range_match.group(1), range_match.group(2))

    single_match = re.search(r'(\d+)\s*s', s.lower())
    if single_match:
        return single_match.group(1)
    return None

def get_current(s):
    if not s or s is None or s is np.nan:
        return None
    val = re.search(r'(\d+(?:\.\d+)?)(\s*A)', s)
    if val:
        return float(val.group(1))
    return None
