# coding=utf-8
#!/usr/bin/env python
import wx
USERNAME = u"员工姓名"
USERID = u"员工号"
CLASS = "Class"
OTPLIST = [('picking',u"领料"),('storage',u"入库")]
SHIFTLIST = [u"早班",u"晚班",u"中班"]


RAWSTUFFLIST=['water','nano','atom']
PRODUCTLIST=['fire','nanp','ipod']


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


    def drawChoiceShift(self):
        shiftRadio = wx.Choice(self, -1, (85, 18), choices=SHIFTLIST) 
        #wx.RadioBox(self, -1, "", (10, 10), wx.DefaultSize,SHIFTLIST, 2, wx.RA_SPECIFY_COLS)
        self.shiftSizer = wx.BoxSizer(wx.VERTICAL)
        self.shiftSizer.Add(shiftRadio,1,wx.EXPAND)
        self.add_to_GuiObject(self.shiftSizer)
        
    def drawChoiceOpt(self):
#        self.optRadio = wx.RadioBox(self, -1, "", (10, 10), wx.DefaultSize,
        otpRadioList = []
        for (otpkey,otp) in OTPLIST:
            otpRadioList.append(wx.RadioButton(self, -1, otpkey, pos=(20, 80)))
        self.otpSizer = wx.BoxSizer(wx.HORIZONTAL)
        for radio in otpRadioList:
            self.otpSizer.Add(radio,1,wx.EXPAND)
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, radio)
        self.add_to_GuiObject(self.otpSizer)

    def drawInputTable(self):
#        self.inputTableSizer = wx.BoxSizer(wx.HORIZONTAL)
#        self.inputPanel = wx.Panel(self,-1,size=(800,600))
        self.inputsizer = wx.BoxSizer(wx.HORIZONTAL)
#        self.inputPanel.SetSizer(self.inputsizer)
        for item in RAWSTUFFLIST:
            text = wx.TextCtrl(self,-1,item,size=(100,-1))
            self.inputsizer.Add(text,1,wx.EXPAND)
#        self.inputTableSizer.Add(self.inputPanel,-1, wx.EXPAND)
        self.add_to_GuiObject(self.inputsizer)

    def OnRadio(self,event):
        radioSelected = event.GetEventObject()
#        self.inputPanel.SetBackgroundColour('Green')
#        self.inputPanel.Refresh()
#        sizer = self.inputPanel.GetContainingSizer()
        #self.inputPanel.Destroy()
        #sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inputsizer.Clear()
        if radioSelected.GetLabel() == "picking":
            DisplayList = RAWSTUFFLIST
        if radioSelected.GetLabel() == "storage":
            DisplayList = PRODUCTLIST
        for item in DisplayList:
            text = wx.TextCtrl(self,-1,item,size=(100,-1))
            self.inputsizer.Add(text,1,wx.EXPAND)
        self.inputsizer.Fit(self)
        self.MainSizer.Fit(self)
        #self.inputPanel.SetSizerAndFit(sizer,True)



#        self.inputTableSizer.Add(self.inputPanel,1, wx.EXPAND)
#        self.MainSizer.Add(self.inputTableSizer,1, wx.EXPAND)

        
    def drawUserInfo(self):
        self.userinfoSizer = wx.BoxSizer(wx.VERTICAL)
        self.userinfoSizer.Add(self.keyValueline(USERNAME,u"周星星"),1,wx.EXPAND)
        self.userinfoSizer.Add(self.keyValueline(USERID,u"007"),1,wx.EXPAND)
#        self.userinfoSizer.Add(self.keyValueline("XX","xx"),1,wx.EXPAND)
        self.add_to_GuiObject(self.userinfoSizer)
        

    def add_to_GuiObject(self,Obj):
        self.GuiObject.append(Obj)
        
    def __init__(self, parent,title):
        wx.Frame.__init__(self, parent, title=title, size=(1024,768))
        self.SetBackgroundColour("white") 
        # self.control = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.GuiObject = []
        self.initDraw()
        self.SetSizer(self.MainSizer)
        self.SetAutoLayout(True)
        self.MainSizer.Fit(self)
        #Don't comment this.
        #self.ShowFullScreen(True)
        self.Show(True)
        
newapp = wx.App(0)
frame = myFrame(None, 'helloword')
newapp.MainLoop()





