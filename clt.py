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

import array

DEFAULT_COLOR   = (255, 255, 255)
DEFAULT_BORDER  = (0, 0, 0)

def get_rgba(color):
  # Alpha is always 255, at least in this game
  return (color[0], color[1], color[2], 255)

class CLTStyle:
  def __init__(self, font = 1, scale = 100, x_shift = 0.0, y_shift = 0.0,
               top_color = None, bottom_color = None, border_size = 0,
               border_color = None):
    self.font         = font
    self.scale        = scale
    self.x_shift      = x_shift
    self.y_shift      = y_shift
    self.top_color    = top_color if top_color else DEFAULT_COLOR
    self.bottom_color = bottom_color
    self.border_size  = border_size
    self.border_color = border_color
  
  def to_bin(self):
    font          = self.font * 0x10
    has_border    = self.border_size
    show_color    = 1 if (self.top_color and self.bottom_color) or has_border else 0
    scale         = self.scale
    top_color     = get_rgba(self.top_color) if self.top_color else get_rgba(DEFAULT_COLOR)
    bottom_color  = get_rgba(self.bottom_color) if self.bottom_color else top_color
    border_color  = get_rgba(self.border_color) if self.border_color else get_rgba(DEFAULT_BORDER)
    
#    data = bitstring.pack("uint:8, uint:8, uint:8, uint:8", font, has_border, show_color, scale) + \
#           bitstring.pack("uint:8, uint:8, uint:8, uint:8", *top_color) + \
#           bitstring.pack("uint:8, uint:8, uint:8, uint:8", *bottom_color) + \
#           bitstring.pack("uint:8, uint:8, uint:8, uint:8", *border_color)

    data = array.array('B', [font, has_border, show_color, scale] + list(top_color) + list(bottom_color) + list(border_color))

    return data

