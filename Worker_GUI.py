# coding=gbk
#!/usr/bin/env python
import wx
USERNAME = u"员工姓名"

USERID = "USER ID"
CLASS = "Class"
OTPLIST = ["Picking","Store"]
SHIFTLIST = ["Morning","Night","Afternoon"] 
class mappingSizer(wx.BoxSizer):
    def __init__(self,Key,Value):
        self = BoxSizer(wx.HORIZONTAL)
        wx.StaticText(self, label=Key)
    

class myFrame(wx.Frame):
    def keyValueline(self,Key,Value):
        TmpBox = wx.BoxSizer(wx.HORIZONTAL)
        KeyText = wx.StaticText(self, label=Key)
        ValueText = wx.StaticText(self, label=Value)
        TmpBox.Add(KeyText,1, wx.EXPAND)
        TmpBox.Add(ValueText,1,wx.EXPAND)
        TmpBox.Fit(self)
        return TmpBox

    def initDraw(self):
        self.drawUserInfo()
        self.drawChoiceShift()
        self.drawChoiceOpt()
        self.drawInputTable()
        for obj in self.GuiObject:
            self.MainSizer.Add(obj,1, wx.EXPAND)

    def drawInputTable(self):
        self.inputTableSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Text1 = wx.TextCtrl(self, -1, "")
        self.Text1.Enable(True)
        self.inputTableSizer.Add(self.Text1,1, wx.EXPAND)
        self.add_to_GuiObject(self.inputTableSizer)

    def drawChoiceShift(self):
        shiftRadio = wx.Choice(self, -1, (85, 18), choices=SHIFTLIST) 
        #wx.RadioBox(self, -1, "", (10, 10), wx.DefaultSize,SHIFTLIST, 2, wx.RA_SPECIFY_COLS)
        self.shiftSizer = wx.BoxSizer(wx.VERTICAL)
        self.shiftSizer.Add(shiftRadio,1,wx.EXPAND)
        self.add_to_GuiObject(self.shiftSizer)
        
    def drawChoiceOpt(self):
#        self.optRadio = wx.RadioBox(self, -1, "", (10, 10), wx.DefaultSize,
        otpRadioList = []
        for otp in OTPLIST:
            otpRadioList.append(wx.RadioButton(self, -1, otp, pos=(20, 80)))
        self.otpSizer = wx.BoxSizer(wx.VERTICAL)
        for radio in otpRadioList:
            self.otpSizer.Add(radio,1,wx.EXPAND)
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, radio)
        self.add_to_GuiObject(self.otpSizer)

    def OnRadio(self,event):
        radioSelected = event.GetEventObject() 
             #text = self.texts[radioSelected.GetLabel()]
#             if radioSelected.GetLabel == "Picking":
        self.Text1.SetValue(radioSelected.GetLabel())
#        self.selectedText = text 
        
    def drawUserInfo(self):
        self.userinfoSizer = wx.BoxSizer(wx.VERTICAL)
        self.userinfoSizer.Add(self.keyValueline(USERNAME,"bb"),1,wx.EXPAND)
        self.userinfoSizer.Add(self.keyValueline(USERID,"aa"),1,wx.EXPAND)
#        self.userinfoSizer.Add(self.keyValueline("XX","xx"),1,wx.EXPAND)
        self.add_to_GuiObject(self.userinfoSizer)

    def add_to_GuiObject(self,Obj):
        self.GuiObject.append(Obj)
        
    def __init__(self, parent,title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.SetBackgroundColour("white") 
        # self.control = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.GuiObject = []
        self.initDraw()
        self.SetSizer(self.MainSizer)
        self.SetAutoLayout(True)
        self.MainSizer.Fit(self)
        #self.ShowFullScreen(True)
        self.Show(True)
        
newapp = wx.App(False)
frame = myFrame(None, 'helloword')
newapp.MainLoop()





