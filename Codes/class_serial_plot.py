
#import matplotlib.pyplot as plt
'''
import matplotlib
matplotlib.use("Qt5Agg")
plt = matplotlib.pyplot
'''
'''
 supported values are ['GTK3Agg', 'GTK3Cairo', 'GTK4Agg', 'GTK4Cairo', 'MacOSX', 'nbAgg', 'QtAgg', 'QtCairo', 'Qt5Agg', 'Qt5Cairo', 'TkAgg', 'TkCairo', 'WebAgg', 'WX', 'WXAgg', 'WXCairo', 'agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg', 'template']

''' 

class Sensor_B_Hole():
 """ 
 classe définissant un capteur caractérisé par:
 - son nom
 - son type (Pressure,  flow, current,voltage)
 """
 def __init__(self, name_sensor = "sensor00", id_sensor="A00", type_sensor="unknow", value_sensor= 255, Xcoordinate=0):
   # super(Sensor_eexplore, self).__init__()
    self.nom          = name_sensor
    self.idsensor     = id_sensor
    self.kindsensor   = type_sensor
    self.array_conv_v = [value_sensor]
    self.abscisses    = [Xcoordinate]
  
 def changeNom(self, nouveau_nom):
    self.nom = nouveau_nom

 def changeid(self, nouveau_id):
    self.idsensor = nouveau_id

 def changekind(self, nouveau_type):
    self.kindsensor = nouveau_type
    
 def set_arrayconv(self, value_sensor):
    self.array_conv_v.append(value_sensor)
    
 def clean_arrayconv(self):
    self.array_conv_v.pop(0)
    
 def setV_X(self,Xcoordinate):     
    self.abscisses.append(Xcoordinate)
    # self.abscisses= range(len(self.array_conv_v))
 
 def cleanV_X(self):
    self.abscisses.pop(0)

 def read_name(self):
    return (self.nom)

 def read_id(self):
    return (self.idsensor)

 def read_kind(self):
    return (self.kindsensor)
   
 def read_arrayconv(self):
    return (self.array_conv_v)
   
 def read_abscisses(self):
    return (self.abscisses)
  
 
 def plot_signal(self):
    plt.close()
    #print("x={} |||| y={}".format(self.abscisses,self.array_conv_v))
    plt.title('sensor: ' + self.nom) 
    plt.ylabel('Amplitud: ' + self.kindsensor)
    plt.xlabel('Points')
    plt.grid()
    plt.plot(self.abscisses,self.array_conv_v,"-*b",markersize=3, label=self.nom)
    plt.show()
'''
'''
def Nsensor(self,id_sensor):
   if	id_sensor== 0:return	'Sensor1'
   elif id_sensor== 1:return	'Sensor2'
   elif id_sensor== 2:return	'Sensor3'
   elif id_sensor== 3:return	'Sensor4'
   elif id_sensor== 4:return	'Sensor5'
   elif id_sensor== 5:return	'Sensor6'
   elif id_sensor== 6:return	'Sensor7'
   elif id_sensor== 7:return	'Sensor8'
   else   :return 'Unknow Sensor'

   
