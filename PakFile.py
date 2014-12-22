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

import os, struct
from ext_guesser import guess_ext

NULL_BYTE = '\x00'
DEFAULT_EXT = '.dat'
P3D_MAGIC = '\xF0\x30\x60\x90'

class PakFile(object):
    def __init__(self,filename = ''):
        self.filename = filename
        self.files = []
    
    def getFiles(self, offset = 0):
        fp = open(self.filename, 'rb')
        # Added to be compatible with p3d
        fp.seek(offset)
        data = fp.read()
        self.files = list(self.get_pak_files(data))
        
    def fromData(self, data):
        self.files = list(self.get_pak_files(data))
    
    def makePak(self, fn):
        # Open file
        fp = open(fn, 'wb')
        # Write header (4-byte int)
        fp.write(struct.pack('I', len(self.files)))
        # First file offset (+1 for file count)
        offset = (len(self.files) + 1) * 4
        # Writing offsets for each file
        for f in self.files:
            fp.write(struct.pack('I', offset))
            offset += len(f[1])
        # Writing files
        for f in self.files:
            fp.write(f[1])
        # Close file
        fp.close()

    def to_string(self):
        # Buffer
        data = ''
        # Number of files
        data += struct.pack('I', len(self.files))
        # First file offset (+1 for file count)
        offset = (len(self.files) + 1) * 4
        # Writing offsets for each file
        for f in self.files:
            data += struct.pack('I', offset)
            offset += len(f[1])
        # Writing files
        for f in self.files:
            data += f[1]
        return data
            
    ##################################################
    ### 
    ##################################################
    def parse_pak_toc(self, data):
      
      # If we don't have enough to even get a file count, we're obviously no good.
      if len(data) < 32:
        raise Exception('Invalid archive', 'Archive file to short')
      
      # Get the number of files from the first 4 bytes
      num_files = struct.unpack('I', data[0:4])[0]
      # One extra for the file count.
      toc_len = (num_files + 1) * 4
      
      if num_files <= 0 or toc_len >= len(data):
        raise Exception('Invalid archive', 'No files in archive')
      
      file_starts = []
      file_ends   = []
      
      for i in xrange(num_files):
        file_start = struct.unpack('I', data[(i+1)*4 : (i+2)*4])[0]
        
        # Obviously, a file can't start after the end of the archive
        # or inside the table of contents.
        if file_start < toc_len or file_start >= len(data):
          raise Exception('Invalid archive', 'File starts after the EOF')
          
        # Doesn't make much sense if they're not in order.
        if i > 0 and file_start < file_starts[-1]:
          raise Exception('Invalid archive', 'Files not in correct order')
        
        file_starts.append(file_start)
      
      for i in xrange(num_files):
      
        file_start = file_starts[i]
        if i == num_files - 1:
          file_end = len(data)
        else:
          file_end = file_starts[i + 1]
        
        file_ends.append(file_end)
      
      return file_starts, file_ends
    
    
    
    ##################################################
    ### 
    ##################################################
    def get_pak_files(self, data, recursive = False, file_ext = None, ext_mode = 1, toc = None):
      
      # If we don't have enough to even get a file count, we're obviously no good.
      if len(data) < 32:
        raise Exception('Invalid archive', 'Archive file to short')
      
      file_starts = []
      file_ends   = []
      filenames   = None
      
      if toc == None:
        
        file_starts, file_ends = self.parse_pak_toc(data)
        num_files = len(file_starts)
      
      else:
        
        num_files = struct.unpack('I', data[0:4])
        
        filenames = []
        for entry in toc:
          file_pos = entry["file_pos"]
          file_end = file_pos + entry["file_len"]
          filename = entry["filename"]
          
          file_starts.append(file_pos)
          file_ends.append(file_end)
          filenames.append(filename)
      
      ### if toc == None ###
      
      for i in xrange(num_files):
        
        file_start  = file_starts[i]
        file_end    = file_ends[i]
        
        try:
          filename, extension = os.path.splitext(filenames[i])
          
        except TypeError, IndexError:
          filename = "%04d" % i
          extension = None
          
          if ext_mode == 1 or ext_mode == 2:# or file_ext == None:
            extension = guess_ext(data, file_start, file_end)
            
          if ext_mode == 0 or (ext_mode == 1 and extension == None):
            extension = file_ext
        
        # Look for a null character signifying the end of text data,
        # so we don't end up with any left-over junk or extra nulls.
        # Since text is UTF-16, we check two bytes at a time.
        if extension == ".txt":
          txt_end = file_end
          for txt_byte in xrange(file_start, file_end, 2):
            if data[txt_byte] == NULL_BYTE and data[txt_byte + 1] == NULL_BYTE:
              txt_end = txt_byte + 2
              break
          file_end = txt_end
        
        file_data = data[file_start : file_end]
        
        #print file_start, file_end, filename, extension
        
        if extension == None:
          if recursive == True:
            try:
              for subfile, subdata in get_pak_files(file_data, True, None):
                full_filename = os.path.join(filename, subfile)
                yield full_filename, subdata
            except InvalidArchiveException:
              extension = DEFAULT_EXT
          else:
            extension = DEFAULT_EXT
        
        if not extension == None:
          filename = filename + extension
          yield filename, file_data
      
      ### for i in xrange(num_files) ###
    

# Actually, p3d is a superclass of pak, only the header is changed
class P3dFile(PakFile):
    def __init__(self, filename = ''):
        super(P3dFile, self).__init__(filename)
        pass
    
    def getFiles(self):
        # Check magic number
        fp = open(self.filename, 'rb')
        magic = fp.read(len(P3D_MAGIC))
        fp.close()
        # If everything is ok - open just as if it was a pak file
        if struct.unpack('I', magic) == struct.unpack('I', P3D_MAGIC):
            super(P3dFile, self).getFiles(len(P3D_MAGIC))
            return 0
        else:
            print "Invalid P3D file: should start with %s" % P3D_MAGIC
            return -1
        pass

