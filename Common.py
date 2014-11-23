#coding=utf8

import rpErrorHandler
from Tkinter import *

from enum import Enum

SCREEN_W = 480
SCREEN_H = 272

TEXT_H = 90

SCENE_MODES   = Enum("normal", "normal_flat", "trial", "rules", "ammo", "ammoname", "ammosummary", "present", "presentname", "debate", "mtb", "climax", "anagram", "dive", "hanron", "menu", "map", "report", "report2", "skill", "skill2", "music", "eventname", "artworkname", "moviename", "theatre", "novel", "help", "other")
SCENE_SPECIAL = Enum("option", "showopt", "react", "debate", "chatter", "hanron", "checkobj", "checkchar")
BOX_COLORS    = Enum("yellow", "green", "blue")
BOX_TYPES     = Enum("normal", "flat", "novel")

CHAPTER_MONOKUMA = 100
CHAPTER_FREETIME = 101
CHAPTER_ISLAND   = 102
CHAPTER_NOVEL    = 103