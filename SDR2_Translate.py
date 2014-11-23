#!/usr/bin/python
#coding=utf8

import rpErrorHandler
from Tkinter import *
#------------------------------------------------------------------------------#
#                                                                              #
#                                    Filter                                    #
#                                                                              #
#------------------------------------------------------------------------------#
class Filter(Toplevel):
    def __init__(self,Master=None,*pos,**kw):
        #
        #Your code here
        #

        apply(Toplevel.__init__,(self,Master),kw)
        self.bind('<Map>',self.on_Filter_Map)
        self._OpCodesFrame = Frame(self)
        self._OpCodesFrame.pack(side='top')
        self._OkFrame = Frame(self)
        self._OkFrame.pack(side='top')
        self._CancelBtn = Button(self._OkFrame,text='Cancel')
        self._CancelBtn.pack(anchor='e',side='right')
        self._OkBtn = Button(self._OkFrame,text='OK')
        self._OkBtn.pack(anchor='e',side='right')
        self._VisibleFrame = Frame(self._OpCodesFrame)
        self._VisibleFrame.pack(side='left')
        self._VisibleCodesLbl = Label(self._VisibleFrame,text='Visible OpCodes')
        self._VisibleCodesLbl.pack(side='top')
        self._VisibleCodeList = Listbox(self._VisibleFrame)
        self._VisibleCodeList.pack(side='top')
        self._VisibleCodeList.bind('<<ListboxSelect>>' \
            ,self._on_VisibleCodeList_select)
        self._BtnFrame = Frame(self._OpCodesFrame)
        self._BtnFrame.pack(side='left')
        self._HideBtn = Button(self._BtnFrame,state='disabled',text='=>')
        self._HideBtn.pack(side='top')
        self._HideBtn.bind('<ButtonPress-1>',self._on_HideBtn_Button_1)
        self._ShowBtn = Button(self._BtnFrame,state='disabled',text='<=')
        self._ShowBtn.pack(side='top')
        self._ShowBtn.bind('<ButtonPress-1>',self._on_ShowBtn_Button_1)
        self._HiddenFrame = Frame(self._OpCodesFrame)
        self._HiddenFrame.pack(side='left')
        self._HiddenCodeLbl = Label(self._HiddenFrame,text='Hidden OpCodes')
        self._HiddenCodeLbl.pack(side='top')
        self._HiddenCodeList = Listbox(self._HiddenFrame)
        self._HiddenCodeList.pack(side='top')
        self._HiddenCodeList.bind('<<ListboxSelect>>' \
            ,self._on_HiddenCodeList_select)
        #
        #Your code here
        #
        self.Master = Master
        self.visible_list = {}
        self.hidden_list = {}
    #
    #Start of event handler methods
    #
    def initLists(self, hidden, visible):
        self.hidden_list = hidden
        self.visible_list = visible
        self.populate()
        pass

    def populate(self):
        self._VisibleCodeList.delete(0,END)
        self._HiddenCodeList.delete(0,END)
        for code,value in self.hidden_list.items():
            if value != '':
                self._HiddenCodeList.insert(END, value)
            else:
                self._HiddenCodeList.insert(END, 'op_'+code)
        for code,value in self.visible_list.items():
            if value != '':
                self._VisibleCodeList.insert(END, value)
            else:
                self._VisibleCodeList.insert(END, 'op_'+code)
        pass

    def _on_HiddenCodeList_select(self,Event=None):
        self._ShowBtn['state'] = 'normal'
        self._HideBtn['state'] = 'disabled'
        pass

    def _on_HideBtn_Button_1(self,Event=None):
        # Delete from the Visible list
        i = int(self._FlowList.curselection()[0])        
        
        self._VisibleCodeList.delete(i)
        # Insert into the Hidden list
        self._HiddenCodeList.insert
        pass

    def _on_ShowBtn_Button_1(self,Event=None):
        pass

    def _on_VisibleCodeList_select(self,Event=None):
        self._ShowBtn['state'] = 'disabled'
        self._HideBtn['state'] = 'normal'
        pass

    def on_Filter_Map(self,Event=None):
        # Grab the focus
        self.focus_set()
        self.grab_set()
        self.transient(self.Master)
        pass
    #
    #Start of non-Rapyd user code
    #


