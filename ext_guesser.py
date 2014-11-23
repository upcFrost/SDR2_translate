################################################################################
### Copyright © 2012-2013 BlackDragonHunt
### 
### This file is part of the Super Duper Script Editor.
### 
### The Super Duper Script Editor is free software: you can redistribute it
### and/or modify it under the terms of the GNU General Public License as
### published by the Free Software Foundation, either version 3 of the License,
### or (at your option) any later version.
### 
### The Super Duper Script Editor is distributed in the hope that it will be
### useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
### 
### You should have received a copy of the GNU General Public License
### along with the Super Duper Script Editor.
### If not, see <http://www.gnu.org/licenses/>.
################################################################################

import os

EXTENSION_MAP = {
  'MIG.00.1PSP':          ".gim",
  'LLFS':                 ".sfl",
  'RIFF':                 ".at3",
  'OMG.00.1PSP':          ".gmo",
  '\x89\x50\x4E\x47':     ".png",
  'BM':                   ".bmp",
  'VAGp':                 ".vag",
  'tFpS':                 ".font",
  '\x41\x46\x53\x32':     ".awb",
  '\xff\xfe':             ".txt",
#  ConstBitStream(hex = '0x7000':         ".scp.wrd",
  '\xF0\x30\x60\x90\x02\x00\x00\x00\x0C\x00\x00\x00': ".p3d",
}

##################################################
### 
##################################################
def guess_ext(data, file_start = 0, file_end = 0):
  
  extension = None
  
  file_len = file_end - file_start
  
  for magic in EXTENSION_MAP.keys():
    if file_len < len(magic):
      continue
    
    if data[file_start : file_start + len(magic)] == magic:
      extension = EXTENSION_MAP[magic]
      break
  
  return extension

### EOF ###