CLT_ORIGINAL = {
   0: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
   1: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (180, 90, 240)),
   2: CLTStyle(font = 1, scale = 100, top_color = (205, 135, 255),   bottom_color = None,             border_size = 1, border_color = (100, 25, 155)),
   3: CLTStyle(font = 1, scale = 100, top_color = (255, 230, 0),     bottom_color = None,             border_size = 1, border_color = (180, 100, 15)),
   4: CLTStyle(font = 1, scale = 100, top_color = (102, 230, 255),   bottom_color = None,             border_size = 0, border_color = None),
   5: CLTStyle(font = 1, scale = 100, top_color = (73, 73, 73),      bottom_color = None,             border_size = 0, border_color = None),
   6: CLTStyle(font = 1, scale = 100, top_color = (100, 255, 60),    bottom_color = None,             border_size = 0, border_color = None),
   7: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
   8: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
   9: CLTStyle(font = 1, scale = 128, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  10: CLTStyle(font = 1, scale = 100, top_color = (255, 0, 0),       bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  11: CLTStyle(font = 1, scale = 171, top_color = (255, 0, 0),       bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  12: CLTStyle(font = 2, scale =  58, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  13: CLTStyle(font = 2, scale =  58, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  14: CLTStyle(font = 2, scale =  58, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  15: CLTStyle(font = 2, scale =  58, top_color = (78, 78, 78),      bottom_color = None,             border_size = 0, border_color = None),
  16: CLTStyle(font = 2, scale =  75, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  17: CLTStyle(font = 2, scale = 100, top_color = (255, 240, 0),     bottom_color = (255, 115, 0),    border_size = 1, border_color = (0, 0, 0)),
  18: CLTStyle(font = 2, scale = 100, top_color = (150, 255, 100),   bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  19: CLTStyle(font = 2, scale = 100, top_color = (255, 0, 0),       bottom_color = (255, 64, 0),     border_size = 1, border_color = (0, 0, 0)),
  20: CLTStyle(font = 2, scale = 100, top_color = (255, 80, 255),    bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  21: CLTStyle(font = 2, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (190, 50, 10)),
  22: CLTStyle(font = 2, scale = 100, top_color = (255, 255, 255),   bottom_color = (205, 255, 0),    border_size = 1, border_color = (0, 0, 0)),
  23: CLTStyle(font = 1, scale =  85, top_color = (102, 230, 255),   bottom_color = None,             border_size = 1, border_color = (35, 110, 255)),
  24: CLTStyle(font = 1, scale =  85, top_color = (102, 230, 255),   bottom_color = None,             border_size = 0, border_color = None),
  25: CLTStyle(font = 2, scale =  75, top_color = (30, 250, 190),    bottom_color = (255, 255, 255),  border_size = 1, border_color = (0, 0, 0)),
  26: CLTStyle(font = 2, scale =  75, top_color = (250, 130, 80),    bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  27: CLTStyle(font = 2, scale =  75, top_color = (255, 0, 0),       bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  28: CLTStyle(font = 2, scale = 100, top_color = (255, 240, 0),     bottom_color = (255, 0, 0),      border_size = 1, border_color = (0, 0, 0)),
  29: CLTStyle(font = 2, scale = 100, top_color = (255, 115, 0),     bottom_color = (255, 0, 0),      border_size = 1, border_color = (0, 0, 0)),
  30: CLTStyle(font = 1, scale =  85, top_color = (0, 0, 0),         bottom_color = None,             border_size = 0, border_color = None),
  31: CLTStyle(font = 1, scale =  78, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  32: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  33: CLTStyle(font = 1, scale =  78, top_color = (255, 128, 128),   bottom_color = None,             border_size = 0, border_color = None),
  34: CLTStyle(font = 1, scale =  78, top_color = (128, 212, 255),   bottom_color = None,             border_size = 0, border_color = None),
  35: CLTStyle(font = 1, scale =  78, top_color = (0, 0, 0),         bottom_color = None,             border_size = 0, border_color = None),
  36: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  37: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  38: CLTStyle(font = 2, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  39: CLTStyle(font = 2, scale =  58, top_color = None,              bottom_color = None,             border_size = 1, border_color = (7, 105, 140)),
  40: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  41: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  42: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  43: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  44: CLTStyle(font = 2, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (255, 255, 0)),
  45: CLTStyle(font = 1, scale = 100, top_color = (50, 50, 50),      bottom_color = None,             border_size = 0, border_color = None),
  46: CLTStyle(font = 1, scale =  85, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  47: CLTStyle(font = 1, scale =  78, top_color = (80, 80, 80),      bottom_color = None,             border_size = 0, border_color = None),
  48: CLTStyle(font = 1, scale =  85, top_color = (107, 107, 107),   bottom_color = None,             border_size = 0, border_color = None),
  49: CLTStyle(font = 1, scale =  85, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  50: CLTStyle(font = 1, scale =  78, top_color = (107, 107, 107),   bottom_color = None,             border_size = 0, border_color = None),
  51: CLTStyle(font = 1, scale =  78, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  52: CLTStyle(font = 1, scale =  85, top_color = (107, 107, 107),   bottom_color = None,             border_size = 0, border_color = None),
  53: CLTStyle(font = 1, scale =  85, top_color = (0, 0, 0),         bottom_color = None,             border_size = 0, border_color = None),
  54: CLTStyle(font = 1, scale =  78, top_color = (50, 50, 50),      bottom_color = None,             border_size = 0, border_color = None),
  55: CLTStyle(font = 1, scale =  92, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  56: CLTStyle(font = 1, scale =  92, top_color = (50, 50, 50),      bottom_color = None,             border_size = 0, border_color = None),
  57: CLTStyle(font = 1, scale =  78, top_color = (107, 107, 107),   bottom_color = None,             border_size = 0, border_color = None),
  58: CLTStyle(font = 1, scale =  78, top_color = (0, 0, 0),         bottom_color = None,             border_size = 0, border_color = None),
  59: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  60: CLTStyle(font = 1, scale = 171, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  61: CLTStyle(font = 1, scale = 100, top_color = (255, 240, 0),     bottom_color = (255, 115, 0),    border_size = 1, border_color = (0, 0, 0)),
  62: CLTStyle(font = 1, scale =  57, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  63: CLTStyle(font = 1, scale = 142, top_color = (255, 128, 255),   bottom_color = None,             border_size = 1, border_color = (128, 64, 128)),
  64: CLTStyle(font = 1, scale = 114, top_color = (255, 128, 255),   bottom_color = None,             border_size = 1, border_color = (128, 64, 128)),
  65: CLTStyle(font = 2, scale =  66, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  66: CLTStyle(font = 2, scale =  66, top_color = (255, 255, 255),   bottom_color = (255, 208, 128),  border_size = 1, border_color = (160, 32, 0)),
  67: CLTStyle(font = 2, scale =  66, top_color = (255, 255, 255),   bottom_color = (128, 208, 255),  border_size = 1, border_color = (0, 32, 160)),
  68: CLTStyle(font = 2, scale =  66, top_color = (255, 255, 255),   bottom_color = (255, 255, 128),  border_size = 1, border_color = (160, 160, 32)),
  69: CLTStyle(font = 2, scale = 100, top_color = (50, 205, 255),    bottom_color = (0, 110, 190),    border_size = 1, border_color = (0, 0, 0)),
  70: CLTStyle(font = 2, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 160, 252)),
  71: CLTStyle(font = 2, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (255, 80, 0)),
  72: CLTStyle(font = 2, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (10, 255, 0)),
  73: CLTStyle(font = 2, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (210, 50, 255)),
  74: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  75: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  76: CLTStyle(font = 1, scale = 100, top_color = (0, 0, 0),         bottom_color = None,             border_size = 0, border_color = None),
  77: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (180, 90, 240)),
  78: CLTStyle(font = 1, scale = 100, top_color = (205, 135, 255),   bottom_color = None,             border_size = 1, border_color = (100, 25, 155)),
  79: CLTStyle(font = 1, scale = 100, top_color = (204, 150, 0),     bottom_color = None,             border_size = 1, border_color = (255, 230, 0)),
  80: CLTStyle(font = 1, scale = 100, top_color = (51, 115, 128),    bottom_color = None,             border_size = 0, border_color = None),
  81: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  82: CLTStyle(font = 1, scale = 100, top_color = (50, 128, 30),     bottom_color = None,             border_size = 0, border_color = None),
  83: CLTStyle(font = 1, scale =  78, top_color = (128, 38, 53),     bottom_color = None,             border_size = 0, border_color = None),
  84: CLTStyle(font = 1, scale =  78, top_color = (102, 102, 102),   bottom_color = None,             border_size = 0, border_color = None),
  85: CLTStyle(font = 2, scale = 100, top_color = None,              bottom_color = None,             border_size = 1, border_color = (0, 0, 0)),
  86: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  87: CLTStyle(font = 1, scale = 100, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  88: CLTStyle(font = 1, scale =  85, top_color = (0, 0, 0),         bottom_color = None,             border_size = 0, border_color = None),
  89: CLTStyle(font = 1, scale =  85, top_color = (102, 102, 102),   bottom_color = None,             border_size = 0, border_color = None),
  90: CLTStyle(font = 1, scale =  85, top_color = None,              bottom_color = None,             border_size = 0, border_color = None),
  91: CLTStyle(font = 1, scale =  85, top_color = None,              bottom_color = None,             border_size = 1, border_color = (180, 90, 240)),
}

MAX_CLT = max(CLT_ORIGINAL.keys())

CLT_STYLES = CLT_ORIGINAL.copy()
# Until I get the proper CLT editor implemented
CLT_STYLES[1]  = CLTStyle(font = 1, scale = 100, top_color = (100, 240, 165), bottom_color = None, border_color = None)
CLT_STYLES[2]  = CLTStyle(font = 2, scale =  75, top_color = (255, 255, 255), bottom_color = (205, 255, 0), border_color = None)
CLT_STYLES[7]  = CLTStyle(font = 2, scale =  75, top_color = (102, 230, 255), bottom_color = None, border_size = 1, border_color = (0, 0, 0))
CLT_STYLES[32] = CLTStyle(font = 2, scale =  75, top_color = None, bottom_color = None, border_size = 1, border_color = (190, 50, 10))
CLT_STYLES[36] = CLTStyle(font = 2, scale =  75, top_color = (100, 240, 165), bottom_color = None, border_size = 1, border_color = (0, 0, 0))

# Temp list of styles we can definitely overwrite.
# CLT_STYLES[37] = CLTStyle(font = 1, scale = 100, top_color = None, bottom_color = None, border_size = 0, border_color = None)
# CLT_STYLES[40] = CLTStyle(font = 1, scale = 100, top_color = None, bottom_color = None, border_size = 0, border_color = None)
# CLT_STYLES[41] = CLTStyle(font = 1, scale = 100, top_color = None, bottom_color = None, border_size = 0, border_color = None)
# CLT_STYLES[42] = CLTStyle(font = 1, scale = 100, top_color = None, bottom_color = None, border_size = 0, border_color = None)
# CLT_STYLES[43] = CLTStyle(font = 1, scale = 100, top_color = None, bottom_color = None, border_size = 0, border_color = None)
# CLT_STYLES[59] = CLTStyle(font = 1, scale = 100, top_color = None, bottom_color = None, border_size = 0, border_color = None)
# CLT_STYLES[81] = CLTStyle(font = 1, scale = 100, top_color = None, bottom_color = None, border_size = 0, border_color = None)
# CLT_STYLES[86] = CLTStyle(font = 1, scale = 100, top_color = None, bottom_color = None, border_size = 0, border_color = None)
# CLT_STYLES[87] = CLTStyle(font = 1, scale = 100, top_color = None, bottom_color = None, border_size = 0, border_color = None)

if __name__ == "__main__":
  for clt in sorted(CLT_STYLES.keys()):
    style = CLT_STYLES[clt]
    print style.to_bin()

### EOF ###
