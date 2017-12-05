#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 10:49:29 2017

@author: fboers

update 21.08.2017 fb
"""

import warnings
import os,time,glob,serial
import numpy as np

__version__='2017-09-05.001'

class JuMEG_Psycho_EventCode(object):
      def __init__(self,port='/dev/ttyACM0',baudrate=115200,startcode=128,duration_ms=200,duration_seq_ms=10,verbose=False):
          """ sending digital eventcodes (TTL) via Arduino (MEGA)
              default setings (LINUX):
                      baudrate    = 115200
                      duration_ms = 200
                      startcode   = 128
                      port        = '/dev/ttyACM0'
                      -> will find arduino port via VENDOR_ID_CODE (123)
              https://github.com/wiseman/arduino-serial/blob/master/arduinoserial.py
              https://github.com/vascop/Python-Arduino-Proto-API-v2/blob/master/arduino/arduino.py
          """
          self.__baudrate_list=( ['9600','19200','38400','57600','115200','230400','500000','576000','921600','1000000','1152000',
                                  '1500000','2000000','2500000','3000000','3500000','4000000'])
          self.__comport_list = []

          #--- parameter
          self.__param={
                        'ComPort':port,'baudrate':baudrate,'port_pattern':'/dev/ttyACM[0-9]*',
                        'find_port':True,
                        'duration_ms':duration_ms,'duration_seq_ms':duration_seq_ms,'startcode':startcode, 
                        'vendor_id_code':123,'vendor_id_repetition':7,
                        'send_byte_code':True,'verbose': verbose,
                        'cmd_code_switch_on' : 111,
                        'cmd_code_switch_off': 112,
                        'cmd_code_send_seq'  : 211,
                        'test_seq_code'      : '211,1000,255,128,64,32,16,8,4,2,1,2048,1024,512,256'
                       }

          self.__serial     = None
          self.__byte_array_size = 7
          self.verbose      = False
          
          self.__isConnected= False
         
            
      def __str__(self):
          return "Arduino is on port %s at %d baudrate" %(self.ComPort,self.serial.baudrate)

      def __del__(self):
          if self.isConnected:
             self.close()  
    
#--- Getter / Setter / Properties
      def __get_baudrate_list(self):
          return self.__baudrate_list
      baudrate_list=property(__get_baudrate_list)
    #---  
      def __get_comport_list(self):
          self.__comport_list = glob.glob( self.port_pattern )   
          print" --> checking ports for Arduino-Event/Trigger-Code: "
          print" --> port pattern: " +self.port_pattern
          print self.__comport_list
          return self.__comport_list
      
      comport_list = property(__get_comport_list)
    #---
      def __get_isConnected(self):
          return self.__isConnected
      isConnected = property(__get_isConnected)
     
    #---  
      def __get_param(self):
          return self.__param     
      def __set_param(self,v):
          self.__param=v     
      parameter = property(__get_param,__set_param)    
    #---
      def __get_Serial(self):
          return self.__serial
      serial = property(__get_Serial)  
    #---
      def __get_ComPort(self):
          return self.__param['ComPort']
      def __set_ComPort(self,v):
          self.__param['ComPort']=v
      ComPort=property(__get_ComPort,__set_ComPort)
    #---
      def __get_port_pattern(self):
          return self.__param['port_pattern']
      def __set_port_pattern(self,v):
          self.__param['port_pattern']=v
      port_pattern=property(__get_port_pattern,__set_port_pattern)
    #---
      def __get_baudrate(self):
          return self.__param['baudrate']
      def __set_baudrate(self,v):
          self.__param['baudrate']=v
      baudrate=property(__get_baudrate,__set_baudrate)
    #---
      def __get_duration_ms(self):
          return self.__param['duration_ms']
      def __set_duration_ms(self,v):
          self.__param['duration_ms']=v
      duration_ms=property(__get_duration_ms,__set_duration_ms)
    #---
      def __get_duration_seq_ms(self):
          return self.__param['duration_seq_ms']
      def __set_duration_seq_ms(self,v):
          self.__param['duration_seq_ms']=v
      duration_seq_ms=property(__get_duration_seq_ms,__set_duration_seq_ms)
    #---
      def __get_startcode(self):
          return self.__param['startcode']
      def __set_startcode(self,v):
          self.__param['startcode']=v
      startcode=property(__get_startcode,__set_startcode)
    #---
      def __get_vendor_id_code(self):
          return self.__param['vendor_id_code']
      def __set_vendor_id_code(self,v):
          self.__param['vendor_id_code']=v
      vendor_id_code=property(__get_vendor_id_code,__set_vendor_id_code)
    #---
      def __get_vendor_id_repetition(self):
          return self.__param['vendor_id_repetition']
      def __set_vendor_id_repetition(self,v):
          self.__param['vendor_id_repetition']=v
      vendor_id_repetition=property(__get_vendor_id_repetition,__set_vendor_id_repetition)
    #---
      def __get_send_byte_code(self):
          return self.__param['send_byte_code']
      def __set_send_byte_code(self,v):
          self.__param['send_byte_code']=v
      send_byte_code=property(__get_send_byte_code,__set_send_byte_code)
    #---
      def __get_cmd_code_switch_on(self):
          return self.__param['cmd_code_switch_on']
      def __set_cmd_code_switch_on(self,v):
          self.__param['cmd_code_switch_on']=v
      cmd_code_switch_on=property(__get_cmd_code_switch_on,__set_cmd_code_switch_on)
    #---
      def __get_cmd_code_switch_off(self):
          return self.__param['cmd_code_switch_off']
      def __set_cmd_code_switch_off(self,v):
          self.__param['cmd_code_switch_off']=v
      cmd_code_switch_off=property(__get_cmd_code_switch_off,__set_cmd_code_switch_off)
    #---
      def __get_cmd_code_send_seq(self):
          return self.__param['cmd_code_send_seq']
      def __set_cmd_code_send_seq(self,v):
          self.__param['cmd_code_send_seq']=v
      cmd_code_send_seq=property(__get_cmd_code_send_seq,__set_cmd_code_send_seq)
    #---
      def __get_verbose(self):
          return self.__param['verbose']
      def __set_verbose(self,v):
          self.__param['verbose']=v
      verbose=property(__get_verbose,__set_verbose)
     #---
      def __get_test_seq_code(self):
          return self.__param['test_seq_code']
      def __set_test_seq_code(self,v):
          self.__param['test_seq_code']=v
      test_seq_code=property(__get_test_seq_code,__set_test_seq_code)   
     #---     
      def calc_vendor_id_code_array(self):
          return np.zeros( self.vendor_id_repetition,dtype=np.byte)+self.vendor_id_code
     #---
      def __get_find_port(self):
          return self.__param['find_port']
      def __set_find_port(self,v):
          self.__param['find_port']=v
      find_port=property(__get_find_port,__set_find_port)
    
      
#----------------    
          
      def __open(self,port=None,baudrate=None):
          if port:
             self.ComPort = port     
          if baudrate:
             self.baudrate = baudrate     
          print"---> Open: Event/Trigger Code connection ..."
          print' --> Arduino start open connection'
          print'  -> port: ' + self.ComPort + ' baudrate: '+ str(self.baudrate)
          self.__close_comport()
          try:
              self.__serial = serial.Serial(self.ComPort,int(self.baudrate))       
              time.sleep(2)
              if self.__serial:
                 self.__isConnected=True
              print '---> done Arduino is connected\n'
          except:
              warnings.warn('---> EEROR can not connected to Arduino !!!\n')
              self.__isConnected=False 
              return False
      
      def open(self,port=None,baudrate=None):
          if port:
             self.ComPort = port     
          if baudrate:
             self.baudrate = baudrate 
          
          if self.find_port:
             self.findArduinoPort()
          else:   
             self.__open()
             
          if self.isConnected:
             self.serial.flushInput()
             self.serial.flushOutput()
             self.sendSwitchOff() 
          return self.isConnected

      def __close_comport(self):
          try:
              if self.isConnected:
                 self.sendSwitchOff() 
                 time.sleep(1)
                 self.serial.close()
                 time.sleep(1)
                 self.__isConnected = False
                 print '---> done Arduino connection closed\n'          
          except:
                 self.__isConnected = False
                 
      def close(self):
          print"---> Close: Event/Trigger Code connection ..."
          print" --> Arduino closing connection ..."
          self.__close_comport()
        
      def getIdCode(self):
          """ 
              check if <event/trigger code arduino> is connected to the port
              return arduino vendor id e.g: 123 for 7 times
          """ 
          self.write_bytes( bytearray( self.calc_vendor_id_code_array() ) ) 
          time.sleep(1)
          id = self.serial.readline()
          time.sleep(1)
          self.serial.flushOutput()
          if self.verbose:
             print " -->ID code : %d"%(int(id)) 
          return int(id)
       
      def findArduinoPort(self):
          ports = glob.glob( self.port_pattern )   
          print" --> Find Arduino Port Event/Trigger-Code: "
          print" --> checking ports ..."
          print ports
          
          for port in ports:
              try:
                  self.__open(port=port)
                  self.serial.timeout=1.0
                  if self.isConnected:
                     id = self.getIdCode()
                     if ( id == self.vendor_id_code ):
                        print " --> found Arduino@Port: " + self.ComPort +" -> Vendor ID: %d" %(id)
                        self.serial.timeout=None
                        return self.ComPort
                     else:
                        self.close() 
              except:
                 self.__isConnected = False
                 print '!!! ---> ERROR in connecting to port: '+ port 
          return self.isConnected
         
      def write_bytes(self,v):
          if self.__isConnected:
           # d=bytes(bytearray([111,255,255,0,0,0,0])  
             self.serial.write(bytes(v))
             self.serial.flushOutput()
          else:
             print"  ->ERROR write bytes to Arduino => Serial conncetion is closed\n"
             
      def number2byte( self,v ):
          """ 
             input  : int
             output : numpy byte array size:4 
             example: 2048+255 => [255,8,0,0]
          """   
          b  = np.zeros(4,dtype=np.uint8)
          mask = np.uint8(255)
          b[0] = v & mask
          b[1] = (v >>  8) & mask
          b[2] = (v >> 16) & mask
          b[3] = (v >> 24) & mask
          return b
      
      def send(self,eventcode=0,duration_ms=-1): 
           
          if not eventcode:
             eventcode = 0
             
          if duration_ms ==-1:
             duration_ms = self.duration_ms 
         #--- send as byte 
          if self.send_byte_code:
             db      = np.zeros( self.__byte_array_size,dtype=np.uint8)
             db[0]   = self.cmd_code_switch_on
             db[1:3] = self.number2byte(eventcode)[0:2]
             db[3:]  = self.number2byte(duration_ms)
             #print "test"
             #print db
            #db=bytes(bytearray([111,255,255,0,0,0,0])
             self.write_bytes( bytearray( db ) )
             if self.verbose:
                print"---> DONE Send: "
                print"  -> eventcode %d" % (eventcode)
                print"  -> duration [ms] %d" % (duration_ms)
                #print bytearray(db)
                print"\n"
          else:
         #--- send as string  no bytearray(t implemented !!!! 
             print" -->Warning Arduino setup can only read bytes!!!\n"
              # self.write( self.__SWITCH_ON_CODE_STR+','+str(eventcode)+','+str(duration_ms) + ',0' )
              
      def sendEventCode(self,eventcode=0,duration_ms=-1) :
          self.send(eventcode=eventcode,duration_ms=duration_ms)
          
      def sendSeq(self,seq=None,duration_seq_ms=-1):
          '''
          send event code seq 
          cmd,number of codes, codes low,high byte .., duration 2 byte
          '''
          if not seq:
              return
          
          if duration_seq_ms ==-1:
             duration_seq_ms = self.duration_seq_ms 
     #--- send as byte 
          if self.send_byte_code:
            #--- arduino 7 byte offset for usual cmds 
             mask     = np.uint8(255)
             seq_ar   = np.array([seq],dtype=np.int).flatten()
             cnt      = len(seq)
             db       = np.zeros(7 + cnt*2,dtype=np.uint8)
             db[0]    = self.cmd_code_send_seq
             db[1]    = np.uint8(cnt*2) # 2 x cnt -> Low/High bytes->Eventcode & Trigger             
             db[3:7]  = self.number2byte( duration_seq_ms) # 6,7 = 0
             db[7::2] = seq_ar & mask 
             db[8::2] = (seq_ar >> 8 ) & mask
           
             self.write_bytes( bytearray(db) ) 
             if self.verbose:
                print"---> DONE send SEQ: "
                print seq             
                print db             
                print"\n"
           
      def sendCmdList(self,cmd_str):
          print" --> send cmd list:"
          print"  -> "+ cmd_str
          cmd = [int(i) for i in cmd_str.split(',')]
          if cmd[0] == self.cmd_code_switch_on:
             dt=-1
             if len(cmd)>2: 
                dt=cmd[2]
             self.send(eventcode=cmd[1],duration_ms=dt)
          elif cmd[0] == self.cmd_code_send_seq:
             self.sendSeq(seq=cmd[2:],duration_seq_ms=cmd[1])
            
          elif cmd[0] == self.cmd_code_switch_off:
             self.sendSwitchOff()        
         
      def sendStartCode(self,startcode=None,duration_ms=-1):
          if not startcode:
             startcode=self.startcode 
          self.send(eventcode=startcode,duration_ms=duration_ms) 
          if self.verbose:
             print " --> DONE send start code: %d" %(startcode)   
        
      def sendTestSEQCode(self,code=None,trigger=None,duration_ms=0):
          self.sendCmdList( str(self.cmd_code_send_seq) +','+ self.test_seq_code )
        
          if self.verbose:
             print " --> DONE send Test SEQ Code: " +self.test_seq_code    
         
      def sendSwitchOff(self):
          """https://stackoverflow.com/questions/31975356/python-arduino-serial-communication"""
          self.write_bytes(bytearray([self.cmd_code_switch_off,0,0,0,0,0,0]) )           
          if self.verbose:
             print " --> DONE send StopCode & switch off"   
      def sendStopCode(self):
          self.sendSwitchOff()   
        
'''
ipy test

from psycho.hardware.jumeg_psycho_eventcode import JuMEG_Psycho_EventCode
evc=JuMEG_Psycho_EventCode()
evc.findArduinoPort()


import serial
com=serial.Serial('/dev/ttyACM0',115200)
com.flush()
-> send code trigger:255 response:255
don=bytes(bytearray([111,255,255,0,0,0,0]))
com.write(don)
-> switch off
doff=bytes(bytearray([112,0,0,0,0,0,0]))
com.write(doff)

-> vendor id
vid=bytes(bytearray([123,123,123,123,123,123,123]))
com.write(vid)
com.readline()
-> out : '123\r\n'

id=np.zeros(7,dtype=np.byte)+123
bvid=bytes(bytearray(id))
com.write(bvid)
com.readline()
-> out : '123\r\n'
'''
