#coding=utf8

import rpErrorHandler
from Tkinter import *
from OpCodes import *
import os
import struct

class LinFile():
    def __init__(self, 
                 baseoffset = -1, 
                 num_strings = -1,
                 string_list = [],
                 action_list = [],
                 pars_list = [],
                 opcode_list = []):
        self.baseoffset  = baseoffset
        self.num_strings = num_strings
        self.string_list = string_list
        self.action_list = action_list
        self.pars_list = pars_list
        self.opcode_list = opcode_list
        # Can't forget it ;)
        self.strange_byte = -1
        pass
    
    def clear(self):
        self.baseoffset = -1
        self.numstrings = -1
        self.string_list = []
        self.action_list = []
        self.pars_list = []
        self.opcode_list = []
        pass
    
    ##########################
    ## Decoder
    ##########################
    def decodeLinFile(self, fn):
        # Clear everything
        self.clear()
        # Open file
        fp = open(fn, 'rb')
        # Get type
        fp.seek(0)
        type = struct.unpack('I',fp.read(4))[0]
        # Get offset
        fp.seek(8)
        self.baseoffset = struct.unpack('I',fp.read(4))[0]
        # Read action list
        self.decodeLinBase(fp)
        # Read strings
        if self.baseoffset < os.path.getsize(fn):
            self.decodeLinStrings(fp)
        fp.close()
        pass
        
    def decodeLinBase(self, fp):
        fp.seek(0)
        while fp.tell() < self.baseoffset:
            curByte = fp.read(1)
            # If that's an operation
            if curByte == b'\x70':
                opCode = struct.unpack('B', fp.read(1))[0]
                action, pars = self.ResolveOpCode(opCode,fp)
                self.opcode_list.append(opCode)
                self.action_list.append(action)
                self.pars_list.append(pars)
            # Just some bytecode
            else:
                byte = struct.unpack('B', curByte)[0]
                self.opcode_list.append(0xFF)
                self.action_list.append('Bytecode')
                self.pars_list.append([('code',byte)])
        pass
        
    def decodeLinStrings(self, fp):
        fp.seek(self.baseoffset)
        self.num_strings = struct.unpack('I',fp.read(4))[0]
        self.string_list = [None] * self.num_strings
        for i in xrange(self.num_strings):
            # Jump to the next text offset value
            fp.seek(self.baseoffset + 4 + i * 4)
            # Read it
            fileoffset = struct.unpack('I',fp.read(4))[0]
            offset = self.baseoffset + fileoffset
            # Jump to this offset
            fp.seek(offset)
            # Read everything until 00 00
            string = ''
            while 1:
                word = fp.read(2)
                if word == '\x00\x00':
                    self.string_list[i] = string
                    break
                elif word == '\x0a\x00':
                    string += '\x0d\x00\x0a\x00'
                else:
                    string += word
        # Get this strange closing byte
        fp.seek(self.baseoffset + 4 + self.num_strings * 4)
        self.strange_byte = fp.read(4)
        pass


    ##########################
    ## Encoder
    ##########################
    def encodeLinFile(self, fn):
        fp = open(fn, 'wb')
        # Encode base
        for i in xrange(len(self.action_list)):
            action = self.action_list[i]
            code = self.opcode_list[i]
            pars = self.pars_list[i]
            ## If not a bytecode
            if code != 0xFF:
                fp.write(b'\x70')
                fp.write(struct.pack('B', code))
                self.encodeOp(code, pars, fp)
            else:
                fp.write(struct.pack('B', pars[0][1]))
        
        # Encode strings header
        for i in xrange(len(self.string_list)):
            # Some line modifications
            try:
                self.string_list[i] = self.string_list[i].encode('utf16')
            except:
                print "Can't encode string to utf16"
            self.string_list[i] = self.string_list[i].replace('\x0d\x00\x0a\x00', '\x0a\x00') + '\x00\x00'
        # Total number of strings
        fp.write(struct.pack('I', len(self.string_list)))
        # Calculating offset for each string
        # Each offset is encoded as 4-byte integer plus 2 integers
        # for header (total) and last int (dunno what it is)
        offset = (len(self.string_list) + 2)*4
        str_len = [offset]
        for s in self.string_list[:-1]:
            str_len.append(len(s) + str_len[-1])
        # Write offsets to file
        for t_len in str_len:
            fp.write(struct.pack('I', t_len))
        # Append the last int
        fp.write(self.strange_byte)
        # Write all texts
        for s in self.string_list:
            fp.write(s)
        
        fp.close()
        pass
    
    
    ##########################
    ## Decode OpCodes
    ##########################
    def UnknownOp(fp, code):
        global baseoffset
        string = []
        a = struct.unpack('B', fp.read(1))[0]
        while a != 0x70 and fp.tell() < baseoffset:
            string.append(a)
            a = struct.unpack('B', fp.read(1))[0]
        # Return 1 byte back
        fp.seek(-1, 1)
        RetStr = "UnknownOp(%s)" % (string)
        return (RetStr, code, string)
    
    def ResolveOpCode(self, code, fp):
        pars_out = []
        # Get parameters for the given OpCode
        pars = OP_PARAMS.get(code, None)
        # If OpCode is unknown
        if pars == None:
            action = 'UnknownOp_%d' % code
            pars_out.append((None, None))
        else:
            # First get name of the function
            action = OP_FUNCTIONS.get(code, None)
            # If the name is empty - just use names like op_66 or op_12, so they can be split by _
            if not action:
                action = 'op_%d' % code
            for par in pars:
                name = par[0]
                value = struct.unpack('%s' % par[1],   fp.read(int('%d' % par[2]))  )[0]
                pars_out.append((name, value))
            # Return name and pars list
            return action, pars_out


    ##########################
    ## Encode OpCodes
    ##########################
    def encodeOp(self, code, pars, fp):
        i = 0
        for parType in OP_PARAMS[code]:
            fp.write(struct.pack('%s' % parType[1], pars[i][1]))
            i += 1
    pass



# from LinFile import *
# Lin = LinFile()
# fp = open('e00_001_180.lin', 'rb')
