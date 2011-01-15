# coding=utf-8
#!/usr/bin/env python

import wx


    

class FrontEnd_Old():
    def __init__(self,Title,QueryMsg,DefaultValue="",Style=wx.OK|wx.CANCEL):
        self.Title = Title
        self.QueryMsg = QueryMsg
        self.DefaultValue = DefaultValue
        self.Style = Style

    def queryUser(self,Msg,DefVal=""):
        app = wx.PySimpleApp() 
        dialog = wx.TextEntryDialog(None,Msg,self.Title,DefVal,style=wx.OK|wx.CANCEL)
        # dialog.SetSizeWH(800,600)
        # dialog.AnsBox()
        dialog.ShowFullScreen(True)
        if dialog.ShowModal() == wx.ID_OK: 
           Value = dialog.GetValue() 
        dialog.Destroy()
        return Value

class BigBox(wx.Dialog):
    def __init__(self,Title,QueryMsg,DefaultValue="",Style=wx.OK|wx.CANCEL):
        wx.Dialog.__init__(self, None, -1, Title, size=(250, 210))

        self.Title = Title
        self.QueryMsg = QueryMsg
        self.DefaultValue = DefaultValue
        self.Style = Style
        
    def queryUser(self,Msg,DefVal="",title="wakaka"):

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        

        font_Ans = wx.Font(40, wx.DECORATIVE, 
                       wx.ITALIC, wx.NORMAL)
        font_Question = wx.Font(30, wx.DECORATIVE, 
                       wx.ITALIC, wx.NORMAL)

        QuestionText = wx.StaticText(self, -1,Msg,size=(-1,300),style = wx.ALIGN_CENTER)
        QuestionText.SetForegroundColour('black') 
        QuestionText.SetBackgroundColour('white')
        QuestionText.SetFont(font_Question)
        
        self.AnsBox = wx.TextCtrl(self, -1, "",
                               size = (-1,400),
                               style = wx.TE_PROCESS_ENTER |wx.ALIGN_CENTER ^(wx.TE_PASSWORD) )

        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPushed, self.AnsBox)
        
        self.AnsBox.SetForegroundColour('white') 
        self.AnsBox.SetBackgroundColour('black')
        self.AnsBox.SetFont(font_Ans)
        
        self.button = wx.Button(self, wx.ID_OK, "OK",style=wx.ID_OK, pos=(50, 20)) 
        #self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()
        
        self.panelSizer.Add(QuestionText,10, flag=wx.EXPAND)
        self.panelSizer.Add(self.AnsBox,10, flag=wx.EXPAND)
        self.panelSizer.Add(self.button,1, flag=wx.EXPAND)
        self.SetSizer(self.panelSizer)
        self.Fit()
        self.ShowFullScreen(True)
        if self.ShowModal() == wx.ID_OK: 
            Value = self.AnsBox.GetValue()
        self.Destroy()
        return Value

        
    def OnClick(self, event):
        print "OK pushed"

    def OnEnterPushed(self, event):
        self.EndModal(wx.ID_OK)
        pass
    
class FrontEnd(BigBox):
    pass

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frontIns = FrontEnd("who are you?","yourName?")
    frontIns.queryUser("bl")
    # app = wx.PySimpleApp()
    # fe2 = BigBox("What's your name??")
    # fe2.ShowFullScreen(True)
    # if fe2.ShowModal() == wx.ID_OK: 
    #     Value = fe2.AnsBox.GetValue()
    #     print Value
    # fe2.Destroy()
    #app.MainLoop()

