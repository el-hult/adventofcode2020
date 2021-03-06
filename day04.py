import re
from util import read_input

test_data1 = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""
test_data2 = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""
test_data3 = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""
data = read_input(4)
needed_keys = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])


def pass2dict(passport: str) -> dict:
    try:
        pp = {entry.split(":")[0]: entry.split(":")[1] for entry in passport.split()}
        out = {}
        for key in needed_keys:
            out[key] = pp[key]
        return pp
    except KeyError:
        return None


def parse_year(s: str, min: int, max: int) -> int:
    i = int(s)
    if min <= i <= max:
        return i
    else:
        raise ValueError


def parse_passport(passport: dict) -> dict:
    """Takes a dict with string values and gives them types"""
    try:
        passport["byr"] = parse_year(passport["byr"], 1920, 2002)
        passport["iyr"] = parse_year(passport["iyr"], 2010, 2020)
        passport["eyr"] = parse_year(passport["eyr"], 2020, 2030)
        hgt = re.compile("^([0-9]+)(cm|in)$").match(passport["hgt"])
        hcl = re.compile("^#[0-9a-f]{6}$").match(passport["hcl"])
        ecl = passport["ecl"]
        pid = re.compile("^[0-9]{9}$").match(passport["pid"])

        if ecl not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            raise ValueError("bad ecl")
        if hgt:
            value = int(hgt.group(1))
            unit = hgt.group(2)
            passport["hgt"] = (value, unit)
            if (unit == "cm" and not 150 <= value <= 193) or (
                unit == "in" and not 59 <= value <= 76
            ):
                raise ValueError("bad hgt")
        else:
            raise ValueError("invalid hgt")
        if hcl:
            passport["hcl"] = hcl.group(0)
        else:
            raise ValueError("invalid hcl")
        if pid:
            passport["pid"] = pid.group(0)
        else:
            raise ValueError("invalid pid")
        return passport
    except ValueError:
        return None


#
# Test data
#
assert sum(pass2dict(line) is not None for line in test_data1.split("\n\n")) == 2
assert all(parse_passport(pass2dict(line)) is None for line in test_data2.split("\n\n"))
assert all(
    parse_passport(pass2dict(line)) is not None for line in test_data3.split("\n\n")
)


s1 = sum(pass2dict(line) is not None for line in data.split("\n\n"))
ansA = s1
assert ansA == 233

dicted_passes = [pass2dict(line) for line in data.split("\n\n")]
passes_with_values = [p for p in dicted_passes if p is not None]
validation_results = [parse_passport(p) for p in passes_with_values]
valid_passes = [p for p in validation_results if p is not None]

ansB = len(valid_passes)
assert ansB < 112
assert ansB == 111
