# coding=utf-8
#!/usr/bin/env python
import wx
USERNAME = u"员工姓名"
USERID = u"员工号"
CLASS = "Class"
OTPLIST = [('picking',[u"领料",("shit",0),("dash",0),("winship",0)]),('storage',[u"入库",("ipod",0),("ipad",0),("G1",0)])]
SHIFTLIST = [u"早班",u"晚班",u"中班"]


RAWSTUFFLIST=['water','nano','atom']
PRODUCTLIST=['fire','nanp','ipod']


class mappingSizer(wx.BoxSizer):
    def __init__(self,Key,Value):
        self = BoxSizer(wx.HORIZONTAL)
        wx.StaticText(self, label=Key)

class OptTable():
    def __init__(self,Parent,OptName,KeyValueList):
        self.Parent = Parent
        self.OptName = OptName
        self.OptKeyTextMapList = []
        self.GuiObjList = []
        ObjectRadio = wx.RadioButton(Parent, -1, OptName)
        Parent.Bind(wx.EVT_RADIOBUTTON, Parent.OnRadio, ObjectRadio)
        self.GuiObjList.append(ObjectRadio)
        for (ObjectName,Objectquantity) in KeyValueList:
            STextOjtNa = wx.StaticText(Parent,-1,label = ObjectName)
            CtextOjtQ = wx.TextCtrl(Parent, -1,str(Objectquantity))
            self.OptKeyTextMapList.append((ObjectName,(STextOjtNa.GetId(),CtextOjtQ.GetId())))
            tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
            tmp_sizer.Add(STextOjtNa,1,wx.EXPAND)
            tmp_sizer.Add(CtextOjtQ,1,wx.EXPAND)
            self.GuiObjList.append(tmp_sizer)
    #TODO  use self.Parent to replace Parent
    def Sizer(self,Parent):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        for eachitem in self.GuiObjList:
            self.sizer.Add(eachitem,1,wx.ALIGN_CENTER)
        self.Enable(Parent,False)
        return self.sizer
    #TODO  use self.Parent to replace Parent
    def Enable(self,Parent,TrueorFalse):
        for (objname,(id1,inputId)) in self.OptKeyTextMapList:
            Parent.FindWindowById(inputId).Enable(TrueorFalse)
    


class myFrame(wx.Frame):
    def keyValueline(self,Key,Value):
        TmpBox = wx.BoxSizer(wx.HORIZONTAL)
        KeyText = wx.StaticText(self, label=Key)
        ValueText = wx.StaticText(self, label=Value)
        TmpBox.Add(KeyText,1, wx.ALIGN_CENTER)
        TmpBox.Add(ValueText,1,wx.ALIGN_CENTER)
        TmpBox.Fit(self)
        return TmpBox

    def initDraw(self):
        self.drawUserInfo()
        self.drawChoiceShift()
        self.drawChoiceOpt()
        #self.drawInputTable()
        for obj in self.GuiObject:
            self.MainSizer.Add(obj,1, wx.EXPAND)


    def drawChoiceShift(self):
        shiftRadio = wx.Choice(self, -1, choices=SHIFTLIST)
        shiftRadio.SetBackgroundColour("Red")
        #wx.RadioBox(self, -1, "", (10, 10), wx.DefaultSize,SHIFTLIST, 2, wx.RA_SPECIFY_COLS)
        self.shiftSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.shiftSizer.Add(shiftRadio,1,wx.EXPAND)
        self.add_to_GuiObject(self.shiftSizer)
        
    def drawChoiceOpt(self):
        self.ChoicesOptTables = []
        self.otpSizer = wx.BoxSizer(wx.HORIZONTAL)            
        for (EachObj,MTlist) in OTPLIST:
            tmpTable = OptTable(self,MTlist[0],MTlist[1:])
            self.otpSizer.Add(tmpTable.Sizer(self),1,wx.EXPAND)
            self.ChoicesOptTables.append(tmpTable)
        self.add_to_GuiObject(self.otpSizer)
            
#        self.optRadio = wx.RadioBox(self, -1, "", (10, 10), wx.DefaultSize,
        # otpRadioList = []
        # self.otpObjectdict = {}
        # for (otpkey,otp) in OTPLIST:
        #     tmpRadioSizer = wx.BoxSizer(wx.VERTICAL)
        #     optRadio = wx.RadioButton(self, -1, otp[0])
        #     tmpRadioSizer.Add(optRadio,1,wx.EXPAND)
        #     for item in otp[1:]:
        #         text = wx.TextCtrl(self,-1,item,size=(100,-1))
        #         text.Enable(False)
        #         tmpRadioSizer.Add(text,1,wx.EXPAND)
        #     otpRadioList.append(tmpRadioSizer)
        # self.otpSizer = wx.BoxSizer(wx.HORIZONTAL)
        # for radio in otpRadioList:
        #     self.otpSizer.Add(radio,1,wx.EXPAND)
        #     #self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, radio)


#     def drawInputTable(self):
# #        self.inputTableSizer = wx.BoxSizer(wx.HORIZONTAL)
# #        self.inputPanel = wx.Panel(self,-1,size=(800,600))
#         self.inputsizer = wx.BoxSizer(wx.HORIZONTAL)
# #        self.inputPanel.SetSizer(self.inputsizer)
#         for item in RAWSTUFFLIST:
#             text = wx.TextCtrl(self,-1,item,size=(100,-1))
#             self.inputsizer.Add(text,1,wx.EXPAND)
# #        self.inputTableSizer.Add(self.inputPanel,-1, wx.EXPAND)
#         self.add_to_GuiObject(self.inputsizer)

    def OnRadio(self,event):
        radioSelected = event.GetEventObject()
        radiotext = radioSelected.GetLabel()
        for otpTable in self.ChoicesOptTables:
            if radiotext == otpTable.OptName:
                otpTable.Enable(self,True)
            else:
                otpTable.Enable(self,False)
            
        
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
        self.Centre()
        self.Show(True)
        
newapp = wx.App(0)
frame = myFrame(None, 'helloword')
newapp.MainLoop()





