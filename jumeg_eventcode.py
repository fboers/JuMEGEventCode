#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 12:08:10 2017

@author: fboers
      
   
"""



import wx
try:
    from psycho.hardware.jumeg_psycho_eventcode       import JuMEG_Psycho_EventCode
    from psycho.wxutils.jumeg_psycho_wxutils_controls import JuMEG_wxControlButtons,JuMEG_wxControls,JuMEG_wxControlCheckButtons
except:
    from hardware.jumeg_psycho_eventcode       import JuMEG_Psycho_EventCode
    from wxutils.jumeg_psycho_wxutils_controls import JuMEG_wxControlButtons,JuMEG_wxControls,JuMEG_wxControlCheckButtons

__version__='2018-02-22.001'

class JuMEG_wxPsychoEventCode(wx.Panel):
  
    def __init__(self,*kargs, **kwargs):
        super(JuMEG_wxPsychoEventCode, self).__init__(*kargs, **kwargs)          
        
        self.label='EventCode'
        self.SetBackgroundColour('white')
        
        self.EventCode = JuMEG_Psycho_EventCode()
        
        """
        self.__param={
                        'ComPort':port,'baudrate':baudrate,
                        'duration_ms':duration_ms,'startcode':startcode, 
                        'vendor_id_code':123,'vendor_id_repetition':7, 'vendor_port_string':'dev/ttyACM[0-9]*',
                        'send_byte_code':True,'verbose': verbose,
                        'cmd_code_switch_on' : 111,
                        'cmd_code_switch_off': 112,
                        'cmd_code_send_seq'  : 211
                         }
        """
       #---          
        self.comport_list = [
             ("COMBO","COM Port",self.EventCode.ComPort, self.EventCode.comport_list, self.OnClick),
             ("COMBO","Baudrate",str(self.EventCode.baudrate),self.EventCode.baudrate_list,self.OnClick),
             ("TXT",  "Pattern", self.EventCode.port_pattern,None,None) ]
        self.vendor_list = [
             ("SP","ID",        [1,255],self.EventCode.vendor_id_code,self.OnClick),
             ("SP","Repetition",[1,10],self.EventCode.vendor_id_repetition,self.OnClick)]
        self.cmd_list = [
             ("SP","Switch On", [1,255],self.EventCode.cmd_code_switch_on, self.OnClick),
             ("SP","Switch Off",[1,255],self.EventCode.cmd_code_switch_off,self.OnClick),
             ("SP","Send SEQ",  [1,255],self.EventCode.cmd_code_send_seq,  self.OnClick)]             
      #---  
        self.option_list = [
             ("SP","Start Code",   [1,2048,1],  self.EventCode.startcode,  self.OnClick),     
             ("SP","Duration [ms]",[1,20000,10],self.EventCode.duration_ms,self.OnClick)]     
       
        
        self.flag_list = [("CK","Byte Code",self.EventCode.send_byte_code,self.OnCkBox ),
                          ("CK","Find Port",self.EventCode.find_port,     self.OnCkBox ),
                          ("CK","Verbose",  self.EventCode.verbose,       self.OnCkBox )]             
        
        self.COM = JuMEG_wxControls(self,label="Com Port",    control_list=self.comport_list )  
        self.VED = JuMEG_wxControls(self,label="Vendor ID",   control_list=self.vendor_list )  
        self.CMD = JuMEG_wxControls(self,label="Command Code",control_list=self.cmd_list )  
        
        self.OPT = JuMEG_wxControls(self,label="Options",  control_list=self.option_list)
        
        self.CKB = JuMEG_wxControlCheckButtons(self,label="Flags",control_list=self.flag_list)  
      
      #--- click on radio button andsend this bit    
        bit_list = ['','D0','D1','D2','D3','D4','D5','D6','D7']
        self.pnl_rgb_trigger = wx.Panel(self,style=wx.SUNKEN_BORDER) 
        self.RB_TRIGGER      = wx.RadioBox(self.pnl_rgb_trigger,label = 'SEND Trigger   Bit',choices = bit_list ,majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        self.RB_TRIGGER.Bind(wx.EVT_RADIOBOX,self.ClickOnRBTrigger)
        self.RB_TRIGGER.SetSelection(0)
      #--- 
        self.pnl_rgb_eventcode = wx.Panel(self,style=wx.SUNKEN_BORDER)
        self.RB_EVENTCODE      = wx.RadioBox(self.pnl_rgb_eventcode,label = 'SEND EventCode Bit',choices = bit_list ,majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        self.RB_EVENTCODE.Bind(wx.EVT_RADIOBOX,self.ClickOnRBEventcode)
        self.RB_EVENTCODE.SetSelection(0)
        
      #---ComPort buttons Open/Close & Update
        self.pnl_bt_comport  = wx.Panel(self.COM,style=wx.SUNKEN_BORDER)
        
        self.BtComPortOpenClose = wx.ToggleButton(self.pnl_bt_comport,id=wx.ID_NEW,label='Open')
        self.BtComPortUpdate    = wx.Button(self.pnl_bt_comport,id=wx.ID_NEW,label='Update')
        
        self.BtComPortOpenClose.Bind(wx.EVT_TOGGLEBUTTON, self.ClickOnComPortOpenClose,id=self.BtComPortOpenClose.GetId())
        self.BtComPortUpdate.Bind(wx.EVT_BUTTON, self.ClickOnComPortUpdate,id=self.BtComPortUpdate.GetId())

      #--- send button and cmd txt ctrl
        self.pnl_bt_send = wx.Panel(self,style=wx.SUNKEN_BORDER)  
        self.BtSendStartCode = wx.Button(self.pnl_bt_send,id=wx.ID_NEW,label='Start Code')
        self.BtSendStartCode.Bind(wx.EVT_BUTTON,self.ClickOnSendCode,id=self.BtSendStartCode.GetId())
        self.BtSendStopCode = wx.Button(self.pnl_bt_send,id=wx.ID_NEW,label='Stop Code')
        self.BtSendStopCode.Bind(wx.EVT_BUTTON,self.ClickOnSendCode,id=self.BtSendStopCode.GetId())
        
        self.BtSendTestCode = wx.Button(self.pnl_bt_send,id=wx.ID_NEW,label='Test Code')
        self.BtSendTestCode.Bind(wx.EVT_BUTTON,self.ClickOnSendCode,id=self.BtSendTestCode.GetId())
        
        self.BtSendCMD   = wx.Button(self.pnl_bt_send,id=wx.ID_NEW,label='SEND CMD')
        self.BtSendCMD.Bind(wx.EVT_BUTTON,self.ClickOnSendCMD,id=self.BtSendCMD.GetId())
        self.TxtSendCMD = wx.TextCtrl(self.pnl_bt_send,wx.NewId() )   
        self.TxtSendCMD.SetValue('211,1000,255,128,64,32,16,8,4,2,1,2048,1024,512,256')
        
        self.__ApplyLayout()   
  
    def ClickOnRBEventcode(self,evt=None): 
        if self.RB_EVENTCODE.GetSelection() > 0:
           code = 2**(self.RB_EVENTCODE.GetSelection()-1)
        else:
           code = 0 
        print" ---> send EventCode bit: "+ self.RB_EVENTCODE.GetStringSelection() +" -> %d" %(2**self.RB_EVENTCODE.GetSelection())
        self.ClickOnSendCode( code=2**self.RB_EVENTCODE.GetSelection() )
        
    def ClickOnRBTrigger(self,evt=None):
        if self.RB_TRIGGER.GetSelection() > 0:
           code = 2**(self.RB_TRIGGER.GetSelection() +8-1)
        else:
           code = 0 
        print" ---> send TriggerCode bit: "+ self.RB_TRIGGER.GetStringSelection() +" -> %d" %(code)
        self.ClickOnSendCode( code = code )
        
    def ClickOnSendCode(self,evt=None,code=None): 
        if self.EventCode.isConnected:
          
           if code:
              self.EventCode.sendEventCode(code)
              print"Done send: %d" % (code)
              print
           elif evt.GetEventObject().GetLabel().startswith('Start'):
              self.EventCode.sendStartCode()
           elif evt.GetEventObject().GetLabel().startswith('Stop'):
              self.EventCode.sendStopCode()
           elif evt.GetEventObject().GetLabel().startswith('Test'):
              self.EventCode.sendTestSEQCode()
           
        else:    
           wx.MessageBox('Arduino not connected! connect and open', 'Error', 
           wx.OK | wx.ICON_ERROR)
           
    def ClickOnSendCMD(self,evt=None): 
        if self.EventCode.isConnected:
           self.EventCode.sendCmdList(self.TxtSendCMD.GetValue())
        else:    
           wx.MessageBox('Arduino not connected! connect and open', 'Error', 
           wx.OK | wx.ICON_ERROR)
       
    
    def ClickOnComPortOpenClose(self,evt=None): 
        print"ClickOnComPortOpenClose"
        state = evt.GetEventObject().GetValue() 
        
        if state == True: #---open com
           
        #--open & disable combos 
           for obj in self.COM.controls:
               if isinstance(obj, wx.ComboBox): 
                  if obj.GetName().startswith('COM Port'):
                     self.EventCode.ComPort= obj.GetValue()
                  elif obj.GetName().startswith('Baudrate'):
                     self.EventCode.baudrate= obj.GetValue()         
                 # obj.Enable(False)          
        #--- open    
           self.EventCode.open()
           for obj in self.COM.controls:
               if obj.GetName().startswith('COM Port'):
                  obj.SetValue( self.EventCode.ComPort )
                  break
           evt.GetEventObject().SetLabel("Close") 
           
        else: #--- close com
           self.EventCode.close()
           for obj in self.COM.controls:
              if isinstance(obj, wx.ComboBox): 
                 obj.Enable(True)
           evt.GetEventObject().SetLabel("Open")
          
    def ClickOnComPortUpdate(self,evt=None): 
        obj_port = None
        for obj in self.COM.controls:
            if isinstance(obj, wx.TextCtrl): 
               if obj.GetName().startswith('Pattern'):
                  self.EventCode.port_pattern = obj.GetValue()
            elif isinstance(obj, wx.ComboBox): 
               if obj.GetName().startswith('COM Port'):
                  obj_port = obj                   
        obj_port.SetItems( self.EventCode.comport_list )
        obj_port.SetValue( self.EventCode.findArduinoPort() )
        
        
        
    def OnClick(self,evt):
        obj = evt.GetEventObject()
      #--- com port 
        if obj.GetLabel().startswith("Com Port"):
             self.EventCode.ComPort  = obj.GetValue()
        elif obj.GetLabel().startswith("Baudrate"):
             self.EventCode.baudrate = int( obj.GetValue() )
      #---       
        elif obj.GetLabel().startswith("ID"):
             self.EventCode.vendor_id_code = int( obj.GetValue() )
        elif obj.GetLabel().startswith("Repetition"):
             self.EventCode.vendor_id_repetition = int( obj.GetValue() )
      #---       
        elif obj.GetLabel().startswith("Switch On"):
             self.EventCode.cmd_code_switch_on = int( obj.GetValue() )
        elif obj.GetLabel().startswith("Switch Off"):
             self.EventCode.cmd_code_switch_off = int( obj.GetValue() )
        elif obj.GetLabel().startswith("Send SEQ"):
             self.EventCode.cmd_code_send_seq = int( obj.GetValue() )
      #--- 
        elif obj.GetLabel().startswith("Start Code"):
             self.EventCode.startcode = int( obj.GetValue() )
        elif obj.GetLabel().startswith("Duration"):
             self.EventCode.duration_ms = int( obj.GetValue() )
        else:
             evt.Skip()       
             
    def OnCkBox(self,evt):
        obj = evt.GetEventObject()
        if   obj.GetLabel().startswith("Verbose") :
             self.EventCode.verbose = obj.GetValue()
        elif obj.GetLabel().startswith("Byte Code") :
             self.EventCode.send_byte_code = obj.GetValue()
        elif obj.GetLabel().startswith("Find Port") :
             self.EventCode.find_port = obj.GetValue()
        else:
             evt.Skip()        
        
    def __ApplyLayout(self):
        ds =5
      #--- com port buttons
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.BtComPortOpenClose,1, wx.ALIGN_LEFT|wx.ALL, ds)
        hbox1.Add((0,0),1,wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        hbox1.Add(self.BtComPortUpdate,1,wx.ALIGN_LEFT|wx.ALL,ds)
     
        self.pnl_bt_comport.SetSizer(hbox1)
        self.COM.vbox.Add(self.pnl_bt_comport,0, wx.EXPAND|wx.ALL,ds)
        self.COM.vbox.Layout()
      #---  send panel
        vboxSend = wx.BoxSizer(wx.VERTICAL)
        vboxSend.Add(wx.StaticText(self.pnl_bt_send,0,label='SEND'),0,wx.LEFT,ds)
        vboxSend.Add(wx.StaticLine(self.pnl_bt_send),0, wx.LEFT|wx.EXPAND|wx.ALL,ds ) 
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)  
        hbox2.Add(self.BtSendStartCode,0, wx.LEFT|wx.ALL,ds ) 
        hbox2.Add(self.BtSendStopCode,0, wx.LEFT|wx.ALL,ds ) 
        hbox2.Add(self.BtSendTestCode,0, wx.LEFT|wx.ALL,ds ) 
        vboxSend.Add(hbox2,1,wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds ) 
        vboxSend.Add(wx.StaticLine(self.pnl_bt_send),0, wx.LEFT|wx.EXPAND|wx.ALL,ds ) 
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.TxtSendCMD,1,wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, ds)
        hbox3.Add((0,0),0, wx.ALIGN_RIGHT|wx.ALL)
      
        hbox3.Add(self.BtSendCMD,0, wx.ALIGN_RIGHT|wx.ALL, ds)
      
        vboxSend.Add(hbox3,1,wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,1 ) 
        self.pnl_bt_send.SetSizer(vboxSend)
        
       #--- panels 
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.COM,0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        vbox1.Add(self.CMD,0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.VED,0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        vbox2.Add(self.OPT,0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        vbox2.Add(self.CKB,0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        
        vbox2.Add(wx.StaticText(self.pnl_rgb_eventcode,0,label='Event Code Bits'),0,wx.LEFT,ds)
        vbox2.Add(self.pnl_rgb_eventcode,0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        vbox2.Add(wx.StaticText(self.pnl_rgb_trigger,0,label='Trigger Code Bits'),0,wx.LEFT,ds)
        vbox2.Add(self.pnl_rgb_trigger,0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
                
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(vbox1,1, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        hbox.Add(vbox2,1, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(hbox,1,wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        vbox3.Add(self.pnl_bt_send,0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,ds)
        
        self.SetSizer(vbox3)      
   
   
           
class JuMEG_wxPsychoEventCodeFrame(wx.Frame):
  
    def __init__(self,*kargs, **kwargs):
        wx.Frame.__init__(self, *kargs, **kwargs)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(JuMEG_wxPsychoEventCode(self),1, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        #self.SetAutoLayout(True)
        #self.SetSizer(vbox) 
        self.InitUI()
        self.SetSizerAndFit(vbox)

        self.Show(True)  
      
        
    def InitUI(self):    
        menubar = wx.MenuBar()
        MyMenuIO  = wx.Menu()
        Mexit   = MyMenuIO.Append(wx.ID_EXIT, 'Close', 'Close application')
        
        MyMenuInfo = wx.Menu()
        Mabout  = MyMenuInfo.Append(wx.ID_ABOUT, 'About', 'About application')
        self.Bind(wx.EVT_MENU, self.ClickOnClose, Mexit)
        self.Bind(wx.EVT_MENU, self.ShowAbout, Mabout)
        
        menubar.Append(MyMenuIO,  '&Close')
        menubar.Append(MyMenuInfo,'&Info')
        
        self.SetMenuBar(menubar)
        self.Show(True)
        
    def ShowAbout(self,evt):
        """
        modified from : http://http://zetc ode.com/wxpython/dialogs/
        :return:
        """

        description="Event Code Generator for Arduino MEGA"
        
        info = wx.AboutDialogInfo()

        info.SetName('JuMEG EventCode Generator INM4-MEG-FZJ')
        info.SetVersion( __version__ )
        info.SetDescription(description)
        info.SetCopyright('(C) 2017 - 2018 Frank Boers')
        info.SetWebSite('https://github.com/fboers/JuMEGEventCode')
        info.AddDeveloper('Frank Boers')
        info.AddDocWriter('Frank Boers')
        info.AddArtist('JuMEG')
        wx.AboutBox(info) 
    
    def ClickOnClose(self,evt):
        dlg = wx.MessageDialog(self, 'Are you sure to quit?', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if (dlg.ShowModal() == wx.ID_YES):
            self.Close(True)
   
    
    
if __name__ == '__main__':
   
   app = wx.App()
   frame = JuMEG_wxPsychoEventCodeFrame(None,-1,style=wx.DEFAULT_FRAME_STYLE|wx.FULL_REPAINT_ON_RESIZE)
    
   frame.Show()
   app.MainLoop()