pass #---end-of-form---
#------------------------------------------------------------------------------#
#                                                                              #
#                                   GameData                                   #
#                                                                              #
#------------------------------------------------------------------------------#
class GameData(Toplevel):
    def __init__(self,Master=None,*pos,**kw):
        #
        #Your code here
        #

        apply(Toplevel.__init__,(self,Master),kw)
        self.GameDataLoc = StringVar()
        self._Frame3 = Frame(self)
        self._Frame3.pack(side='top')
        self._GameDataLbl = Label(self._Frame3,text='Game Data Options')
        self._GameDataLbl.pack(side='top')
        self._Frame2 = Frame(self)
        self._Frame2.pack(side='top')
        self._PathLbl = Label(self._Frame2,text='Path to Game Data')
        self._PathLbl.pack(side='left')
        self._DataLoc = Entry(self._Frame2,textvariable=self.GameDataLoc)
        self._DataLoc.pack(side='left')
        self._BrowseLocBtn = Button(self._Frame2,text='Browse')
        self._BrowseLocBtn.pack(side='left')
        self._BrowseLocBtn.bind('<ButtonPress-1>' \
            ,self._on_BrowseLocBtn_Button_1)
        self._Frame1 = Frame(self)
        self._Frame1.pack(side='top')
        self._Label1 = Label(self._Frame1)
        self._Label1.pack(side='left')
        self._Entry2 = Entry(self._Frame1)
        self._Entry2.pack(side='left')
        #
        #Your code here
        #
        self.GameDataLoc.set(GameDataLoc)
    #
    #Start of event handler methods
    #


    def _on_BrowseLocBtn_Button_1(self,Event=None):
        fn = tkFileDialog.askdirectory('.',False,'Choose Game Data directory',Trues)
        pass
    #
    #Start of non-Rapyd user code
    #


