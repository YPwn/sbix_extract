# https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6sbix.html
# requires fonttools lib (`pip install fonttools>=4.7.0`)
# YPwn was here. 2020
import sys
import os
import shutil
import re
from fontTools.ttLib import TTFont

def convertGlyphName(name):
    skinMap = {
        '1': "1f3fb", '2': "1f3fc",
        '3': "1f3fd", '4': "1f3fe",
        '5': "1f3ff"
    }
    genderMap = {
        'W': "2640",
        'M': "2642"
    }

    isFlag = re.match(r"""^u1F1(E[6-9A-F]|F[0-9A-F])_"""
        r"""u1F1(E[6-9A-F]|F[0-9A-F])$""", name)
    isHoldingHands = re.match(r"""^u1F46[89]_u1F91D_u1F46[89]\."""
        r"""(11|22|33|44|55)$""", name)
    isFamily = re.match(r"^u1F46A\.[MW][BGMW][BG]{0,}[BG]{0,}$", name)
    isKissing = re.match(r"^u1F48F\.(MM|WM|WW)$", name)
    isInLove = re.match(r"^u1F491\.(MM|WM|WW)$", name)
    isExtraFlags = re.match(r"""^u1F3F4_uE0067_uE0062_uE00[67][357]_"""
        r"""uE006[3CE]_uE00[67][347]_uE007F$""", name)
    isHoldingHandsFemale = re.match(r"""^u1F9D1_u1F91D_u1F9D1\."""
        r"""[1-5][1-5]$""", name)
    isHoldingHandsExtra = re.match(r"^u1F9D1_u1F91D_u1F9D1\.66$", name)
    isDoubleSkin = re.match(r"^u[0-9A-F]{1,5}_u[0-9A-F]{1,5}\.[1-5]$", name)
    isDoubleZero = re.match(r"^u[0-9A-F]{1,5}_u[0-9A-F]{1,5}\.0$", name)
    isNumber = re.match(r"^u00(3[0-9]|2[3A])_u20E3$", name)
    isDouble = re.match(r"^u[0-9A-F]{1,5}_u[0-9A-F]{1,5}$", name)
    isSkinGender = re.match(r"^u[0-9A-F]{1,5}\.[1-5]\.[MW]$", name)
    isGender = re.match(r"^u[0-9A-F]{1,5}\.0\.[MW]$", name)
    isSingleSkin = re.match(r"^u[0-9A-F]{1,5}\.[0-5]$", name)
    isSingleGender = re.match(r"^u[0-9A-F]{1,5}\.[MW]$", name)
    isSingle = re.match(r"^u[0-9A-F]{1,5}$", name)

    if isFlag:
        if name == "u1F1F8_u1F1ED":
            return ["u1f1f8_1f1ed", "u1f1e6_1f1e8", "u1f1f9_1f1e6"]
        elif name == "u1F1F3_u1F1F4":
            return ["u1f1f3_1f1f4", "u1f1e7_1f1fb", "u1f1f8_1f1ef"]
        elif name == "u1F1EB_u1F1F7":
            return ["u1f1eb_1f1f7", "u1f1e8_1f1f5", "u1f1f2_1f1eb"]
        elif name == "u1F1EE_u1F1F4":
            return ["u1f1ee_1f1f4", "u1f1e9_1f1ec"]
        elif name == "u1F1EA_u1F1F8":
            return ["u1f1ea_1f1f8", "u1f1ea_1f1e6"]
        elif name == "u1F1E6_u1F1FA":
            return ["u1f1e6_1f1fa", "u1f1ed_1f1f2"]
        elif name == "u1F1FA_u1F1F8":
            return ["u1f1fa_1f1f8", "u1f1fa_1f1f2"]
        else:
            return name.replace("_u", "_").lower()
    elif isHoldingHands:
        prefix = ""
        if name[5] == '9' and name[19] == '8':
            prefix += "u1f46b_"
        elif name[5] == '8' and name[19] == '8':
            prefix += "u1f46c_"
        elif name[5] == '9' and name[19] == '9':
            prefix += "u1f46d_"
        return prefix + skinMap[name[21]]
    elif isFamily:
        members = name[7:]
        membersLen = len(members)
        memberMap = {
            'B': "1f466",
            'G': "1f467",
            'M': "1f468",
            'W': "1f469"
        }
        result = "u"
        for i in range(membersLen):
            result += memberMap[members[i]]
            if i != (membersLen-1):
                result += "_200d_"
        return result
    elif isKissing:
        memberMap = {
            "MM": "u1f468_200d_2764_200d_1f48b_200d_1f468",
            "WM": "u1f469_200d_2764_200d_1f48b_200d_1f468",
            "WW": "u1f469_200d_2764_200d_1f48b_200d_1f469"
        }
        return memberMap[name[7:]]
    elif isInLove:
        memberMap = {
            "MM": "u1f468_200d_2764_200d_1f468",
            "WM": "u1f469_200d_2764_200d_1f468",
            "WW": "u1f469_200d_2764_200d_1f469"
        }
        return memberMap[name[7:]]
    elif isExtraFlags:
        return name.replace("_u", "_").lower()
    elif isHoldingHandsFemale:
        return "u1f9d1_" + skinMap[name[21]] + \
            "_200d_1f91d_200d_1f9d1_" + \
            skinMap[name[22]]
    elif isHoldingHandsExtra:
        return "u1f9d1_200d_1f91d_200d_1f9d1"
    elif isDoubleSkin:
        result = name.split(".")
        codes = result[0].split("_")
        left = codes[0].lower()
        right = codes[1][1:].lower()
        return left + "_" + skinMap[result[1]] + \
            "_200d_" + right
    elif isDoubleZero:
        codes = name.split(".")[0].split("_")
        left = codes[0].lower()
        right = codes[1][1:].lower()
        return left + "_200d_" + right
    elif isNumber:
        codes = name.split("_")
        left = codes[0].lower()
        right = codes[1][1:].lower()
        return left + "_" + right
    elif isDouble:
        codes = name.split("_")
        left = codes[0].lower()
        right = codes[1][1:].lower()
        return left + "_200d_" + right
    elif isSkinGender:
        result = name.split(".")
        base = result[0].lower()
        skin = skinMap[result[1]]
        gender = genderMap[result[2]]
        return base + "_" + skin + "_200d_" + gender
    elif isGender:
        result = name.split(".")
        base = result[0].lower()
        gender = genderMap[result[2]]
        return base + "_200d_" + gender
    elif isSingleSkin:
        result = name.split(".")
        base = result[0].lower()
        if result[1] == '0':
            return base
        else:
            return base + "_" + skinMap[result[1]]
    elif isSingleGender:
        result = name.split(".")
        base = result[0].lower()
        return base + "_200d_" + genderMap[result[1]]
    elif isSingle:
        return name.lower()
    else:
        return None

def dumpEmjc(filename, data):
    with open(filename, "wb") as f:
        f.write(data)

folder = ".".join(sys.argv[1].split(".")[:-1])
if os.path.exists(folder):
    shutil.rmtree(folder)
os.mkdir(folder)
os.mkdir(folder + "/unknown")

font = TTFont(sys.argv[1])
sbix = font["sbix"]

max_ppem = max(sbix.strikes.keys())
strike = sbix.strikes[max_ppem]

for bitmap in strike.glyphs.values():
    if bitmap.graphicType == "emjc":
        converted = convertGlyphName(bitmap.glyphName)
        if converted is None:
            dumpEmjc(folder + "/unknown/" + bitmap.glyphName + \
                ".emjc", bitmap.imageData)
        elif isinstance(converted, list):
            for elem in converted:
                dumpEmjc(folder + "/emoji_" + elem + \
                    ".emjc", bitmap.imageData)
        else:
            dumpEmjc(folder + "/emoji_" + converted + \
                ".emjc", bitmap.imageData)
