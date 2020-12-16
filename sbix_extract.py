# https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6sbix.html
# requires fonttools lib (`pip install fonttools>=4.7.0`)
import sys
import os
from fontTools.ttLib import TTFont

folder = ".".join(sys.argv[1].split(".")[:-1])
if os.path.exists(folder):
    print("Folder already exists!")
    sys.exit(1)
os.mkdir(folder)

font = TTFont(sys.argv[1])
sbix = font["sbix"]

max_ppem = max(sbix.strikes.keys())
strike = sbix.strikes[max_ppem]

for bitmap in strike.glyphs.values():
    #print(bitmap.graphicType)
    if bitmap.graphicType == "emjc":
        filename = f"glyph-{bitmap.glyphName}.emjc"
        with open(folder + "/" + filename, "wb") as f:
            f.write(bitmap.imageData)
