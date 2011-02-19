# -*- coding: utf-8 -*-
from ctypes import *
import os,sys,traceback,time

BLOCK_ID = 3
BLOCK_NAME = 5
BLOCK_TIMETAG = 55



class M1CardReader():
    def __init__(self,PortNumber):
        self.portNum = PortNumber
        windll.LoadLibrary('d:\wsr.dll')
        f = c_float()
        windll.wsr.ws_getPort(self.portNum,byref(f))
        self.icdev = f

    def reset_card(self):
        self.reset_Counter()
        
    def update_time_tag(self):
        Tag = str(time.time())
        return self.write_block_data(BLOCK_TIMETAG,Tag);
    
    def get_time_tag(self):
        return self.read_block_data(BLOCK_TIMETAG)
        
    def open_port(self):
        windll.wsr.ws_openPort(self.portNum)

    def close_port(self):
        windll.wsr.ws_closePort(self.portNum)

    def beep(self):
        windll.wsr.ws_beep(self.portNum)

    def set_password(self,pwd):
        self.pwd = pwd

    def apply_password(self):
        windll.wsr.ws_loadKey(self.portNum,c_char_p(self.pwd),0)
        windll.wsr.ws_loadKey(self.portNum,c_char_p(self.pwd),1)

    def get_card_number(self):
        CP_cardNum = create_string_buffer(10)
        if 1 == windll.wsr.ws_getCardNo_String(self.portNum,byref(CP_cardNum)):
            self.cardNum=CP_cardNum.value
            return self.cardNum
        else:
            return ""
        
    def read_block_data(self,Block):
        CP_DATA = create_string_buffer(16)
        self.apply_password()
        if 1 == windll.wsr.ws_readBlock(self.portNum,Block,byref(CP_DATA)):
                    return CP_DATA.value
        else:
            return ""

    def write_block_data(self,Block,Value):
        if Block in range(3,64,4):
            print "Not allow to write password block:"+ str(Block)
        Input = c_char_p(Value)
        Len = len(Value)
        if  Len > 16:
            print "DATA too long!"
            return False
        self.apply_password()
        Result = windll.wsr.ws_writeBlock(self.portNum,Block,Input)
        if 1 == Result:
            return True
        else:
            print Result
            return False

    def set_name_and_id(self,Name,Id):
        result1 = self.write_block_data(BLOCK_ID,Id)
        
        result2 = self.write_block_data(BLOCK_NAME,Name)
        if result1 and result2:
            self.beep()
            return True
            
        else:
            return False
        
    def get_name_and_id(self):
        return self.read_block_data(BLOCK_NAME),  self.read_block_data(BLOCK_ID)
    
    def get_name(self):
        return self.read_block_data(BLOCK_NAME)

    def get_id(self):
        return self.read_block_data(BLOCK_ID)

        

if __name__ == "__main__":
    this = M1CardReader(2)
    try:
         pwd = "\xFF\xFF\xFF\xFF\xFF\xFF"
         this.open_port()
         print this.get_card_number()
         this.set_password(pwd)
         print this.read_block_data(1)
         if not this.write_block_data(1,"tt"):
             print "write fault"
         print this.read_block_data(1)
         print this.read_block_data(2)
         
         if this.set_name_and_id("You3!","7530"):
            print "================="
            print this.get_name_and_id()
            print "+++++++++++++++"
            print this.get_id()
         
         
         else:
             print "Cannot set Name or Id"
         this.update_time_tag()
         print this.get_time_tag()
         
         
    except Exception:
        exceptionTraceback = sys.exc_info()
        traceback.print_exc(file=sys.stdout)
    
    this.close_port()
    
    