pass #---end-of-form---
#------------------------------------------------------------------------------#
#                                                                              #
#                                OpCodeCreator                                 #
#                                                                              #
#------------------------------------------------------------------------------#
class OpCodeCreator(Toplevel):
    def __init__(self,Master=None,*pos,**kw):
        #
        #Your code here
        #
        self.selected_opcode = 0
        self.selected_par = 0
        self.opcode_list = []
        self.par_list = []
        self.Master = Master

        apply(Toplevel.__init__,(self,Master),kw)
        self.bind('<Map>',self.on_OpCodeCreator_Map)
        self._ParValue = StringVar()
        self._ParName = StringVar()
        self._HeaderFrame = Frame(self)
        self._HeaderFrame.pack(side='top')
        self._TopLabel = Label(self._HeaderFrame
            ,text='Define the opcode and press OK')
        self._TopLabel.pack(side='top')
        self._ListFrame = Frame(self)
        self._ListFrame.pack(side='top')
        self._OpCodeList = Listbox(self._ListFrame)
        self._OpCodeList.pack(expand='yes',fill='both',side='left')
        self._OpCodeList.bind('<<ListboxSelect>>',self._on_OpCodeList_select)
        self._OpCodeList.bind('<Map>',self._on_OpCodeList_Map)
        self._ParBox = Listbox(self._ListFrame)
        self._ParBox.pack(side='left')
        self._ParBox.bind('<<ListboxSelect>>',self._on_ParBox_select)
        self._EntryFrame = Frame(self)
        self._EntryFrame.pack(side='top')
        self._ParNameLbl = Label(self._EntryFrame,textvariable=self._ParName)
        self._ParNameLbl.pack(side='left')
        self._ParEntry = Entry(self._EntryFrame,textvariable=self._ParValue)
        self._ParEntry.pack(side='left')
        self._AddParBtn = Button(self._EntryFrame,text='Set')
        self._AddParBtn.pack(side='left')
        self._AddParBtn.bind('<ButtonPress-1>',self._on_AddParBtn_Button_1)
        self._SubmitFrame = Frame(self)
        self._SubmitFrame.pack(expand='yes',fill='x',side='top')
        self._CancelBtn = Button(self._SubmitFrame,text='Cancel')
        self._CancelBtn.pack(anchor='e',side='right')
        self._CancelBtn.bind('<ButtonPress-1>',self._on_CancelBtn_Button_1)
        self._OkBtn = Button(self._SubmitFrame,text='OK')
        self._OkBtn.pack(anchor='e',side='right')
        self._OkBtn.bind('<ButtonPress-1>',self._on_OkBtn_Button_1)
        #
        #Your code here
        #
    #
    #Start of event handler methods
    #


    def _on_AddParBtn_Button_1(self,Event=None):
        # Save current parameter to the list
        i = self.selected_par  
        self.par_list[i] = (self.par_list[i][0], int(self._ParValue.get()))
        # Re-populate parameters listbox
        self._ParBox_populate()
        pass

    def _on_CancelBtn_Button_1(self,Event=None):
        self.destroy()
        pass

    def _on_OkBtn_Button_1(self,Event=None):
        question = "You really sure you want to add the new op?"
        proceed = tkMessageBox.askyesno("WARNING", question)
        if proceed:
            # Insert new value into the master's lists
            i = self.Master.current_act_idx+1
            self.Master.Lin.opcode_list.insert(i, self.selected_opcode)
            self.Master.Lin.action_list.insert(i, OP_FUNCTIONS[self.selected_opcode])
            self.Master.Lin.pars_list.insert(i, self.par_list)
            # Refresh master's listboxes
            self.Master.populateLinLists()
            # Exit
            self.destroy()
        pass

    def _on_OpCodeList_Map(self,Event=None):
        for code,name in OP_FUNCTIONS.iteritems():
            if not name:
                self._OpCodeList.insert(END, "op_%d" % code)
            else:
                self._OpCodeList.insert(END, name)
            # We need to store the opcodes, otherwise we won't have 2-sided relation
            self.opcode_list.append(code)
        pass
    

    def _on_OpCodeList_select(self,Event=None):
        i = int(self._OpCodeList.curselection()[0])
        self.selected_opcode = self.opcode_list[i]
        # Add the parameters to the list
        self.par_list = []
        for par in OP_PARAMS[self.selected_opcode]:
            self.par_list.append((par[0], -1))
        # Display pars in the listbox
        self._ParBox_populate()
        pass
        
    def _ParBox_populate(self):
        self._ParBox.delete(0,END)
        for par in self.par_list:
            self._ParBox.insert(END, par)
        pass
    

    def _on_ParBox_select(self,Event=None):
        self.selected_par = int(self._ParBox.curselection()[0])  
        i = self.selected_par      
        # Put the current name and value to the label and editbox
        self._ParName.set(self.par_list[i][0])
        self._ParValue.set(self.par_list[i][1])
        pass

    def on_OpCodeCreator_Map(self,Event=None):
        # Grab the focus
        self.focus_set()
        self.grab_set()
        self.transient(self.Master)
        pass
    #
    #Start of non-Rapyd user code
    #


