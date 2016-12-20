#!/usr/bin/python

import wx
import sys
import hashlib
import wx
import os
import stat
import time

class MyFileDropTarget(wx.FileDropTarget):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, panel):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.panel = panel

 
    #----------------------------------------------------------------------
    def OnDropFiles(self, x, y, files):
        self.panel.SetInsertionPointEnd()
        self.panel.updateText("\n%d file(s) dropped at %d,%d:\n" %
                              (len(files), x, y))
        # Compute sha256
        BLOCKSIZE = 65536
        hasher = hashlib.sha256()
        for filepath in files:
            with open(filepath, 'rb') as myFile:
                buffer = myFile.read(BLOCKSIZE)
                while len(buffer) > 0:
                    hasher.update(buffer)
                    buffer = myFile.read(BLOCKSIZE)
            print(hasher.hexdigest())
            
            filename = os.path.basename(filepath)
            file_stats = os.stat(filepath)
            creation_time = time.strftime("%m/%d/%Y %I:%M %p",
                                          time.localtime(file_stats[stat.ST_CTIME]))
            modified_time = time.strftime("%m/%d/%Y %I:%M %p",
                                          time.localtime(file_stats[stat.ST_MTIME]))
            file_size = file_stats[stat.ST_SIZE]
            self.panel.updateText(filename + '\n')
            self.panel.updateText(filepath + '\n')
            self.panel.updateText(creation_time + '\n')
            self.panel.updateText(modified_time + '\n')
            self.panel.updateText(hasher.hexdigest() + '\n')

        
class Panel(wx.Panel):
    """"""
    def __init__(self, parent):      
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        #--- START Definition of the Panel ---#      
        titleText = wx.StaticText(self, wx.ID_ANY, 'Drag and Drop panel below')
        
        # Buttons events
        okButton = wx.Button(self, wx.ID_ANY, 'OK')
        exitButton = wx.Button(self, wx.ID_ANY, 'Exit')
        exitButton.Bind(wx.EVT_BUTTON, parent.OnClose)

        #---------------------- DnD ELEMENTS ----------------------#
        file_drop_target = MyFileDropTarget(self)
        # Field
        self.fileTextCtrl = wx.TextCtrl(self,
                                        style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY, size=(420,370))
        self.fileTextCtrl.SetDropTarget(file_drop_target)

        #---------------------- DnD ELEMENTS ----------------------#
        
        # Layers
        sizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        DragNDropSizer = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(titleText, 0, wx.ALL, 5)
        buttonSizer.Add(okButton, 0, wx.ALL, 5)
        buttonSizer.Add(exitButton, 0, wx.ALL, 5)
        DragNDropSizer.Add(self.fileTextCtrl, 0, wx.ALL|wx.EXPAND, 5)

        # All in the main sizer
        sizer.Add(titleSizer, 0, wx.CENTER)
        sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(DragNDropSizer, 1,  wx.ALL|wx.EXPAND, 5)
        sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(buttonSizer, 0, wx.ALL|wx.CENTER, 5)
        
        self.SetSizer(sizer)

    #----------------------------------------------------------------------
    def SetInsertionPointEnd(self):
        """
        Put insertion point at end of text control to prevent overwriting
        """
        self.fileTextCtrl.SetInsertionPointEnd()
    #----------------------------------------------------------------------
    def updateText(self, text):
        """
        Write text to the text control
        """
        self.fileTextCtrl.WriteText(text)

  
 
        
class Frame(wx.Frame):
    def __init__(self, title):
        """Constructor"""
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(455,390))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        #--- START Menu ---#
        menuBar = wx.MenuBar()

        # First Menu
        menu = wx.Menu()
        # Bind Event OnClose
        m_exit = menu.Append(wx.ID_EXIT, "Exit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "File")
        
        self.SetMenuBar(menuBar)
        
         # Bar with definition
        self.statusbar = self.CreateStatusBar()
        
        #--- END Menu ---#
        
        topPanel = Panel(self)  
        topPanel.Layout()


    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
            "Are you sure?",
            "Confirm exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
        
if __name__ == "__main__":
    app = wx.App(False)
    top = Frame("Hash Drag and Drop Project")
    top.Show()
    app.MainLoop()
