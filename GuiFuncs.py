import os, ConfigParser, PIL
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PakFile import *
from GimFile import *
from Common import *
from clt import *

def showSprite(self, GameDataLoc, pars):
    fn = os.path.join(GameDataLoc,'all','cg', 'bustup_%02d_%02d.gim' % (pars[1][1], pars[2][1]))
    GimImage = GimFile()
    GimImage.openGim(fn)
    GimImage.getImage()
    pilImage = PIL.Image.new("RGBA", (GimImage.width, GimImage.height))
    pilImage.putdata(GimImage.image)
    self.scene.sprite = ImageTk.PhotoImage(pilImage)
    POS_X = (2*SCREEN_W - GimImage.width)/2
    POS_Y = (2*SCREEN_H - GimImage.height)/2
    imagesprite = self._ScreenView.create_image(POS_X,POS_Y,image=self.scene.sprite, tag = 'sprite')
    pass

def showBGD(self, GameDataLoc, pars):
    fn = os.path.join(GameDataLoc,'all','cg', 'bgd_%03d.gim' % (pars[0][1]))
    # Show image
    if (pars[1][1] == 1):
        GimImage = GimFile()
        GimImage.openGim(fn)
        GimImage.getImage()
        pilImage = PIL.Image.new("RGBA", (GimImage.width, GimImage.height))
        pilImage.putdata(GimImage.image)
        self.scene.bgd = ImageTk.PhotoImage(pilImage)
        POS_X = (2*SCREEN_W - GimImage.width)/2
        POS_Y = (2*SCREEN_H - GimImage.height)/2
        imagebgd = self._ScreenView.create_image(POS_X,POS_Y,image=self.scene.bgd, tag = 'bgd')
    else:
        self.scene.bgd = [];
        self._ScreenView.delete('bgd')
    pass
    
def showFlash(self, GameDataLoc, pars):
    # Flash types:
    #   If id <  1000, then it's a flash event.
    #   if id >= 1000, then it's ammo
    #   if id >= 1500, then it's an ammo update
    #   if id >= 2000, then it's a present
    #   If id >= 3000, it's a cutin.
    
    id = pars[0][1]         # Flash ID
    added_Y = SCREEN_H/2    # Additional display height
    readfile = True         # Flag that we're reading file, not dataarray
    # Check if that really is a flash
    if id >= 3000:
        # Cutin
        root = os.path.join(GameDataLoc,'all','cg','cutin')
        fn_tmp = 'cutin_ico_%03d.gim'
        id = id - 3000

    elif id >= 2000:
        # Present
        root = os.path.join(GameDataLoc,'all','cg','present')
        fn_tmp = 'present_ico_%03d.gim'
        id = id - 2000

    elif id >= 1500:
        # Ammo
        root = os.path.join(GameDataLoc,'all','cg','kotodama')
        fn_tmp = 'kotodama_ico_%03d.gim'
        id = id - 1500

    elif id >= 1000:
        # Also ammo
        root = os.path.join(GameDataLoc,'all','cg','kotodama')
        fn_tmp = 'kotodama_ico_%03d.gim'
        id = id - 1000

    # A flash event.
    else:
        added_Y = 0 # Don't need an additional height here
        root = os.path.join(GameDataLoc,'all','flash')
        fn_tmp = 'fla_%03d.pak'
        file = os.path.join(root, fn_tmp % id)
        # Check dir because we have 2 of those
        if not os.path.isfile(file):
            root = os.path.join(GameDataLoc,'jp','flash')
    
    file = os.path.join(root, fn_tmp % id)
    # Check for file
    if not os.path.isfile(file):
        return -1
        
    # Get extension
    _, ext = os.path.splitext(file)
    if ext not in ['.pak', '.gmo', '.gim']:
        return -1
    
    if ext == '.pak':
        Pak = PakFile(file)
        Pak.getFiles()
        # FIXME: need to check its number
        idx = pars[-1][1]
        if idx == 255:
            # Erase everything from the screen
            self._ScreenView.delete(ALL)
            self.scene.flash = []
            return 0
        # Else - check for image, numeration starts with 1
        # Note that i'm using the SAME variable for unification
        file = Pak.files[idx - 1][1]
        _, ext = os.path.splitext(Pak.files[idx - 1][0])
        # Set flag that we're reading data
        readfile = False
        # Check extension
        if ext not in ['.gmo', '.gim']:
            return -1
        
    if ext == '.gmo':
        GmoImage = GmoFile()
        if readfile:
            GmoImage.openGmo(file)
        else:
            GmoImage.fromData(file)
        GmoImage.extractGim()
        GimImage = GmoImage.gim
        
    if ext == '.gim':
        GimImage = GimFile()
        if readfile:
            GimImage.openGim(file)
        else:
            GimImage.fromData(file)
    
    # Now working with gim image
    GimImage.getImage()
    pilImage = PIL.Image.new("RGBA", (GimImage.width, GimImage.height))
    pilImage.putdata(GimImage.image)
    self.scene.flash.append(ImageTk.PhotoImage(pilImage))
    POS_X = (2*SCREEN_W - GimImage.width)/2
    POS_Y = (2*SCREEN_H - GimImage.height)/2 - added_Y
    imagesprite = self._ScreenView.create_image(POS_X,POS_Y,image=self.scene.flash[-1])
    # Text should be kept on the top
    self._ScreenView.tag_raise('text')
    return 0

def printLine(self):
    # First delete the old line
    try:
        self._ScreenView.delete(self.scene.text_idx)
    except:
        print "No old line present on the screen"
    # I'm using images here because of the following things: positioning, alpha and font
    pilImage = PIL.Image.new("RGBA", (SCREEN_W, TEXT_H), (32,32,32,192))
    draw = PIL.ImageDraw.Draw(pilImage)
    font = PIL.ImageFont.truetype("rounded-mgenplus-2pp-regular.ttf", 20)
    # First  - draw the speaker name at (20,0)
    draw.text((20,0), self.scene.speaker, (255,255,255), font=font)
    # Default highlighting
    clt = 0
    color = CLT_STYLES[clt].top_color
    # Regex for finding highlighted regions
    clt_marker = re.compile(r"\<CLT (\d+)\>(.*?)\<CLT\>", re.DOTALL)
    clt_counter = 0
    # The text is split into a list like [CLT0_TEXT, CLT_NUM, CLT_TEXT, CLT0_TEXT]
    text = re.split(clt_marker, self.scene.text)
    # Draw lines with the fixed line spacing
    attSpacing = 20
    x = 20 # Margin
    y = 20  # Initial y
    partNum = 0
    for part in text:
        # Reset text color
        if partNum % 3 == 0:
            clt = 0
            color = CLT_STYLES[clt].top_color
        # Every first out of 3 - CLT number (look at the list form once again)
        if partNum % 3 == 1:
            clt = int(part)
            color = CLT_STYLES[clt].top_color
        # Dealing with a string
        else:
            # Draw text with the color we need
            for line in part.splitlines():
                draw.text( (x,y), line, color, font=font)
                y = y + attSpacing
        # Next part
        partNum += 1
    # Draw the text on canvas
    self.scene.text_img = ImageTk.PhotoImage(pilImage)
    self.scene.text_idx = self._ScreenView.create_image(SCREEN_W/2, SCREEN_H - TEXT_H/2,image=self.scene.text_img, tag = 'text')
    pass    