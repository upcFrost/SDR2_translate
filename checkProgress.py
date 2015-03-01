#coding=utf8

import rpErrorHandler
from Tkinter import *
#------------------------------------------------------------------------------#
#                                                                              #
#                              checkProgressForm                               #
#                                                                              #
#------------------------------------------------------------------------------#
class checkProgressForm(Frame):
    def __init__(self,Master=None,*pos,**kw):
        #
        #Your code here
        #
        self.returning = ''
        self.DataPath = {}
        self.root = Master

        apply(Frame.__init__,(self,Master),kw)
        self._Frame2 = Frame(self)
        self._Frame2.pack(side='top')
        self._TreeView = ttk.Treeview(self._Frame2)
        self._TreeView.pack(side='left')
        self._TreeView.bind('<Double-1>',self._onTreeViewDblClick)
        self._TreeScroll = Scrollbar(self._Frame2)
        self._TreeScroll.pack(expand='yes',fill='y',side='left')
        self._Frame1 = Frame(self)
        self._Frame1.pack(expand='yes',fill='x',side='top')
        self._Button1 = Button(self._Frame1)
        self._Button1.pack(anchor='w',expand='yes',fill='x',side='left')
        self._Button2 = Button(self._Frame1)
        self._Button2.pack(anchor='e',expand='yes',fill='x',side='left')
        #
        #Your code here
        #
        self._TreeView.insert('', 'end', 'ep_0', text='Prologue')
        self._TreeView.insert('', 'end', 'ep_1', text='Episode 1')
        self._TreeView.insert('', 'end', 'ep_2', text='Episode 2')
        self._TreeView.insert('', 'end', 'ep_3', text='Episode 3')
        self._TreeView.insert('', 'end', 'ep_4', text='Episode 4')
        self._TreeView.insert('', 'end', 'ep_5', text='Episode 5')
        self._TreeView.insert('', 'end', 'ep_M', text='Monokuma Theater')
        self._TreeView.insert('', 'end', 'ep_F', text='Free Time')
        self._TreeView.insert('', 'end', 'ep_O', text='Other')
        # Scrollbar
        self._TreeScroll.config( command = self._TreeView.yview )
        self._TreeView['yscrollcommand'] = self._TreeScroll.set
    #
    #Start of event handler methods
    #
    def populateTree(self, DataPath):
        self.DataPath = DataPath
        # Populate lists
        orig = []
        for (dirpath, dirnames, filenames) in walk(DataPath['orig']):
            orig.extend(filenames)
        proc = []
        for (dirpath, dirnames, filenames) in walk(DataPath['proc']):
            proc.extend(filenames)
        done = []
        for (dirpath, dirnames, filenames) in walk(DataPath['done']):
            done.extend(filenames)
        print proc
        # Episodes
        regexDict = {'ep_0': 'e00', 
                              'ep_1': 'e01', 
                              'ep_2': 'e02', 
                              'ep_3': 'e03', 
                              'ep_4': 'e04', 
                              'ep_5': 'e05'}
        for key, regex in regexDict.iteritems():
            epList = filter(lambda fn: re.match(r'%s' % regex, fn) != None, orig)
            for ep in epList:
                if ep in proc:
                    self._TreeView.insert(key, 'end', ep, text='%s' % ep, tags='proc')
                elif ep in done:
                    self._TreeView.insert(key, 'end', ep, text='%s' % ep, tags='done')
                else:
                    self._TreeView.insert(key, 'end', ep, text='%s' % ep, tags='orig')
        self._TreeView.tag_configure('proc', background='orange')
        self._TreeView.tag_configure('done', background='green')
        pass

    def _onTreeViewDblClick(self,Event=None):
        item = self._TreeView.selection()[0]
        fn = None
        # Create filename using tags
        if 'proc' in self._TreeView.item(item, 'tags'):
            fn = join(self.DataPath['proc'], 'jp', 'script', self._TreeView.item(item,"text"))
        elif 'done' in self._TreeView.item(item, 'tags'):
            fn = join(self.DataPath['done'], 'jp', 'script', self._TreeView.item(item,"text"))
        elif 'orig' in self._TreeView.item(item, 'tags'):
            fn = join(self.DataPath['orig'], 'jp', 'script', self._TreeView.item(item,"text"))
        else:
            # Exit if there's no tag (e.g. category)
            pass
        # Confirm
        question = 'Open file: %s?' % self._TreeView.item(item,"text")
        confirm = tkMessageBox.askyesno("Confirm action", question)
        if confirm:
            # Return filename and close popup
            self.returning = fn
            self.root.quit()
        pass
    #
    #Start of non-Rapyd user code
    #


pass #---end-of-form---
import re, ttk, tkMessageBox
import os
from os import listdir, walk
from os.path import isfile, join

# Data path is a dictionary with 3 paths - 'orig', 'proc' and 'done'
def checkProgress(DataPath):
    Root = Tk()
    Root.title('Progress')
    GetFn = checkProgressForm(Root)
    GetFn.pack(expand='yes',fill='both')
    GetFn.populateTree(DataPath)
    Root.mainloop()
    try:
        Root.destroy()
    except:
        pass
    return GetFn.returning