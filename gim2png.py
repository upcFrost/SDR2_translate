#coding=utf8

from Tkinter import *
import os, struct, math
from PIL import Image

MIG_MAGIC = '\x4D\x49\x47'

class GmoFile():
    def __init__(self):
        self.fn = ''
        self.full = ''
        self.header = ''
        self.data = ''
        self.gim = GimFile()
    
    def openGmo(self, fn):
        self.fn = fn
        self.fp = open(self.fn, 'rb')
        # Go the the beginnipng
        self.fp.seek(0)
        # Get filesize
        self.fileSize = os.path.getsize(self.fn)
        # Read full file
        self.full = self.fp.read()
        # Reading header
        self.fp.seek(0)
        self.header = self.fp.read(128)
        self.data = self.fp.read()
        pass
    
    def fromData(self, data):
        self.full = data
        self.header = self.full[0:0x80]
        self.data = self.full[0x80:]
        pass
    
    def extractGim(self):
        try:
            offset = self.full.index(MIG_MAGIC)
            self.gim.fromData(self.full, offset)
        except:
            print 'No MIG found'
        pass

class GimFile():
    # Gim image format is pretty simple, The're 2 types: Direct and Inverted
    # - 128 byte for header
    # - Quantized image data (color number in palette)
    # - Palette in RGBA format
    # - Optional footer
    # Palette location is specified by the value of 
    #  0x35-0x36 byteword little-endian followed by D0 (?) for the inverted one
    # Palette size (num of color bits) is specified by 0x4C byte (2^n)
    # When resolving quantized data we should remember that for 4-bit palette
    #  each byte represents 2 image pixels
    # Optional footer should contain GimConv utility name
    def __init__(self):
        # Variables
        self.width = 0
        self.height = 0
        self.compressed = False
        self.full = ''
        self.header = ''
        self.footer = ''
        self.data = ''
        self.fileSize = ''
        self.fn = ''
        self.inverted = False
        self.image = []
        # Palette info
        self.palettePosition = ''
        self.paletteSize = 256
        self.palette = []
        pass
        
    def openGim(self, fn):
        self.fn = fn
        self.fp = open(self.fn, 'rb')
        # Go the the beginning
        self.fp.seek(0)
        # Get filesize
        self.fileSize = os.path.getsize(self.fn)
        # Read full file
        self.full = self.fp.read()
        # Reading header
        self.fp.seek(0)
        self.header = self.fp.read(128)
        self.data = self.fp.read()
        # Check image header
        self.checkHeader()
        self.checkFooter()
        # Check for compression
        if self.width*self.height > len(self.data):
            self.compressed = True
        pass
    
    def fromData(self, data, offset = 0):
        # Just using the given offset for the master file
        self.full = data[offset:]
        self.header = self.full[0:0x80]
        self.data = self.full[0x80:]
        # Check header and footer
        self.checkHeader()
        self.checkFooter()
        # Check for compression
        if self.width*self.height > len(self.data):
            self.compressed = True
        pass
    
    def checkHeader(self):
        # Read checksum - first 3 bytes
        checkSum = 0
        for i in xrange(3):
            checkSum += struct.unpack('B', self.header[i])[0]
        # It should be 221 (0x4D 0x49 0x47 -> MIG)
        if checkSum == 221:
            # [72:74] <- 74 is not included, so it's only 72 and 73
            self.width = struct.unpack('H', self.header[72:74])[0]
            self.height = struct.unpack('H', self.header[74:76])[0]
            # Check for inversion
            invByte = struct.unpack('B', self.header[0x30])[0]
            if invByte == 4:
                self.inverted = True
                # Get palette position
                bitDepth = struct.unpack('B', self.full[0x4C])[0]
                self.palettePosition = len(self.full) - (2 ** bitDepth)*4
                self.data = self.full[128:self.palettePosition]
            return True
        return False

    def checkFooter(self):
        try:
            # Try to find it
            self.full.index('GimConv')
            # Footer starts with 0xff 0x00 0x00 0x00
            footerStartIdx = self.full[::-1].index('\x00\x00\x00\xff') + 4
            self.palettePosition -= footerStartIdx
            self.data = self.full[128:self.palettePosition]
        except:
            # Ok, found nothing
            pass
        pass
        
    
    def getPalette(self):
        bitDepth = struct.unpack('B', self.full[0x4C])[0]
        self.paletteSize = 2 ** bitDepth
        # For 32 bits there's no color palette
        if bitDepth != 32:
            for i in xrange(self.paletteSize):
                # 4 Bytes for each color (RGBA)
                color = [None] * 4
                # Pallete position
                position = self.palettePosition + i*4
                color[0] = struct.unpack('B', self.full[position])[0]
                color[1] = struct.unpack('B', self.full[position + 1])[0]
                color[2] = struct.unpack('B', self.full[position + 2])[0]
                color[3] = struct.unpack('B', self.full[position + 3])[0]
                self.palette.append(tuple(color))
        else:
            pass
        pass
    
    def getImage(self):
        self.getPalette()
        self.image = [0] * self.width*self.height
        self.arrangeByteImage()  
        
        bitDepth = struct.unpack('B', self.full[0x4C])[0]
        byteSize = self.width*self.height * bitDepth/8
        byteHeight = self.height * 8 / bitDepth
        byteWidth = self.width * 8 / bitDepth
        color = [None] * 4
        
        if bitDepth == 32:
            # For 32 bits there's no color palette
            for i in xrange(byteSize):
                color[i%4] = struct.unpack('B', self.byteImage[i])[0]
                # Inverting alpha
                if i%4 == 3:
                    color[i%4] = 255 - color[i%4]
                # Dumping into the image
                if i%4 == 0 and i > 0:
                    self.image[i//4 - 1] = tuple(color)
                # For the last one
                if i == byteSize - 1:
                    self.image[-1] = tuple(color)
        else:
            for y in xrange(byteHeight):
                for x in xrange(byteWidth):
                    try:
                        # Calculate pixel position
                        blockWidth = 16
                        posByte = x + int(math.ceil(float(self.width)/blockWidth)*blockWidth)*y
                        pos = x + y*byteWidth
                        # Get color index
                        colorIdx = struct.unpack('B', self.byteImage[posByte])[0]
                        if bitDepth == 4:
                            pos1 = 2*x+1 + (y+1)*byteWidth/2
                            pos2 = 2*x + (y+1)*byteWidth/2
                            self.image[pos1] = self.palette[(colorIdx & 0xf0) / 0x10]
                            self.image[pos2] = self.palette[colorIdx & 0x0f]
                        else:
                            self.image[pos] = self.palette[colorIdx]
                    except:
						continue
        pass
    
    def arrangeByteImage(self):
        # Image is arranges into number of blocks'
        # Width is 16 bytes for all images except 4-bit images
        blockWidth = 16
        # Height is 8 bytes
        blockHeight = 8
        # We assume that the total height is a bit bigger
        byteWidth = int(math.ceil(float(self.width) / blockWidth) * blockWidth )
        byteHeight = int(math.ceil(float(self.height) / blockHeight) * blockHeight)
        # The resulting image size
        self.byteImage = [None] * byteHeight*byteWidth
        # Block size
        blockSize = blockHeight*blockWidth
        block = [None] * blockSize
        # Blocks in one row
        blockRow = byteWidth/blockWidth
        # Byte offset for 1 row
        byteRow = int(float(self.width)/blockWidth * blockSize)
        # Total number of blocks in image
        numBlocks = byteHeight*byteWidth / (blockSize)
        # Add few blocks to process the last part of the image (it can be not divided by blockHeight)
        #numBlocks += blockRow - self.height % blockHeight
        # For 32-bit images block number should be x4 (4-byte groups)
        if struct.unpack('B', self.full[0x4C])[0] == 32:
            numBlocks *= 4
            self.byteImage *= 4
            blockRow *= 4
            byteWidth *= 4
        # If the image is just too small
        if numBlocks == 0:
            bitDepth = struct.unpack('B', self.full[0x4C])[0]
            for row in xrange(byteHeight):
                for col in xrange(byteWidth * bitDepth/8):
                    bytePos = col + row * byteWidth * 8/bitDepth
                    self.byteImage[bytePos] = self.full[128 + col + blockWidth*row]
            pass 
        # If everything's ok    
        lastPos = len(self.header)
        i = 0
        while lastPos < len(self.data):
            # Offset from the left border of the block row on the full image
            fromLeft = (i % blockRow)*blockWidth
            # Block row offset
            rowOffset = i//blockRow * blockSize * blockRow
            # Block data
            # Even the block at the end contains the same amount of data
            # There'll just be few trailing zeros in each line
            block = self.full[lastPos: lastPos + blockSize]
            lastPos += blockSize
            # Now we should put data into byteimage with the reversed row order
            # e.g. first we should put the last 16-byte row, then the second last...
            for j in xrange(blockHeight):
                fromTop = j*byteWidth
                # Beginning and ending position for the row in the image
                posBegin = fromLeft + fromTop + rowOffset
                posEnd = posBegin + blockWidth
                # Row inside the block
                blockRowBegin = j*blockWidth
                blockRowEnd = blockRowBegin + blockWidth
                for x in range(posBegin, posEnd):
                    try:
                        self.byteImage[x] = block[blockRowBegin + (x - posBegin)]
                    except:
                        # Don't care (maybe we're just handling the last lines)
                        continue
            i += 1
        # Remove all Nones (is the image height mod blockHeight != 0)
        self.byteImage = filter(lambda z: z != None, self.byteImage)
        pass
