#coding=utf8

import rpErrorHandler
from Tkinter import *
#------------------------------------------------------------------------------#
#                                                                              #
#                                  ResViewer                                   #
#                                                                              #
#------------------------------------------------------------------------------#
class ResViewer(Toplevel):
    def __init__(self,Master=None,*pos,**kw):
        #
        #Your code here
        #

        apply(Toplevel.__init__,(self,Master),kw)
        self._Frame5 = Frame(self)
        self._Frame5.pack(side='top')
        self._TopMenu = Menu(self._Frame5)
        self._TopMenu.pack(side='left')
        self._TopMenu.bind('<Map>',self._on_TopMenu_Map)
        self._Frame3 = Frame(self)
        self._Frame3.pack(side='top')
        self._FileListFrame = Frame(self._Frame3)
        self._FileListFrame.pack(side='left')
        self._FileList = Listbox(self._FileListFrame)
        self._FileList.pack(side='top')
        self._Frame4 = Frame(self._Frame3)
        self._Frame4.pack(side='left')
        self._TabHost = ttk.Notebook(self._Frame4)
        self._TabHost.pack(side='top')
        self._Frame1 = Frame(self._Frame4)
        self._Frame1.pack(side='top')
        self._TextFrame = Frame(self._TabHost)
        self._TextFrame.pack(side='left')
        self._TextEdit = Entry(self._TextFrame)
        self._TextEdit.pack(side='top')
        self._CanvasFrame = Frame(self._TabHost)
        self._CanvasFrame.pack(side='left')
        self._Canvas = Canvas(self._CanvasFrame)
        self._Canvas.pack(side='top')
        self._MiscFrame = Frame(self._TabHost)
        self._MiscFrame.pack(side='left')
        #
        #Your code here
        #
        self._TabHost.add(self._TextFrame, text="Text")
        self._TabHost.add(self._CanvasFrame, text="Graphics")
        self._TabHost.add(self._MiscFrame, text="Misc")
    #
    #Start of event handler methods
    #


    def _on_TopMenu_Map(self,Event=None):
        # File menu
        FileMenu = Menu(self._RootMenu, tearoff=0)
        FileMenu.add_command(label="Open", command=self.openFile)
        FileMenu.add_command(label="Save", command=self.saveFile)
        FileMenu.add_command(label="Exit", command=exit)
        self._RootMenu.add_cascade(label="File", menu=FileMenu)
        pass
    
    def openFile(self):
        pass
    
    def saveFile(self):
        pass
    
    def exit(self):
        self.destroy()
        pass
    #
    #Start of non-Rapyd user code
    #


pass #---end-of-form---
import ttk, PIL, tkMessageBox

gui = ResViewer()