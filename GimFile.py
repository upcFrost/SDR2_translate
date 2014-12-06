#coding=utf8

from Tkinter import *
import os, struct, math, array
from PIL import Image

MIG_MAGIC = '\x4D\x49\x47'

class GmoFile():
    def __init__(self):
        self.fn = ''
        self.full = array.array('B')
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
        self.full.fromfile(self.fp, self.fileSize/self.full.itemsize)
        # Reading header
        self.header = self.full[0:0x80]
        self.data = self.full[0x80:]
        pass
    
    def fromData(self, data):
        if isinstance(data, array.array):
            self.full = data
        else:
            self.full.fromstring(data)
        self.header = self.full[0:0x80]
        self.data = self.full[0x80:]
        pass
    
    def extractGim(self):
        try:
            offset = self.full.tostring().index(MIG_MAGIC)
            self.gim.fromData(self.full, offset)
        except:
            print 'No MIG data found'
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
        self.full = array.array('B')
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
        self.bitDepth = -1;
        pass
        
    def openGim(self, fn):
        self.fn = fn
        self.fp = open(self.fn, 'rb')
        # Go the the beginning
        self.fp.seek(0)
        # Get filesize
        self.fileSize = os.path.getsize(self.fn)
        # Read full file
        self.full.fromfile(self.fp, self.fileSize/self.full.itemsize)
        # Reading header
        self.header = self.full[0:0x80]
        self.data = self.full[0x80:]
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
        # Check if the array was passed
        if not isinstance(self.full, array.array):
            self.full = array.array('B')
            self.full.fromstring(data[offset:])
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
        # Check magic
        if self.header[0:3].tostring() == MIG_MAGIC:
            self.width = self.header[73]*256 + self.header[72]
            self.height = self.header[75]*256 + self.header[74]
            # Check for inversion
            invByte = self.header[0x30]
            if invByte == 4:
                self.inverted = True
                # Get palette position
                self.bitDepth = self.full[0x4C]
                if self.bitDepth != 32:
                    self.palettePosition = len(self.full) - (2 ** self.bitDepth)*4
                    self.data = self.full[0x80:self.palettePosition]
            return True
        return False

    def checkFooter(self):
        try:
            # Try to find it
            self.full.tostring().index('GimConv')
            # Footer starts with 0xff 0x00 0x00 0x00
            footerStartIdx = self.full[::-1].tostring().index('\x00\x00\x00\xff') + 4
            self.palettePosition -= footerStartIdx
            self.data = self.full[128:self.palettePosition]
        except:
            # Ok, found nothing
            pass
        pass
        
    
    def getPalette(self):
        self.paletteSize = int(2 ** self.bitDepth)
        # For 32 bits there's no color palette
        if self.bitDepth != 32:
            # Adjust palette if file has some trailing zeros
            i = 1
            while self.full[-i:-i-4:-1] == array.array('B', [0,0,0,0]):
                i += 4
            first_nonzero = i-1
            #first_nonzero = next((i for i, x in enumerate(self.full[::-1]) if x), None)
            if first_nonzero != 0:
                self.palettePosition -= first_nonzero
            for i in xrange(self.paletteSize):
                # 4 Bytes for each color (RGBA)
                color = [None] * 4
                # Pallete position
                position = self.palettePosition + i*4
                color[0] = self.full[position]
                color[1] = self.full[position + 1]
                color[2] = self.full[position + 2]
                color[3] = self.full[position + 3]
                self.palette.append(tuple(color))
        else:
            pass
        pass
    
    def getImage_OLD(self):
        self.getPalette()
        self.image = [0] * self.width*self.height
        self.arrangeByteImage()  
        
        byteSize = self.width*self.height * self.bitDepth/8
        byteHeight = self.height
        byteWidth = self.width 
        color = [None] * 4
        
        #if self.bitDepth == 4:
        #    # Stretch it, because bytes're coupled
        #    tmp = [[l >> 4, l & 0xf] for l in self.byteImage]
        #    self.byteImage = [x for sublist in tmp for x in sublist]
        
        if self.bitDepth == 32:
            # For 32 bits there's no color palette
            for i in xrange(byteSize):
                color[i%4] = self.byteImage[i]
                # Inverting alpha
                if i%4 == 3:
                    color[i%4] = 255 - color[i%4]
                # Dumping into the image
                if i%4 == 0 and i > 0:
                    self.image[i//4 - 1] = tuple(color)
                # For the last one
                if i == byteSize - 1:
                    self.image[-1] = tuple(color)
        elif self.bitDepth == 8:
            for y in xrange(byteHeight):
                for x in xrange(byteWidth):
                    try:
                        # Calculate pixel position
                        blockWidth = 16
                        posByte = x + int(math.ceil(float(self.width)/blockWidth)*blockWidth)*y
                        pos = x + y*byteWidth
                        # Get color index
                        colorIdx = self.byteImage[posByte]
                        self.image[pos] = self.palette[colorIdx]
                    except:
                        continue
        elif self.bitDepth == 4:
            self.aa = []
            for y in xrange(byteHeight):
                for x in xrange(byteWidth):
                    try:
                        # Calculate pixel position
                        blockWidth = 16
                        posByte = x + int(math.ceil(float(self.width)/blockWidth)*blockWidth)*y
                        self.aa.append(posByte)
                        # Get color index
                        colorIdx = self.byteImage[posByte]
                        # Calculate positions
                        pos1 = (2*x) + y*self.width
                        pos2 = (2*x+1) + y*self.width
                        self.image[pos1] = self.palette[(colorIdx & 0xf0) / 0x10]
                        self.image[pos2] = self.palette[colorIdx & 0x0f]
                    except:
                        continue
        else:
            print "Unknown bit depth!"
        pass
    
    
    #
    # FOR TESTING ONLY, DOES NOT WORK
    #
    def getImage(self):
        self.arrangeByteImage()
        if self.bitDepth == 32:
            self.image = map(self.long_to_bytearray, self.byteImage)
        else:
            self.getPalette()
            self.image = [self.palette[i] for i in self.byteImage]
        pass
	
    #
    # FOR TESTING ONLY, DOES NOT WORK
    #
    def arrangeByteImage(self):
        # We need to group the items differently for different bit depths
        tmpData = self.data
        if self.bitDepth == 32:
            # For 32-bit image - read by 4 bytes
            tmpData = array.array('I')
            tmpData.fromstring(self.data.tostring())
        if self.bitDepth == 4:
            # For 4-bit image - split each byte into 2
            tmpData = array.array('B')
            tmpData = self.flattenList(map(self.split_bytes, self.data))
        # Block Width
        bw = 128/self.bitDepth
        # Block Height
        bh = 8
        # Blocks in one row
        blk_row = int(math.ceil(float(self.width) / bw))
        # Total number of rows of height bh
        blk_height = int(math.ceil(float(self.height) / bh))
        # Original data organized by blocks of the given width
        tmpMtx = self.to_matrix(tmpData, bw)
        self.aa = tmpMtx
        # Index transformation matrix - shows how 16x1 blocks will be permuted
        transMtx = self.blockTransformMtx(blk_row, bh)
        tmpImage = []
        # For each bh block row
        for i in xrange(blk_height):
            try:
                tmpImage.append([tmpMtx[b + blk_row*bh*i] for b in transMtx])
            except:
                continue
        # Flatten the list
        tmpImage = self.flattenList(self.flattenList(tmpImage))
        # Delete those list items which were added to make it into 16x8 blocks
        added_len = bw - self.width % bw
        byte_width = self.width + added_len if self.width % bw != 0 else self.width
        self.byteImage = [tmpImage[i*byte_width:i*byte_width+self.width] for i in xrange(self.height)]
        self.byteImage = self.flattenList(self.byteImage)
        pass
        
    def arrangeByteImage_OLD(self):
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
        if self.bitDepth == 32:
            numBlocks *= 4
            self.byteImage *= 4
            blockRow *= 4
            byteWidth *= 4
        # If the image is just too small
        if numBlocks == 0:
            for row in xrange(byteHeight):
                for col in xrange(byteWidth * self.bitDepth/8):
                    bytePos = col + row * byteWidth * 8/self.bitDepth
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
    
    def to_matrix(self, l, n):
        return [l[i:i+n] for i in xrange(0, len(l), n)]
    
    def blockTransformMtx(self, blocksInWidth, bh = 8):
        return self.flattenList([range(i,blocksInWidth*bh,bh) for i in xrange(bh)])
        
    def flattenList(self, list):
        return [item for sublist in list for item in sublist]

    def long_to_bytearray(self, l):
        return tuple(l >> i & 0xff for i in (0,8,16,24))

    def split_bytes(self, l):
        return [l >> i & 0xf for i in (0,4)]
    
