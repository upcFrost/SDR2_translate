#coding=utf8

import rpErrorHandler
from Tkinter import *
from Sprite import *
from Common import * 
from Voice import *

class Scene():
    def __init__(self,
        file_id    = -1,
        speaker    = '',
        speaking   = False,
        sprite     = '',
        voice      = VoiceId(),
        bgm        = -1,
        headshot   = -1,
        mode       = None,
        special    = None,
        format     = None,
        box_color  = BOX_COLORS.yellow,
        box_type   = BOX_TYPES.normal,
        ammo       = -1,
        present    = -1,
        bgd        = -1,
        cutin      = -1,
        flash      = [],
        movie      = -1,
        img_filter = None,
        chapter    = -1,
        scene      = -1,
        room       = -1,
        extra_val  = -1,
        goto_ch    = -1,
        goto_scene = -1,
        goto_room  = -1,
        text       = '',
        text_idx   = -1,
        text_img   = '',
        text_clt   = False,
    ):
        # File ID
        self.file_id    = file_id
        self.chapter    = chapter
        # Info about scene
        self.scene      = scene
        self.room       = room
        # Info about speacking char
        self.speaker    = speaker
        self.speaking   = speaking
        self.sprite     = sprite
        self.voice      = voice
        self.bgm        = bgm
        self.headshot   = headshot
        self.mode       = mode
        self.special    = special
        self.format     = format
        # Text box
        self.box_color  = box_color
        self.box_type   = box_type
        self.text       = text
        self.text_idx   = text_idx
        self.text_img   = text_img
        self.text_clt   = text_clt
        # Current status
        self.ammo       = ammo
        self.present    = present
        # Scene graphics
        self.bgd        = bgd
        self.cutin      = cutin
        self.flash      = flash
        self.movie      = movie
        self.img_filter = img_filter
        # Any extra values
        self.extra_val  = extra_val