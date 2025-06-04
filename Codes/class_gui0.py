#!/usr/bin/env python3
# -*- coding: utf-8 -*-

    
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication,QGraphicsScene
from PyQt5.QtCore import *

from PyQt5.QtCore import QObject, QThread, pyqtSignal as Signal, pyqtSlot as Slot
import serial

import gui0 as ihm
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import time
import numpy as np

pg.setConfigOption('background', (200,200,200)) # couleur de fond du graphique
pg.setConfigOption('foreground', 'k')

# couleur des axes

#pg.setConfigOptions(antialias=True)


class MonInterface(QtWidgets.QMainWindow, ihm.Ui_MainWindow):
    """
    Dessine l'interface graphique
    """
    work_requested_serial = Signal(str)#(serial.serialposix.Serial )#for pyQt thread
    work_requested = Signal(serial.serialposix.Serial )#for pyQt thread


    def __init__(self):
        super(MonInterface, self).__init__()
        self.setupUi(self)
        
        self.graphicsView.addLegend()
        self.graphicsView_2.addLegend()
        
        self.graphicsView.showGrid(x=True, y=True)
        self.graphicsView_2.showGrid(x=True, y=True)
        
        self.graphicsView.setLabel('left', "Sensor", units = 'Volts' )
        self.graphicsView.setLabel('bottom', "Time", units='s')

        self.graphicsView_2.setLabel('left', "Sensor", units = 'Volts' )
        self.graphicsView_2.setLabel('bottom', "Time", units='s')

        self.plot_sensor = self.graphicsView.plot(pen='b',name='volts')
        self.plot_sensor_2      = self.graphicsView_2.plot(pen ='r',name ='volts')
        
        self.show()

        
    def hide_curves(self,i):        
        self.plot_sensor.hide()
        self.plot_sensor_2.hide()

         
    def show_curves(self,i):        
        self.plot_sensor.show()
        self.plot_sensor_2.show()

    def clean_g(self):        
        self.plot_sensor.clear()
        self.plot_sensor_2.clear()


        
      
        
    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.MouseButton.RightButton:
            self.autoRange()
    
    ## reimplement mouseDragEvent to disable continuous axis zoom
    def mouseDragEvent(self, ev, axis=None):
        if axis is not None and ev.button() == QtCore.Qt.MouseButton.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev, axis=axis)


            
    def closeEvent(self, event): # ajoute une boite de dialogue pour confirmation de fermeture
        result = QtWidgets.QMessageBox.question(self,
        "Confirm Exit...",
        "Are you sure you want to exit ?",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
           event.accept()
        else:
           event.ignore()
           
         

