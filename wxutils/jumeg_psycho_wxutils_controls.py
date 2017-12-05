#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 22:35:34 2017

@author: fboers
"""

import numpy as np
import wx
try:
    from agw import floatspin as FS
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.floatspin as FS

__version__='2017.11.30.001'

class JuMEG_wxControlButtons(wx.Panel):
    def __init__(self, parent,boxsizer=wx.HORIZONTAL):
        """"""
 
        super(JuMEG_wxControlButtons,self).__init__(parent=parent, id=wx.ID_ANY,style=wx.SUNKEN_BORDER)
        
        self.label    = 'Buttons'
        self.boxsizer = boxsizer       
        self.SetBackgroundColour('white')
        
        self.BtApply= wx.Button(self,id=wx.ID_APPLY,label='Apply')
        self.BtApply.Bind(wx.EVT_BUTTON, self.ClickOnBtApply)
        
        self.BtExit         = wx.Button(self,id=wx.ID_EXIT)
        self.BtCloseDisplay = wx.Button(self,id=wx.ID_ANY,label='CloseDisplay')
        self.BtInitDisplay  = wx.Button(self,id=wx.ID_ANY,label='InitDisplay')
        
        self.__btlist2disable=[self.BtExit,self.BtCloseDisplay,self.BtInitDisplay]
    
        self.__ApplyLayout()
        
    def ClickOnBtApply(self,evt):
        if evt:
           #self.BtApply.GetId() == wx.ID_APPLY
           self.BtApply.SetId(wx.ID_STOP)
           self.BtApply.SetLabel('Stop')
           evt.Skip()
        else:
           self.BtApply.SetId(wx.ID_APPLY)
           self.BtApply.SetLabel('Apply')
          
    
    def SetButtonState(self,state):
        for bt in self.__btlist2disable:
           if state:
              bt.Enable()
           else:
              bt.Disable()
    
    def __ApplyLayout(self):
        box = wx.BoxSizer(self.boxsizer)
        box.Add(self.BtApply,1, wx.ALIGN_LEFT|wx.ALL, 5)
        box.Add(self.BtInitDisplay,1,wx.ALIGN_LEFT|wx.ALL, 5)
        box.Add(self.BtCloseDisplay,1,wx.ALIGN_LEFT|wx.ALL, 5)
        box.Add((0,0),1,wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        box.Add(self.BtExit,1,wx.ALIGN_RIGHT|wx.ALL, 5)
          
        self.SetSizer(box)
  
class JuMEG_wxControls(wx.Panel):
    """
     generate spin/floatspin combobx controls
     input:
        title: text
        bg   : background colo
        control_list: array of( ( type,label,min,max,value,callback fct) )
        control_list = ( ("SP","Xpos",-500,500,0,self.OnSpinXYpos),
                         ("SP","Ypos",-500,500,0,self.OnSpinXYpos),
                         ("SP","Width",1,5000,640,self.OnSpinSize),
                         ("SP","Height",1,5000,480,self.OnSpinSize)
                        )   
    """
    def __init__(self, parent,control_list=None,label='TEST',bg="grey90",boxsizer=wx.VERTICAL):
        wx.Panel.__init__(self,parent,-1,style=wx.SUNKEN_BORDER)
        self.vbox = wx.BoxSizer(boxsizer)
        self.SetBackgroundColour(bg)

        self.__obj     = []   
       
       #--- Label + line 
        self.vbox.Add( wx.StaticText(self,0,label=label),0,wx.LEFT,5)
        self.vbox.Add( wx.StaticLine(self),0, wx.EXPAND|wx.ALL,5 ) 
       
       #--- add controls 
        self.vbox.Add( self.initControl(control_list), 0, wx.EXPAND|wx.ALL,15)
       
        self.SetAutoLayout(True)
        self.SetSizer(self.vbox)         
    
    def initControl(self,splist):
        if np.ndim(splist) > 1:
           row  = len( splist   )
        else:
           row = 1
           
        col  = 4
        ds   = 5
        fgs1 = wx.FlexGridSizer(row,col,ds,ds)
        empty_cell=(0,0)
        
        for d in splist:
          
            fgs1.Add( wx.StaticText(self,-1,label=d[1]),0,wx.LEFT,ds)
           #---Button      
            if d[0] == "BT":
               self.__obj.append(wx.Button(self,wx.NewId(),label=d[2],style=wx.BU_EXACTFIT))
               self.__obj[-1].SetName(d[3])
               self.__obj[-1].Bind(wx.EVT_BUTTON,d[-1])
               fgs1.Add(empty_cell,0,wx.LEFT|wx.EXPAND,ds) # skip min bt
               fgs1.Add(self.__obj[-1],0,wx.LEFT|wx.EXPAND,ds)
               fgs1.Add(empty_cell,0,wx.LEFT|wx.EXPAND,ds) # skip max bt
            elif d[0] == 'CK':   
               self.__obj.append( wx.CheckBox(self,wx.NewId(),label=d[2] ) )  
               self.__obj[-1].SetValue(d[3])
               self.__obj[-1].Bind(wx.EVT_CHECKBOX, d[-1])  
               fgs1.Add(empty_cell,0,wx.LEFT|wx.EXPAND,ds) # skip min bt
               fgs1.Add(self.__obj[-1],0,wx.EXPAND,ds)
               fgs1.Add(empty_cell,0,wx.LEFT|wx.EXPAND,ds) # skip max bt
               
            #---ComboBox      
            elif d[0] == "COMBO":
               self.__obj.append(wx.ComboBox(self,wx.NewId(),choices=d[3],style=wx.CB_READONLY))
               self.__obj[-1].SetName(d[1])           
               self.__obj[-1].SetValue(d[2])
               self.__obj[-1].Bind(wx.EVT_COMBOBOX,d[-1])
               fgs1.Add(empty_cell,0,wx.LEFT|wx.EXPAND,ds) # skip min bt
               fgs1.Add(self.__obj[-1],0,wx.LEFT|wx.EXPAND,ds)
               fgs1.Add(empty_cell,0,wx.LEFT|wx.EXPAND,ds) # skip max bt
          #---wx.TextCtrl     
            elif d[0] == 'TXT':
                 self.__obj.append( wx.TextCtrl(self,wx.NewId() ))   
                 self.__obj[-1].SetName(d[1])
                 self.__obj[-1].SetValue(d[2])
                  #if d[3]:
                  #   self.__obj[-1].Bind(wx.EVT_TXTCTRL, d[3])  #6 
                 fgs1.Add(empty_cell,0,wx.LEFT|wx.EXPAND,ds) # skip min bt
                 fgs1.Add(self.__obj[-1],0,wx.LEFT|wx.EXPAND,ds)
                 fgs1.Add(empty_cell,0,wx.LEFT|wx.EXPAND,ds) # skip max bt
        
         #---  MIN/MAXSpin Buttons
            else: 
           #--- min button 
               self.__obj.append( wx.Button(self,wx.NewId(),label="|<",style=wx.BU_EXACTFIT,name="MIN") ) 
               self.__obj[-1].Bind(wx.EVT_BUTTON,self.OnClickMinMax)  
               fgs1.Add(self.__obj[-1],0,wx.LEFT,ds)
           #---SpinCrtl     
               if d[0] == 'SP':   
                  self.__obj.append( wx.SpinCtrl(self,wx.NewId(),style=wx.SP_ARROW_KEYS|wx.SP_WRAP|wx.TE_PROCESS_ENTER|wx.ALIGN_RIGHT)) 
                  self.__obj[-1].SetLabel(d[1])
                  self.__obj[-1].SetToolTipString("Min: " + str(d[2][0]) +"  Max: " + str(d[2][1]) )
                  self.__obj[-1].SetRange(d[2][0],d[2][1])
                  self.__obj[-1].SetValue(d[3])
                  self.__obj[-1].Bind(wx.EVT_SPINCTRL, d[-1])  #5
                  fgs1.Add(self.__obj[-1],1,wx.EXPAND,ds)
           #---FloatSpinCrtl      
               elif d[0] == "SPF":
                  self.__obj.append( FS.FloatSpin(self,wx.NewId(),min_val=d[2][0],max_val=d[2][1],increment=d[2][2],value=1.0,agwStyle=FS.FS_RIGHT) )   
                  self.__obj[-1].SetLabel(d[1])
                  self.__obj[-1].SetFormat("%f")
                  self.__obj[-1].SetDigits(3)
                  self.__obj[-1].SetValue(d[3])
                 # self.__obj[-1].Bind(FS.EVT_FLOATSPIN, d[-1])  #6 
                  self.__obj[-1].Bind(wx.EVT_SPINCTRL, d[-1])  #6 
                  #self.__obj_spf.append( self.__obj[-1] )
                  fgs1.Add(self.__obj[-1],1,wx.EXPAND,ds) 
               else:
                  fgs1.Add(wx.StaticText(self,-1,label="NOT A CONTROLL"),wx.EXPAND,ds)
                    
           #--- max button   
               self.__obj.append( wx.Button(self,wx.NewId(),label=">|",style=wx.BU_EXACTFIT,name="MAX") )  
               self.__obj[-1].Bind(wx.EVT_BUTTON,self.OnClickMinMax)  
               fgs1.Add(self.__obj[-1],0,wx.RIGHT,ds)
 
        return fgs1                    

    def __get_obj(self):
        return self.__obj
    
    controls=property(__get_obj)    
    objects =property(__get_obj)    
    
    def OnClickMinMax(self,evt): 
        obj = evt.GetEventObject()
          
    #--- get obj SpinCtrl   
        if   obj.GetName() == "MIN":
             obj_sp = self.FindWindowById( obj.GetId()+1)
             obj_sp.SetValue( obj_sp.GetMin() )
        elif obj.GetName() == "MAX": 
             obj_sp = self.FindWindowById( obj.GetId()-1)
             obj_sp.SetValue( obj_sp.GetMax() )
        else:
            evt.Skip()
            return    
        evtsp = wx.CommandEvent(wx.EVT_SPINCTRL.typeId, obj_sp.GetId()) 
        evtsp.SetEventObject(obj_sp)
        obj_sp.ProcessEvent(evtsp)
   
class JuMEG_wxControlCheckButtons(wx.Panel):
    """
     generate check button controls
     input:
        title: text
        bg   : background colo
        control_list: array of( ( type,label,min,max,value,callback fct) )
        control_list = ( ("CB","TEST 1",True,self.OnCB),
                         ("CB","TEST 2",True,self.OnCB)
                       )   
    """
    def __init__(self, parent,control_list=None,label='TEST',bg="grey90",boxsizer=wx.VERTICAL):
        wx.Panel.__init__(self,parent,-1,style=wx.SUNKEN_BORDER)
        self.vbox = wx.BoxSizer(boxsizer)
        self.SetBackgroundColour(bg)

        self.__obj     = []   
        self.__obj_spf = []   
      
       #--- Label + line 
        self.vbox.Add( wx.StaticText(self,0,label=label),0,wx.LEFT,5)
        self.vbox.Add( wx.StaticLine(self),0, wx.EXPAND|wx.ALL,5 ) 
       
       #--- add controls  
        self.vbox.Add( self.initControl(control_list), 0, wx.EXPAND|wx.ALL,15)
       
        self.SetAutoLayout(True)
        self.SetSizer(self.vbox)         
    
    def initControl(self,splist):
        row  = len( splist )
        col  = 1
        ds   = 5
        fgs1 = wx.FlexGridSizer(row,col,ds,ds)
        
        for d in splist:
          #---SpinCrtl     
            if d[0] == 'CK':   
               self.__obj.append( wx.CheckBox(self,wx.NewId(),label=d[1] ) )  
               self.__obj[-1].SetValue(d[2])
               self.__obj[-1].Bind(wx.EVT_CHECKBOX, d[-1])  
               fgs1.Add(self.__obj[-1],1,wx.EXPAND,ds)
            else:
               fgs1.Add(wx.StaticText(self,-1,label="NOT A CONTROLL"),wx.EXPAND,ds)
                    
        return fgs1       
             
