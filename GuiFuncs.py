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
    
def showFlash(self, GameDataLoc, pars):
    root = GameDataLoc + 'all/flash/'
    if not os.path.isfile(root + 'fla_%03d.pak' % pars[0][1]):
        root = GameDataLoc + 'jp/flash/'
    try:
        Pak = PakFile(root + 'fla_%03d.pak' % pars[0][1])
        Pak.getFiles()
    except:
        # If there's no such file
        Pak = PakFile(root + 'fla_%03d.pak' % 999)
        Pak.getFiles()
    # FIXME: need to check its number
    idx = pars[-1][1]
    if idx == 255:
        # Erase everything from the screen
        self._ScreenView.delete(ALL)
        self.scene.flash = []
        return 0
    # Else - check for image, numeration starts with 1
    imageFile = Pak.files[idx - 1]
    if '.gmo' in imageFile[0]:
        GmoImage = GmoFile()
        GmoImage.fromData(imageFile[1])
        GmoImage.extractGim()
        GmoImage.gim.getImage()
        image = GmoImage.gim.image
        pilImage = PIL.Image.new("RGBA", (GmoImage.gim.width, GmoImage.gim.height))
        pilImage.putdata(GmoImage.gim.image)
        self.scene.flash.append(ImageTk.PhotoImage(pilImage))
        POS_X = (2*SCREEN_W - GmoImage.gim.width)/2
        POS_Y = (2*SCREEN_H - GmoImage.gim.height)/2
        imagesprite = self._ScreenView.create_image(POS_X,POS_Y,image=self.scene.flash[-1])
        return 0
    if '.gim' in imageFile[0]:
        GimImage = GimFile()
        GimImage.fromData(imageFile[1])
        GimImage.getImage()
        pilImage = PIL.Image.new("RGBA", (GimImage.width, GimImage.height))
        pilImage.putdata(GimImage.image)
        self.scene.flash.append(ImageTk.PhotoImage(pilImage))
        POS_X = (2*SCREEN_W - GimImage.width)/2
        POS_Y = (2*SCREEN_H - GimImage.height)/2
        imagesprite = self._ScreenView.create_image(POS_X,POS_Y,image=self.scene.flash[-1])
        # Text should be kept on the top
        self._ScreenView.tag_raise('text')
        return 0
    # If neither gim nor gmo - i don't know how to use sfl files yet
    imagesprite = self._ScreenView.create_text(SCREEN_W/2, SCREEN_H/2, text="FLASH ANIMATION STUB")
    return -1
    pass

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