# coding=utf-8
#!/usr/bin/env python

import wx

class FrontEnd():
    def __init__(self,Title,QueryMsg,DefaultValue="",Style=wx.OK|wx.CANCEL):
        self.Title = Title
        self.QueryMsg = QueryMsg
        self.DefaultValue = DefaultValue
        self.Style = Style

    def queryUser(self,Msg,DefVal=""):
        app = wx.PySimpleApp() 
        dialog = wx.TextEntryDialog(None,Msg,self.Title,DefVal,style=wx.OK|wx.CANCEL)
        # dialog.SetSizeWH(800,600)
        # dialog.Center()
        dialog.ShowFullScreen(True)
        if dialog.ShowModal() == wx.ID_OK: 
           Value = dialog.GetValue() 
        dialog.Destroy()
        return Value

if __name__ == '__main__':
    frontIns = FrontEnd("who are you?","yourName?")
    frontIns.queryUser("bl")