pass #---end-of-form---
#------------------------------------------------------------------------------#
#                                                                              #
#                                SDR2_Translate                                #
#                                                                              #
#------------------------------------------------------------------------------#
class SDR2_Translate(Frame):
    def __init__(self,Master=None,*pos,**kw):
        #
        #Your code here
        #
        self.curPath = '.'
        self.current_str_idx = 0
        self.current_act_idx = 0
        self.actionFlow = []
        self.strange_byte = ''
        self.currentImage = ''
        self.scene = Scene()
        self.charNames = getCharNames(GameDataLoc)
        self.Lin = LinFile()
        self.mode = ''
        self.pak_level = 0
        self.visible_opcodes = OP_FUNCTIONS
        self.hidden_opcodes = {}

        apply(Frame.__init__,(self,Master),kw)
        self._CurAction = StringVar()
        self._CurrentEditString1 = StringVar()
        self._CurrentEditString2 = StringVar()
        self._CurrentEditString3 = StringVar()
        self._FileNameText = StringVar()
        self._Filtered = StringVar()
        self._OpCodeEditText = StringVar()
        self._ParEditText = StringVar()
        self._ParLabelText = StringVar()
        self._EditString1Len = StringVar()
        self._EditString2Len = StringVar()
        self._EditString3Len = StringVar()
        self._MenuFrame = Frame(self)
        self._MenuFrame.pack(anchor='nw',fill='both',side='top')
        self._RootMenu = Menu(self._MenuFrame,type='menubar')
        self._RootMenu.pack(anchor='nw',expand='yes',fill='both',side='left')
        self._RootMenu.bind('<Map>',self._on_RootMenu_Map)
        self._FileNameFrame = Frame(self)
        self._FileNameFrame.pack(fill='x',side='top')
        self._FileName = Label(self._FileNameFrame
            ,textvariable=self._FileNameText)
        self._FileName.pack(side='top')
        self._Frame2 = Frame(self)
        self._Frame2.pack(anchor='nw',expand='yes',fill='both',side='top')
        self._OpFrame = Frame(self._Frame2)
        self._OpFrame.pack(anchor='nw',fill='y',ipadx='25',side='left')
        self._ContentFrame = Frame(self._Frame2)
        self._ContentFrame.pack(anchor='nw',expand='yes',fill='both',side='left')
        self._Frame1 = Frame(self._OpFrame)
        self._Frame1.pack(fill='both',side='top')
        self._FlowFrameLabel = Label(self._Frame1,text='Actions List')
        self._FlowFrameLabel.pack(anchor='nw',fill='x',side='left')
        self._FilterFlowList = Checkbutton(self._Frame1
            ,command=self._on_FilterFlowList_check,text='Filtered'
            ,variable=self._Filtered)
        self._FilterFlowList.pack(anchor='ne',side='right')
        self._FlowFrame = Frame(self._OpFrame)
        self._FlowFrame.pack(expand='yes',fill='both',side='top')
        self._FlowList = Listbox(self._FlowFrame)
        self._FlowList.pack(expand='yes',fill='both',side='top')
        self._FlowList.bind('<<ListboxSelect>>',self._on_FlowList_select)
        self._Frame3 = Frame(self._OpFrame)
        self._Frame3.pack(fill='x',side='top')
        self._AddOpBtn = Button(self._Frame3,height='3',text='ADD OP')
        self._AddOpBtn.pack(expand='yes',fill='both',side='left')
        self._AddOpBtn.bind('<ButtonPress-1>',self._on_AddOpBtn_Button_1)
        self._DelOpBtn = Button(self._Frame3,text='DELETE OP')
        self._DelOpBtn.pack(expand='yes',fill='both',side='left')
        self._DelOpBtn.bind('<ButtonPress-1>',self._on_DelOpBtn_Button_1)
        self._TabHost = ttk.Notebook(self._ContentFrame)
        self._TabHost.pack(anchor='nw',expand='yes',fill='both',side='top')
        self._Frame9 = Frame(self._ContentFrame)
        self._Frame9.pack(fill='x',side='top')
        self._WorkLabelFrame = Frame(self._ContentFrame)
        self._WorkLabelFrame.pack(anchor='nw',fill='x',side='top')
        self._WorkFrameLabel = Label(self._WorkLabelFrame,text='Parameters List')
        self._WorkFrameLabel.pack(padx='35',side='left')
        self._CurActionLabel = Label(self._WorkLabelFrame
            ,textvariable=self._CurAction)
        self._CurActionLabel.pack(side='left')
        self._ParFrame = Frame(self._ContentFrame)
        self._ParFrame.pack(anchor='nw',expand='yes',fill='both',side='top')
        self._StringFrame = Frame(self._TabHost)
        self._StringFrame.pack(side='left')
        self._StringListLabel = Label(self._StringFrame,text='String list')
        self._StringListLabel.pack(anchor='n',fill='x',side='top')
        self._StringList = Listbox(self._StringFrame)
        self._StringList.pack(anchor='nw',expand='yes',fill='both',side='top')
        self._StringList.bind('<<ListboxSelect>>',self._on_StringList_select)
        self._MiscFrame = Frame(self._TabHost)
        self._MiscFrame.pack(side='left')
        self._MiscList = Listbox(self._MiscFrame)
        self._MiscList.pack(side='top')
        self._CanvasFrame = Frame(self._TabHost)
        self._CanvasFrame.pack(side='left')
        self._ScreenView = Canvas(self._CanvasFrame,background='#000000'
            ,height=SCREEN_H,width=SCREEN_W)
        self._ScreenView.pack(expand='yes',side='top')
        self._Frame10 = Frame(self._Frame9)
        self._Frame10.pack(side='left')
        self._EditString1 = Entry(self._Frame10
            ,textvariable=self._CurrentEditString1,width='50')
        self._EditString1.pack(anchor='s',side='top')
        self._EditString3 = Entry(self._Frame10
            ,textvariable=self._CurrentEditString3,width='50')
        self._EditString3.pack(side='bottom')
        self._EditString2 = Entry(self._Frame10
            ,textvariable=self._CurrentEditString2,width='50')
        self._EditString2.pack(side='bottom')
        self._Frame12 = Frame(self._Frame9)
        self._Frame12.pack(side='left')
        self._String1Len = Label(self._Frame12,textvariable=self._EditString1Len)
        self._String1Len.pack(side='top')
        self._String2Len = Label(self._Frame12,textvariable=self._EditString2Len)
        self._String2Len.pack(side='top')
        self._String3Len = Label(self._Frame12,textvariable=self._EditString3Len)
        self._String3Len.pack(side='bottom')
        self._Frame11 = Frame(self._Frame9)
        self._Frame11.pack(anchor='nw',fill='x',side='left')
        self._SetStringBtn = Button(self._Frame11,text='SET STRING')
        self._SetStringBtn.pack(side='left')
        self._SetStringBtn.bind('<ButtonPress-1>' \
            ,self._on_SetStringBtn_Button_1)
        self._Frame4 = Frame(self._ParFrame)
        self._Frame4.pack(expand='yes',fill='both',side='left')
        self._ParList = Listbox(self._Frame4)
        self._ParList.pack(expand='yes',fill='both',side='left')
        self._Frame5 = Frame(self._ParFrame)
        self._Frame5.pack(expand='yes',fill='x',side='left')
        self._ParListFrame = Frame(self._Frame5)
        self._ParListFrame.pack(expand='yes',fill='x',side='top')
        self._OpCodeLabel = Label(self._ParListFrame,text='Op Code',width='10')
        self._OpCodeLabel.pack(anchor='nw',side='left')
        self._OpCodeEdit = Entry(self._ParListFrame
            ,textvariable=self._OpCodeEditText)
        self._OpCodeEdit.pack(anchor='nw',side='left')
        self._ParEditFrame = Frame(self._Frame5)
        self._ParEditFrame.pack(expand='yes',fill='x',side='top')
        self._ParLabel = Label(self._ParEditFrame
            ,textvariable=self._ParLabelText,width='10')
        self._ParLabel.pack(anchor='nw',side='left')
        self._ParEdit = Entry(self._ParEditFrame,textvariable=self._ParEditText)
        self._ParEdit.pack(anchor='nw',side='left')
        self._Button1 = Button(self._ParEditFrame)
        self._Button1.pack(anchor='nw',side='left')
        #
        #Your code here
        #
        self._FileNameText.set('Select the file')
        self._ParLabelText.set('Par name')
        self._CurrentEditString1.trace('w', self._on_EditString1_modified)
        self._CurrentEditString2.trace('w', self._on_EditString2_modified)
        self._CurrentEditString3.trace('w', self._on_EditString3_modified)
        # Tabs
        self._TabHost.add(self._CanvasFrame, text="Canvas")
        self._TabHost.add(self._StringFrame, text="Strings")
        self._TabHost.add(self._MiscFrame, text="Misc")
        # Filter
        self._FilterFlowList.deselect()
    #
    #Start of event handler methods
    #
    def _on_EditString1_modified(self,*args):
        # We don't need to count the <CLT>s
        string = self._CurrentEditString1.get()
        string = re.sub(r'<CLT.*?>', '', string)
        self._EditString1Len.set('Chars left: %d' % (30 - len(string)))
        pass

    def _on_EditString2_modified(self,*args):
        # We don't need to count the <CLT>s
        string = self._CurrentEditString2.get()
        string = re.sub(r'<CLT.*?>', '', string)
        self._EditString2Len.set('Chars left: %d' % (30 - len(string)))
        pass

    def _on_EditString3_modified(self,*args):
        # We don't need to count the <CLT>s
        string = self._CurrentEditString3.get()
        string = re.sub(r'<CLT.*?>', '', string)
        self._EditString3Len.set('Chars left: %d' % (30 - len(string)))
        pass

    def _on_AddOpBtn_Button_1(self,Event=None):
        question = "This action will ADD a new Operation into the script. Continue?"
        proceed = tkMessageBox.askyesno("WARNING", question)
        if proceed:
            # Here we should open another window to add op
            w = OpCodeCreator(self)
            # Wait for the window to close
            w.wait_window(w)
            pass
        pass

    def _on_DelOpBtn_Button_1(self,Event=None):
        question = "This action will DELETE the Operation from the script. Continue?"
        proceed = tkMessageBox.askyesno("WARNING", question)
        if proceed:
            i = int(self._FlowList.curselection()[0])
            self._FlowList.delete(i)
            del self.Lin.action_list[i]
        pass

    def _on_FilterFlowList_check(self,Event=None):
        if self._Filtered.get() == '1':
            # Create a filter window
            flt = Filter(self)
            # Populate the window
            flt.initLists(self.hidden_opcodes, self.visible_opcodes)
            # Wait for the window to close
            flt.wait_window(flt)
            pass
        else:
            pass
        pass

    def _on_FlowList_select(self,Event=None):
        self.current_act_idx = int(self._FlowList.curselection()[0])
        if self.mode == '.lin':
            self._on_FlowList_select_Lin()
        if self.mode == '.pak':
            self._on_FlowList_select_Pak()
        pass
    
    def _on_FlowList_select_Lin(self):
        if self._FlowList.size() > 0:
            i = int(self._FlowList.curselection()[0])
            action = self.Lin.action_list[i]
            pars = self.Lin.pars_list[i]
            code = self.Lin.opcode_list[i]
            # Clear everything related to pars in GUI
            self._OpCodeEditText.set('')
            self._ParEditText.set('')
            self._ParLabelText.set('Par name')
            self._ParList.delete(0,END)
            # Put all parameters to the GUI
            self._OpCodeEditText.set(code)
            for par in pars:
                self._ParList.insert(END, "%s:\t %d" % (par[0],par[1]) )
            # What to do for different opcodes
            # Show sprite
            if code == WRD_SPRITE:
                self.showSprite(pars)
            # Show flash
            if code == WRD_FLASH:
                self.showFlash(pars)
            # Text highlighting
            if code == WRD_CLT:
                self.scene.text_clt = True
            # Get string idx
            if code == WRD_GET_LINE_IDX:
                self._StringList.select_set(pars[0][1])
                self._on_StringList_select()
                self.scene.text = self._StringList.get(pars[0][1])
            # Print next string from FIFO
            if code == WRD_PRINT_LINE:
                self.printLine()
            # If waiting for input (go to the next line waiting)
            if code == WRD_WAIT_INPUT:
                self.scene.text = ''
            # Set speaker
            if code == WRD_SPEAKER:
                self.scene.speaker = self.charNames[pars[0][1]]
            # Go to the next script
            if code == WRD_GOTO_SCRIPT:
                question = 'Go to the next script: e%02d_%03d_%03d.lin?' % (pars[0][1], pars[1][1], pars[2][1])
                loadNext = tkMessageBox.askyesno("Go to the next script", question)
                if loadNext:
                    # Clear canvas
                    self._ScreenView.delete(ALL)
                    self.scene.flash = []
                    # Clear lists
                    self._FlowList.delete(0,END)
                    self._StringList.delete(0,END)
                    # Load next file
                    next_fn = os.path.join(GameDataLoc, 'jp', 'script', 'e%02d_%03d_%03d.lin' % (pars[0][1], pars[1][1], pars[2][1]))
                    self.decodeFile(next_fn)
        pass
    
    def _on_FlowList_select_Pak(self):
        if self._FlowList.size() > 0:
            # Now working not with actions, but with files
            i = int(self._FlowList.curselection()[0])
            # If we're returning from sub-pak
            if self._FlowList.get(i)[0] == '..':    
                self._FlowList.delete(0,END)
                for f in self.Pak.files:
                    self._FlowList.insert(END, "%s" % f[0])                
                self.pak_level -= 1
                pass
            # If not - looking at the current pak file and level
            if self.pak_level == 0:
                file = self.Pak.files[i]
            else:
                file = self.internalPak.files[i]
            # Checking the file type
            if '.gim' in file[0]:
                GimImage = GimFile()
                GimImage.fromData(file[1])
                GimImage.getImage()
                pilImage = PIL.Image.new("RGBA", (GimImage.width, GimImage.height))
                pilImage.putdata(GimImage.image)
                self.scene.sprite = ImageTk.PhotoImage(pilImage)
                POS_X = (2*SCREEN_W - GimImage.width)/2
                POS_Y = (2*SCREEN_H - GimImage.height)/2
                imagesprite = self._ScreenView.create_image(POS_X,POS_Y,image=self.scene.sprite, tag = 'sprite')                
            elif '.gmo' in file[0]:
                GmoImage = GmoFile()
                GmoImage.fromData(file[1])
                GmoImage.extractGim()
                GmoImage.gim.getImage()
                pilImage = PIL.Image.new("RGBA", (GmiImage.gim.width, GmoImage.gim.height))
                pilImage.putdata(GmoImage.gim.image)
                self.scene.sprite = ImageTk.PhotoImage(pilImage)
                POS_X = (2*SCREEN_W - GmoImage.gim.width)/2
                POS_Y = (2*SCREEN_H - GmoImage.gim.height)/2
                imagesprite = self._ScreenView.create_image(POS_X,POS_Y,image=self.scene.sprite, tag = 'sprite')                
            elif '.txt' in file[0]:
                self.scene.text = file[1].decode('utf16')
                self._CurrentEditString1.set(self.scene.text)
            elif '.dat' in file[0]:
                self.pak_level += 1
                # We'll use it as a directory
                self._FlowList.delete(0,END)
                # Inserting the 'go back' value
                self._FlowList.insert(END, '..')
                # Now unpack the file
                self.internalPak = PakFile()
                self.internalPak.fromData(file[1])
                for f in self.internalPak.files:
                    self._FlowList.insert(END, "%s" % f[0])
        pass
        
    def showSprite(self, pars):
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
    
    def showFlash(self, pars):
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

    def _on_RootMenu_Map(self,Event=None):
        # File menu
        FileMenu = Menu(self._RootMenu, tearoff=0)
        FileMenu.add_command(label="Open", command=self.openFile)
        FileMenu.add_command(label="Save", command=self.saveFile)
        FileMenu.add_command(label="Exit", command=exit)
        self._RootMenu.add_cascade(label="File", menu=FileMenu)
        # Options menu
        OptionsMenu = Menu(self._RootMenu, tearoff=0)
        OptionsMenu.add_command(label="Game Data", command=self.openGameDataOpts)
        self._RootMenu.add_cascade(label="Options", menu=OptionsMenu)
        pass
    
    def openGameDataOpts(self):
        gd = GameData()
        pass
        
    def openFile(self):
        options = {}
        options['filetypes'] = [('script files', '.lin'), ('image files', ('*.gim','*.gmo')), ('pak files', ('*.pak','*.p3d')), ('all files', '.*')]
        fn = tkFileDialog.askopenfilename(**options)
        self.decodeFile(fn)
        pass
    
    def saveFile(self):
        fn = tkFileDialog.asksaveasfilename()
        self.encodeFile(fn)
        pass
    
    def populateLinLists(self):
        # Clear everything
        self._StringList.delete(0,END)
        self._FlowList.delete(0,END)
        # Put strings into listbox
        for s in self.Lin.string_list:
            self._StringList.insert(END, s.decode('utf16'))        
        # Set action list
        for i in xrange(len(self.Lin.action_list)):
            self._FlowList.insert(END, "%s%s" % (self.Lin.action_list[i], self.Lin.pars_list[i]))
        pass
    
    def decodeFile(self, fn):
        file = os.path.split(fn)[1]
        self._FileNameText.set(file)
        print "Decoding %s" % fn
        # Lin file
        if '.lin' in file:
            self.mode = '.lin'
            # Decode another file
            self.Lin.decodeLinFile(fn)
            self.populateLinLists()
        
        # Pak file
        if '.pak' in file:
            self.mode = '.pak'
            # Decode .pak file
            self.Pak = PakFile(fn)
            self.Pak.getFiles()
            # Clear everything
            self._StringList.delete(0,END)
            self._FlowList.delete(0,END)
            # Put all filenames into the flow list
            for f in self.Pak.files:
                self._FlowList.insert(END, "%s" % f[0])
        
        # P3d file
        if '.p3d' in file:
            # That's the same pak
            self.mode = '.pak'
            # Decode .pak file
            self.Pak = P3dFile(fn)
            self.Pak.getFiles()
            # Put all filenames into the flow list
            for f in self.Pak.files:
                self._FlowList.insert(END, "%s" % f[0])
        pass
        
    def encodeFile(self,fn):
        file = os.path.split(fn)[1]
        self._FileNameText.set(file)
        if '.lin' in fn:
            self.Lin.encodeLinFile(fn)
        if '.pak' in fn:
            self.Pak.makePak(fn)
        pass
        
    def exit():
        Root.quit()

    def _on_SetStringBtn_Button_1(self,Event=None):
        # For .lin file we're just changing the string in its string_list
        if self.mode == '.lin':
            # Construct the new string
            str1 = self._CurrentEditString1.get()
            str2 = self._CurrentEditString2.get()
            str3 = self._CurrentEditString3.get()
            final_string = ''
            if str1 != '':
                final_string += str1 + ('\x0d\x00\x0a\x00').decode('utf16')
            if str2 != '':
                final_string += str2 + ('\x0d\x00\x0a\x00').decode('utf16')
            if str3 != '':
                final_string += str3 + ('\x0d\x00\x0a\x00').decode('utf16')
            # Replace chars that're not present in the game
            final_string = final_string.replace('?', u"\uFF1F") # Question mark
            # Get string index
            idx = self.current_str_idx
            # Delete the old string from the visible list
            self._StringList.delete(idx)
            # Insert the new string
            self.Lin.string_list[idx] = final_string
            self._StringList.insert(idx, final_string)
            # Show the new version
            self.scene.text = self._StringList.get(idx)
            self.printLine()
        # For .pak we're changing the Pak.files[i] content
        elif self.mode == '.pak':
            str = self._CurrentEditString1.get()
            i = self.current_act_idx
            l = list(self.Pak.files[i])
            l[1] = str.encode('utf16')
            self.Pak.files[i] = tuple(l)
        pass

    def _on_StringList_select(self,Event=None):
        if self._StringList.size() > 0:
            num = int(self._StringList.curselection()[0])
            string = self._StringList.get(num)
            string = string.split('\r\n')
            self._CurrentEditString1.set(string[0])
            if len(string) > 1:
                self._CurrentEditString2.set(string[1])
            else:
                self._CurrentEditString2.set('')
            if len(string) > 2:
                self._CurrentEditString3.set(string[2])
            else:
                self._CurrentEditString3.set('')
            self.current_str_idx = num
        pass
    #
    #Start of non-Rapyd user code
    #

