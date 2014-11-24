import os
from PakFile import *

def getCharNames(ROOT_DIR):
    # All char names are stored in a single fixed .pak file
    Pak = PakFile(os.path.join(ROOT_DIR,'jp','script','32_CharaName.pak'))
    Pak.getFiles()
    out = []
    for f in Pak.files:
        if '.txt' in f[0]:
            out.append(f[1][:-2].decode('utf16'))
    return out
