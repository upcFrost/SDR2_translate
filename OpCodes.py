#coding=utf8

################################################################################
### Copyright © 2012-2013 BlackDragonHunt
### Copyright © 2012-2013 /a/nonymous scanlations
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

import rpErrorHandler
from Tkinter import *

CMD_MARKER = 0x70

WRD_HEADER          = 0x00
# ???                 = 0x01
WRD_GET_LINE_IDX    = 0x02
WRD_CLT             = 0x03
WRD_FILTER_IMG      = 0x04
WRD_MOVIE           = 0x05
WRD_FLASH           = 0x06
# ???                 = 0x07
WRD_VOICE           = 0x08
WRD_BGM             = 0x09
WRD_SFX_A           = 0x0A
WRD_SFX_B           = 0x0B
WRD_SET_AMMO        = 0x0C
# ???                 = 0x0D
# ???                 = 0x0E
WRD_CHAR_TITLE      = 0x0F

WRD_REPORT_INFO     = 0x10
# ???                 = 0x11
# ???                 = 0x12
# ???                 = 0x13
WRD_TRIAL_CAM       = 0x14
WRD_LOAD_MAP        = 0x15
# ???                 = 0x16
WRD_GOTO_SCRIPT     = 0x19
# ???                 = 0x1A
WRD_CALL_SCRIPT     = 0x1B
# ???                 = 0x1C
# ???                 = 0x1D
WRD_SPRITE          = 0x1E
WRD_BLINK           = 0x1F

# ???                 = 0x20
WRD_SPEAKER         = 0x21
# ???                 = 0x22
# ???                 = 0x23
# ???                 = 0x24
WRD_CHANGE_UI       = 0x25
WRD_SET_FLAG        = 0x26
WRD_CHECK_CHAR      = 0x27
# ???                 = 0x28
# ???                 = 0x29
# ???                 = 0x2A
WRD_CHECK_OBJ       = 0x2B
WRD_SET_LABEL       = 0x2C
# ???                 = 0x2D
# ???                 = 0x2E
# ???                 = 0x2F

# ???                 = 0x30
WRD_NVL_NEW_PAGE    = 0x31
WRD_CHOICE          = 0x32
# ???                 = 0x34
# ???                 = 0x35
WRD_BGD             = 0x37
# ???                 = 0x3A
WRD_GOTO_LABEL      = 0x3B
# ???                 = 0x3D
# ???                 = 0x3E

WRD_CHECKFLAG_A     = 0x46
WRD_CHECKFLAG_B     = 0x47
# ???                 = 0x48
# ???                 = 0x49
# ???                 = 0x4A
WRD_WAIT_INPUT      = 0x4B
WRD_PRINT_LINE      = 0x4C
WRD_FLAG_CHECK_END  = 0x4D

# ???                 = 0x64

WRD_INVALID         = 0xFF

OP_PARAMS = {

  WRD_HEADER:         [("lines", "H", 2)],
  0x01:               [(None, "B", 1)] * 4,
  WRD_GET_LINE_IDX:   [("line",  ">H", 2)],
  WRD_CLT:            [("clt", "B", 1)], # Something to do with CLT'd text
  WRD_FILTER_IMG:     [("unk1", "B", 1), ("filter", "B", 1), ("unk2", ">H", 2)],
  WRD_MOVIE:          [("id", "B", 1), ("state", "B", 1), ],
  WRD_FLASH:          [("id", ">H", 2), ("padding", "I", 4), ("unk", "B", 1), ("state", "B", 1)],
  0x07:               [(None, "B", 1)] * 5,
  WRD_VOICE:          [("char_id", "B", 1), ("chapter", "B", 1), ("voice_id", ">H", 2), ("unk", "B", 1)],
  WRD_BGM:            [("id", "B", 1), ("transition", "B", 1), ("unk", "B", 1)],
  WRD_SFX_A:          [("id", ">H", 2), ("volume", "B", 1)],
  WRD_SFX_B:          [("id", "B", 1), ("volume", "B", 1)],
  WRD_SET_AMMO:       [("id", "B", 1), ("state", "B", 1)],
  0x0D:               [(None, "B", 1)] * 3, # Something to do with presents
  0x0E:               [(None, "B", 1)] * 2,
  WRD_CHAR_TITLE:     [("id", "B", 1), ("unk", "B", 1), ("title", "B", 1)],
  WRD_REPORT_INFO:    [("id", "B", 1), ("unk", "B", 1), ("info_known", "B", 1)],
  0x11:               [(None, "B", 1)] * 4, # Something to do with multiple-choice
  0x12:               [(None, "B", 1)] * 2,
  0x13:               [(None, "B", 1)] * 2,
  WRD_TRIAL_CAM:      [("char_id", "B", 1), ("unk1", "B", 1), ("motion", "B", 1), ("unk2", "B", 1), ("unk3", "B", 1), ("unk4", "B", 1)],
  WRD_LOAD_MAP:       [("room", ">H", 2), ("state", "B", 1), ("padding", "B", 1)],
  0x16:               [(None, "B", 1)] * 2,
  WRD_GOTO_SCRIPT:    [("chapter", "B", 1), ("scene", ">H", 2), ("room", ">H", 2)],
  0x1A:               [], # Cleanup?
  WRD_CALL_SCRIPT:    [("chapter", "B", 1), ("scene", ">H", 2), ("room", ">H", 2)],
  0x1C:               [], # Return to calling script?
  0x1D:               [(None, "B", 1)] * 1,
  WRD_SPRITE:         [("obj_id", "B", 1), ("char_id", "B", 1), ("sprite_id", "B", 1), ("sprite_state", "B", 1), ("sprite_type", "B", 1)],
  WRD_BLINK:           [(None, "B", 1)] * 7, # Screen flash effect?
  0x20:               [(None, "B", 1)] * 5,
  WRD_SPEAKER:        [("id", "B", 1)],
  0x22:               [(None, "B", 1)] * 3,
  0x23:               [(None, "B", 1)] * 5,
  0x24:               [(None, "B", 1)] * 4, 
  WRD_CHANGE_UI:      [("element", "B", 1), ("state", "B", 1)],
  WRD_SET_FLAG:       [("group", "B", 1), ("id", "B", 1), ("state", "B", 1)],
  WRD_CHECK_CHAR:     [("id", "B", 1)],
  0x28:               [(None, "B", 1)] * 4,
  0x29:               [(None, "B", 1)] * 13,
  0x2A:               [(None, "B", 1)] * 12,
  WRD_CHECK_OBJ:      [("id", "B", 1)],
  WRD_SET_LABEL:      [("id", ">H", 2)],
  0x2D:               [(None, "B", 1)] * 12,
  0x2E:               [(None, "B", 1)] * 5,
  0x2F:               [(None, "B", 1)] * 2,
  0x30:               [(None, "B", 1)] * 2,
  WRD_NVL_NEW_PAGE:   [], # New page in the IF story?
  WRD_CHOICE:         [("flag", "B", 1)],
  0x34:               [(None, "B", 1)] * 1, # Something in the IF story?
  0x35:               [(None, "B", 1)] * 2,
  WRD_BGD:            [("id", ">H", 2), ("state", "B", 1)],
  0x3A:               [(None, "B", 1)] * 4, # Set values checked by WRD_CHECKFLAG_B?
  WRD_GOTO_LABEL:     [("id", ">H", 2)],
  0x3D:               [(None, "B", 1)] * 5, # Full-screen distortion effect?
  0x3E:               [(None, "B", 1)] * 2,
  #WRD_CHECKFLAG_A:    "parse_checkflag_a",
  WRD_CHECKFLAG_A:    [],
  #WRD_CHECKFLAG_B:    "parse_checkflag_b",
  WRD_CHECKFLAG_B:    [],
  0x48:               [(None, "B", 1)] * 5,
  0x49:               [(None, "B", 1)] * 5,
  0x4A:               [(None, "B", 1)] * 5,
  WRD_WAIT_INPUT:     [],
  #WRD_PRINT_LINE:     "parse_wait_frame",
  WRD_PRINT_LINE:     [],
  WRD_FLAG_CHECK_END: [],
  0x64:               [],
  WRD_INVALID:        "byte",

}

