# coding=utf-8
#!/usr/bin/env python

import datetime;

class RecordClient():
    AskUserIdString = "������Ա����\n"
    UserDict = dict(a1="���ǳ�",a2="����ΰ",a3="��˽�",a4="�����")
    ShiftDict = dict(Morning="���",Middle="�а�",Night="���")
    MPdict = dict(a777888=("����1","����"),a999000=("����2","����"))
    ParmDict = {"aa":0,"bb":0,"cc":0,"ee":0}
    
    def __init__(self):
        #do some init..
        pass

    #Get username via userid
    def getUserId(self):
        self.userid = raw_input(self.AskUserIdString).strip()
        return self.userid

    def getUserName(self,id):
        #ToDo: exception
        return self.UserDict[id];

    def calculateShift(self):
        #ÿ��3�࣬8��00-16��00��16��00-24��00��24��00-8��00
        hour = datetime.datetime.now().hour
        if hour in range(9,17):
            return self.ShiftDict['Morning']
        if hour in range(17,23):
            return self.ShiftDict['Middle']
        if hour in range(0,9):
            return self.ShiftDict['Night']
        
    def scanbarcode(self):
        #Todo: add some timeout
        self.MPbarcode = raw_input("Please Scan Barcode!\n\t").strip()
        print "\t\t====Get Barcode:"+self.MPbarcode+"====\n"
        return self.MPbarcode

    def getMachineAndProduct(self):
        (M,P) = self.MPdict[self.scanbarcode()]
        return M,P

    def queryParms(self):
        for parm in self.ParmDict:
            self.ParmDict[parm] = raw_input("������"+parm+":\n\t")


    def updateDB(self):
            print "����д�����ݿ�.....\n"
            print "д�����ݿ���ɣ�\n"
 
    def printViaPrinter(self):
            print "���ڴ�ӡ\n"
            print "��ӡ�����ȡƱ\n"

if __name__ == '__main__':
    while True :
        try:
            is_name_confirmed = False
            while is_name_confirmed == False:
                this = RecordClient()
                UserId = this.getUserId()
                UserName = this.getUserName(UserId)
                if raw_input("��ȷ������(��=y,����=n)��" + UserName+"\n") == "y":
                    is_name_confirmed = True
                    
            is_MPS_confirmed = False
            while is_MPS_confirmed == False:         
                Machine, Product = this.getMachineAndProduct()
                print "=====��ȷ��������Ϣ====="
                print "����" + UserName+"\n"
                print "�����ţ�" + Machine +"\n"
                print "��Ʒ��" + Product +"\n"
                Shift = this.calculateShift()
                print "���" + Shift +"\n"
                if raw_input("(��=y)��" + UserName+"\n") == "y":
                    is_MPS_confirmed = True

            is_Parms_confirmed = False
            while is_Parms_confirmed == False:
                this.queryParms()
                print "=====��ȷ��������Ϣ,������������====="
                for each in this.ParmDict:
                    print each;
                if raw_input("(��ȷ=y)��" + UserName+"\n") == "y":
                    is_Parms_confirmed = True
            this.updateDB()
            this.printViaPrinter()

                
        #�쳣����
        except Exception as excep1:
            print "Error found ! please mailto:mscame@gmail.com"
            print type(Exception)
            print excep1.args
            
        
    
    
    
    
    
