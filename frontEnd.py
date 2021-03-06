# coding=utf-8
#!/usr/bin/env python

import wx 
import time
import winsound
from config import JiuJiuConfig
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "My Friendly Window",
                          (100, 100), (100, 100))
        

class BigBox(wx.Dialog):
    def __init__(self,Title,QueryMsg,DefaultValue="",Style=wx.OK|wx.CANCEL,Config="",QbgC="white",AnsBoxSize=10):
        wx.Dialog.__init__(self, None, -1, Title, size=(250, 210))
        #Read Config
        if Config != "":
            #Colors
            self.QbgC =  QbgC
            #Full Screen?
            if Config.get_GLCvalue('FullScreen') == u"yes":
                self.Is_FullScreen = True
            else:
                self.Is_FullScreen = False
        self.Title = Title
        self.QueryMsg = QueryMsg
        self.DefaultValue = DefaultValue
        self.Style = Style
        self.AnsBoxSize = AnsBoxSize
        
    def showInfo2User(self,Msg):
        self.queryUser(Msg,DefVal="Error!Error!",title="send email to mscame@gmail.com ASAP")
        
    def queryUser(self,Msg,DefVal="",title="wakaka"):
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        font_Ans = wx.Font(90, wx.DECORATIVE,
                           wx.NORMAL,
                           wx.NORMAL)
        lines = Msg.count('\n')
        if  lines > 5:
            Dsize = 40
        else:
            Dsize = 60 
        
        font_Question = wx.Font(Dsize, wx.DECORATIVE, 
                                wx.NORMAL,
                                wx.NORMAL)
        QuestionText = wx.StaticText(self, -1,Msg,size=(-1,300),style = wx.ALIGN_LEFT)
        QuestionText.SetForegroundColour('black') 
        QuestionText.SetBackgroundColour(self.QbgC)
        self.SetBackgroundColour(self.QbgC)
        QuestionText.SetFont(font_Question)
        self.AnsBox = wx.TextCtrl(self, -1, "",
                               size = (700,400),
                               style = wx.TE_PROCESS_ENTER |wx.ALIGN_CENTER ^(wx.TE_PASSWORD) )

        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPushed, self.AnsBox)
        self.AnsBox.SetForegroundColour('white') 
        self.AnsBox.SetBackgroundColour('black')
        self.AnsBox.SetFont(font_Ans)
        self.AnsBox.Bind(wx.wx.EVT_KEY_DOWN, self.OnKeyDown)


        self.panelSizer.Add(QuestionText,10, border = 256, flag=wx.LEFT|wx.ALIGN_LEFT)
        self.panelSizer.Add(self.AnsBox,self.AnsBoxSize, border = 60 ,flag=wx.ALL|wx.ALIGN_CENTER)
        self.SetSizer(self.panelSizer)
        self.Fit()
        self.ShowFullScreen(self.Is_FullScreen)
        Value = ""
        if self.ShowModal() == wx.ID_OK: 
            Value = self.AnsBox.GetValue()
        self.Destroy()
        return str(Value)
        
    def OnClick(self, event):
        print "OK pushed"

    def OnEnterPushed(self, event):
        beep('beep')
        self.EndModal(wx.ID_OK)
        pass

    def OnKeyDown(self, keyevent):
        keyPushed = keyevent.GetKeyCode()
        keyevent.Skip()
        if wx.WXK_NUMPAD_ADD== keyPushed:
            beep('plus')
            self.EndModal(wx.ID_OK)

class FrontEnd(BigBox):
    pass

class UnitTest():
    def __init__():
        pass
    def test1():
        pass

def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    thisconfig = JiuJiuConfig()
    # frontIns = FrontEnd("who are you?","yourName?",Config=thisconfig,AnsBoxSize=1)
    # frontIns.queryUser("Hello, man!\nNextLine\nNextLine\n435345\n435345\nDDDD\n")
    mainFrame = MainFrame()
    mainFrame.ShowFullScreen(True)
    frontIns = FrontEnd("who are you?","yourName?",Config=thisconfig,AnsBoxSize=1)
    frontIns.queryUser("Hello, man!\nNextLine\nNextLineDDDD\n")