OP_FUNCTIONS = {

  WRD_HEADER:         "header",
  0x01:               None,
  WRD_GET_LINE_IDX:   "get_line_idx",
  WRD_CLT:            "clt",
  WRD_FILTER_IMG:     "filter_img",
  WRD_MOVIE:          "play_movie",
  WRD_FLASH:          "show_flash",
  0x07:               None,
  WRD_VOICE:          "play_voice",
  WRD_BGM:            "play_bgm",
  WRD_SFX_A:          "play_sfx_a",
  WRD_SFX_B:          "play_sfx_b",
  WRD_SET_AMMO:       "set_ammo",
  0x0D:               None,               # Something to do with presents
  0x0E:               None,
  WRD_CHAR_TITLE:     "set_title",
  WRD_REPORT_INFO:    "set_report_info",
  0x11:               None,               # Something to do with multiple-choice
  0x12:               None,
  0x13:               None,
  WRD_TRIAL_CAM:      "trial_cam",
  WRD_LOAD_MAP:       "load_map",
  0x16:               None,
  WRD_GOTO_SCRIPT:    "goto_script",
  0x1A:               None,               # Cleanup?
  WRD_CALL_SCRIPT:    "call_script",
  0x1C:               None,               # Cleanup?
  0x1D:               None,
  WRD_SPRITE:         "show_sprite",
  WRD_BLINK:          "blink_screen",               # Screen flash effect?
  0x20:               None,
  WRD_SPEAKER:        "set_speaker",
  0x22:               None,
  0x23:               None,
  0x24:               None,
  WRD_CHANGE_UI:      "change_ui",
  WRD_SET_FLAG:       "set_flag",
  WRD_CHECK_CHAR:     "check_char",
  0x28:               None,
  0x29:               None,
  0x2A:               None,
  WRD_CHECK_OBJ:      "check_obj",
  WRD_SET_LABEL:      "set_label",
  0x2D:               None,
  0x2E:               None, 
  0x2F:               None,
  0x30:               None,
  WRD_NVL_NEW_PAGE:   "nvl_new_page",
  WRD_CHOICE:         "choice",
  0x34:               None,
  0x35:               None,
  WRD_BGD:            "show_bgd",
  0x3A:               None, 
  WRD_GOTO_LABEL:     "goto_label",
  0x3D:               None,
  0x3E:               None,
  WRD_CHECKFLAG_A:    "check_flag_a",
  WRD_CHECKFLAG_B:    "check_flag_b",
  0x48:               None,
  0x49:               None,
  0x4A:               None,
  WRD_WAIT_INPUT:     "wait_for_input",
  WRD_PRINT_LINE:     "print_line",
  WRD_FLAG_CHECK_END: "flag_check_end",
  0x64:               None,
  WRD_INVALID:        "byte",             # For anything that doesn't parse correctly
  
  # WRD_LOAD_MAP:       "load_map",

}

### EOF ###
