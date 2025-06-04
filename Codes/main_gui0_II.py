#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on wendsday june 17 14:00:00 2024

end june 17, 2024 16:22
@author: Elfrich
"""

from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from PyQt5.QtCore import QObject

import os
import class_gui0
# https://stackoverflow.com/questions/73693104/valueerror-exceeds-the-limit-4300-for-integer-string-conversion
import sys
#sys.set_int_max_str_digits(0)
sys.maxsize
import fileinput
import threading

#---------------------------------
import class_serial_plot as CSP_B_Hole # Class Serial Plot = CSP
# http://lense.institutoptique.fr/mine/python-pyserial-premier-script/
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
# https://www.programiz.com/python-programming/time
import time
from time import sleep

import numpy as np
import matplotlib
# https://pypi.org/project/bitstring/
from bitstring import Bits, BitArray, BitStream, pack

import serial.tools.list_ports
import io
#https://medium.com/@ryan_forrester_/remove-special-characters-from-strings-in-python-complete-guide-53651c8163d9
import re 

matplotlib.use("Qt5Agg")

app = QApplication(sys.argv)
mon_interface = class_gui0.MonInterface()

#https://bic-berkeley.github.io/psych-214-fall-2016/numpy_logical.html
#https://www.geeksforgeeks.org/python-boolean-list-initialization/
sensor_boolean = [False for i in range(8)]

sensor1 = CSP_B_Hole.Sensor_B_Hole("Sensor 1","","",0,0)
sensor2 = CSP_B_Hole.Sensor_B_Hole("Sensor 2","","",0,0)

serialqueue = serial.Serial.in_waiting

#==============================================

#==================  
def writelog(logfile, string):
    with open(logfile, 'a') as file:
        file.write( string + '\n')


def clean_arrays():
  #print(sensors[0].read_arrayconv())
  #print(sensor0.read_abscisses())
  
  for j in range(0,len(sensor1.read_arrayconv())):
       sensor1.clean_arrayconv()

  for j in range(0,len(sensor2.read_arrayconv())):
       sensor2.clean_arrayconv()

  for j in range(0,len(sensor1.read_abscisses())):    
     sensor1.cleanV_X()

  for j in range(0,len(sensor2.read_abscisses())):    
     sensor2.cleanV_X()   
   #print(sensors[0].read_arrayconv())
   #print(sensor0.read_abscisses())

def read_stream(ser):
 # with serial.Serial(port="/dev/ttyACM0", baudrate=115200, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS) as ser:
     str_experiment = mon_interface.lineEdit.text()
     str2=mon_interface.lineEdit_3.text()
     duration_seconds = 60
     # https://www.geeksforgeeks.org/python-check-if-given-string-is-numeric-or-not/
     if  str2.isdigit() == True:
         duration_seconds = int(mon_interface.lineEdit_3.text())
     #print(f'duration_seconds:   {duration_seconds}')
    
     aux0=0
     aux1=0
  
     logfile =  str_experiment +'.txt'
     seconds0 = 0
     #seconds00 = 0
     ADC = []
     array0 = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

     while seconds0 < duration_seconds:#64:
        if  ser.inWaiting() > 0 :
          #aux = ser.readline().decode("utf8")
          # https://www.geeksforgeeks.org/python-remove-initial-character-in-string-list/
          #aux = aux.replace('\n', '')
          #aux = aux.replace('\r', '')
          #aux = ser.read_until(expected='\r', size= 20)
          #aux = ser.read_until(expected='\n', size= 16)
          aux = ser.readline().decode("utf8")
          #print(f'aux:   {aux}')         

          for j in range(0,10):
              aux100 = ser.readline().decode("utf8")
              ADC100=aux100.split(',')
              for i in range(len(ADC100)):
                  if i == 0:
                      aux_0 = ADC100[i]
                      aux0 = re.sub(r'[^0-9\s]', '', aux_0)#int.from_bytes(aux_0, "little")
                  if i == 1:
                      aux_1 = ADC100[i]
                      aux1 = re.sub(r'[^0-9\s]', '', aux_1)
              array0[j] =  [aux0,aux1]  
              #print(f'j:   {j}')
              #print(f'toto[j]:   {toto[j]}')
          
          ADC=aux.split(',')          
          #print(f'ADC:   {ADC}')
          
          for i in range(len(ADC)):
              if i == 0:
                  aux_0 = ADC[i]
                  aux0 = re.sub(r'[^0-9\s]', '', aux_0)#int.from_bytes(aux_0, "little")
                  
              if i == 1:
                  aux_1 = ADC[i]                  
                  aux1 = re.sub(r'[^0-9\s]', '', aux_1)                
          #ADC = []
          #aux=0
          #print(f'aux0:   {aux0}')
          #print(f'aux1:   {aux1}')
          #print(type(aux0))
          #print(type(aux1))
          
        if aux0 != ""  and aux1 != "" and aux0 != 0:# and aux0 != "\r\n" and aux1 != "\r\n": #.isdigit():
                seconds0 = int(aux1)/1000 #(1/fe->fe=100Hz)
                #seconds00 = round(seconds0)
                sensor1.set_arrayconv(int(aux0)*(5/4095))# ADC 12 bits
                sensor1.setV_X(seconds0)#
                sensor2.set_arrayconv(int(aux0)*(5/4095))# 
                sensor2.setV_X(seconds0)# 
                
                #print(f'seconds0:   {seconds0}')
                #print(f'aux0:   {aux0}')
                
                #if aux0 != 0 and seconds0 != 0.0:
                str_data = 'Volts[V]: ' + str(round(int(aux0)*(5/4095),4)) +' ' + 'time: ' + str(seconds0)
                writelog(logfile, str_data)

                for j in range(0,10):
                    aux200 = array0[j]
                    str_data = 'Volts[V]: ' + str(round(int(aux200[0])*(5/4095),4)) +' ' + 'time: ' + str(int(aux200[1])/1000)
                    writelog(logfile, str_data)

                plot_signal()
                seconds1=50            
                shift_image(seconds0,seconds1)
                if mon_interface.Btn_stop_2.isDown() == True:
                  seconds0 = duration_seconds
       
     ser.close()
     clean_arrays()
     print("Close COM")
     
   
def shift_image(seconds0,seconds1): #-----------------------------------------------------
  shift_img=seconds1
  shift_img2=round(shift_img/50)
  # https://www.geeksforgeeks.org/convert-integer-to-string-in-python/
  '''
  if str_shift.isdigit() == True:
     shift_img = int(mon_interface.lineEdit_5.text())
  else:
     shift_img = 1 
  '''   
  #print(f'len(sensor0.abscisses):   {len(sensor0.abscisses)}')
  #print(f'len(sensors[0].array_conv_v:   {len(sensors[0].array_conv_v)}') 
  mon_interface.show_curves
  if (len(sensor1.abscisses) == len(sensor1.array_conv_v) ) :
      if seconds0 > shift_img:# = 1s
        if len(sensor1.abscisses) > 0:
              sensor1.cleanV_X()              
              sensor1.clean_arrayconv()
  if (len(sensor2.abscisses) == len(sensor2.array_conv_v) ) :
      if seconds0 > shift_img2:# = 1s
        if len(sensor2.abscisses) > 0:
              sensor2.cleanV_X()              
              sensor2.clean_arrayconv()
      
def plot_signal():#-----------------------------------------------------
    mon_interface.show_curves
    #if time_process.abscisses.ndim == 1:
    if len(sensor1.abscisses) == len(sensor1.array_conv_v):
        #mon_interface.plot_Channel1.setData(time_process.abscisses[1:],sensors[0].array_conv_v[1:])
        mon_interface.plot_sensor.setData(sensor1.abscisses[1:],sensor1.array_conv_v[1:])
        
    if len(sensor2.abscisses) == len(sensor2.array_conv_v):
        #mon_interface.plot_Channel1.setData(time_process.abscisses[1:],sensors[0].array_conv_v[1:])
        mon_interface.plot_sensor_2.setData(sensor2.abscisses[1:],sensor2.array_conv_v[1:])    
         
def get_comlst(self):  
        """Returns a list of available COM ports with description"""
        comports = serial.tools.list_ports.comports()
        comlst = []    
        
        for item in comports:
            name = item[0]
            
            if len(item[1]) > 50:
                description = item[1][0:44] + "..."
            else:
                description = item[1]
                
            comlst.append(str(name + " - " + description))
        
        return sorted(comlst)
        
def updateCOMbox(self):
        self.COMcombo['values'] = self.get_comlst()
#-------------------------------- main

def main_():
 global aux1,ser
 global quitter
 global flag_exe
 flag_exe = 13
 flag_r=0
 quitter=False
 
 comlist0 = 0
 comlist1 = 0
 comlistupdate0 = 0
 comlistupdate1 = 0
 connected = []

 cycle_mesure=0
 
 while(not quitter):
    
    aux1 = False#0
    # http://lense.institutoptique.fr/mine/python-pyserial-premier-script/ 
    comlist = serial.tools.list_ports.comports()
    comlist0 = len(comlist)
    if comlist0 == 0 and comlist1 > 0:
      mon_interface.comboBox_port_com.clear()#acquisition board communication port      
      for i in range(0,len(connected)):
          connected.pop(0)
      comlistupdate1 = 0
      

    if comlist0 > 0:
      if comlistupdate1 == 0:
        for element in comlist:
          connected.append(element.device)
        #print(f'len(connected):   {len(connected)}')
        comlist1 = comlist0
        comlistupdate0 = 1
        
      if comlist1 == comlist0 and comlistupdate0 == 1:
        for element in connected:
          mon_interface.comboBox_port_com.addItem(element[0:len(element)],element)#text[0:n], text)
        comlistupdate0 = 0
        comlistupdate1 = 1
        
      if comlist0 != comlist1 and comlistupdate1 == 1:
        #print(f'len(connected):   {len(connected)}')
        mon_interface.comboBox_port_com.clear()
        for i in range(0,len(connected)):
          connected.pop(0)
        comlist0 = 0
        comlist1 = 0
        connected = []
        comlistupdate1 = 0

    aux1 = mon_interface.Btn_Con.isDown()
        
    if aux1 == True:
      mon_interface.clean_g()
      cycle_mesure=0
      if mon_interface.comboBox_port_com.currentIndex() >= 0:#acquisition board communication port 
          port_carte_sensors= connected[mon_interface.comboBox_port_com.currentIndex()]
          baudr=115200#230400#115200
          timeout0=0.5#1#0,125#L/Fe#round(L/Fe)+1
          ser = serial.Serial(port=port_carte_sensors, baudrate=baudr, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=timeout0, rtscts=True, dsrdtr=True)
          io.DEFAULT_BUFFER_SIZE = 5000
          serial.Serial.reset_input_buffer(ser)
          serial.Serial.reset_output_buffer(ser)

          ser.close()
          ser.open()
          read_stream(ser)     


thread_read_stream = threading.Thread(target=read_stream, name='read stream')
thread_read_stream.start()

thread_plot_signal = threading.Thread(target=plot_signal, name='plot signal')
thread_plot_signal.start()

thread_main_GUI = threading.Thread(name='main_', target=main_,)
thread_main_GUI.start()

       
app.exec_()
quitter=True
thread_main_GUI.join()
thread_read_stream.join()
thread_plot_signal.join()

sys.stdout.flush()
del app
del thread_read_stream
del thread_plot_signal
del thread_main_GUI