# This one-liner splits the string without consuming delimiters
def splitkeepsep(s, sep):
    return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == sep else acc + [elem], re.split("(%s)" % re.escape(sep), s), [])

pass #---end-of-form---
import ttk, PIL, tkMessageBox
from gim2png import GimFile, GmoFile
from pak_extract import PakFile
from OpCodes import *
from Common import *
from Scene import Scene
from PIL import Image, ImageTk, ImageDraw, ImageFont
from clt import *
import re
from Character import *
from LinFile import *
from enum import *

try:
    #--------------------------------------------------------------------------#
    # User code should go after this comment so it is inside the "try".        #
    #     This allows rpErrorHandler to gain control on an error so it         #
    #     can properly display a Rapyd-aware error message.                    #
    #--------------------------------------------------------------------------#

    #Adjust sys.path so we can find other modules of this project
    import sys
    if '.' not in sys.path:
        sys.path.append('.')
    #Put lines to import other modules of this project here
    import os, re, struct
    import tkFileDialog
    
    # Global options (should migrate those into a file or smth)
    GameDataLoc = './game/'
    
    if __name__ == '__main__':

        Root = Tk()
        import Tkinter
        Tkinter.CallWrapper = rpErrorHandler.CallWrapper
        del Tkinter
        App = SDR2_Translate(Root)
        App.pack(expand='yes',fill='both')

        Root.geometry('640x480+10+10')
        Root.title('SDR2 Translate')
        Root.mainloop()
        
    #--------------------------------------------------------------------------#
    # User code should go above this comment.                                  #
    #--------------------------------------------------------------------------#
except:
    rpErrorHandler.RunError()