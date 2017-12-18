
# coding: utf-8

# In[52]:

import functions as funcs
from matplotlib import pyplot as plt
import time as timeLib

import numpy as np
np.random.seed(0)
import math
import random 
import pandas
from bokeh.io import curdoc
from bokeh.layouts import widgetbox, row, column, layout
from bokeh.models import ColumnDataSource, Select, Slider, Button, Label
from bokeh.palettes import Spectral6
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file, show
from sklearn import tree
from sklearn.cross_validation import train_test_split

from sklearn import neighbors, datasets
from sklearn.neighbors import NearestNeighbors
from sklearn import cluster, datasets
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import cross_val_score


from sklearn.cluster import KMeans
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.models import BoxZoomTool
from bokeh.models import WheelZoomTool
from bokeh.models import PanTool
from bokeh.models import Arrow, OpenHead, NormalHead, VeeHead




sensorData, sensor_file_location = funcs.openSensorFile()
meteorData = funcs.openMeteorFile()
facs = pandas.read_csv('factories.csv')




# for i in range(0, len(sensorData)):
#     print(sensorData[i])

#print("len(sensorData) = ", len(sensorData))
#print("len(meteorData) = ", len(meteorData))



#for i in range(0, len(meteorData)):
#    print(meteorData[i])




combinedData, numToDateHashMap = funcs.combineData(sensorData, meteorData, sensor_file_location)
# plt.plot([0,1,2],[0,1,2])
# plt.show()
# for keyTriple in combinedData.keys():
#     print(keyTriple, " ) ", len(combinedData[keyTriple]))
#     print()

print("len(combinedData) = ", len(combinedData))







def findRanksBasedOnChemicalMeasurement(combinedData, chemical, time):
    currentTimeData = combinedData[time]
    
    #print("currentTimeData[len(currentTimeData)-1] = ", currentTimeData[len(currentTimeData)-1])
    #print()
    sensor_measurements = []
    for i in range(0, len(currentTimeData)-2):
        if currentTimeData[i][1] == chemical:
            sensor_measurements.append((currentTimeData[i][0], currentTimeData[i][2]))
            
    #print("sensor_measurements = ", sensor_measurements)
    #print()
    sensor_measurements.sort(key=lambda tup: tup[1])
    #print("sensor_measurements = ", sensor_measurements)
    return sensor_measurements
            








def drawGasPlot(combinedData, chemical, time, numToDateHashMap):
    p = figure( title= "Gas Measure of " + chemical, x_axis_location=None, y_axis_location=None, 
     x_axis_label='Map', y_axis_label='Map',  tools="pan,wheel_zoom,reset,hover,save") 

    # p.circle(x = facs['x'], y = facs['y'], color = 'blue', size = 15)

    sensor_measurements = findRanksBasedOnChemicalMeasurement(combinedData, chemical, time)
    rankSize = 10
    print('wind direction is')
    print(combinedData[time][-1][1])
    angle = combinedData[time][-1][1]
    print('sin shift {} and cos shift {}'.format(math.sin(math.radians(angle)),math.cos(math.radians(angle))))
    print("date is ", numToDateHashMap[time])
    for pair in sensor_measurements:
        if pair[0] == 1.0:
            p.circle(61, 21, size=pair[1]*25, line_color="green", fill_color="green", fill_alpha=0.5)
        elif pair[0] == 2.0:
            p.circle(66, 35, size=pair[1]*25, line_color="green", fill_color="green", fill_alpha=0.5)
        elif pair[0] == 3.0:
            p.circle(76, 41, size=pair[1]*25, line_color="green", fill_color="green", fill_alpha=0.5)
        elif pair[0] == 4.0:
            p.circle(88, 45, size=pair[1]*25, line_color="green", fill_color="green", fill_alpha=0.5)
        elif pair[0] == 5.0:
            p.circle(103, 43, size=pair[1]*25, line_color="green", fill_color="green", fill_alpha=0.5)
        elif pair[0] == 6.0:
            p.circle(102, 22, size=pair[1]*25, line_color="green", fill_color="green", fill_alpha=0.5)
        elif pair[0] == 7.0:
            p.circle(89, 3, size=pair[1]*25, line_color="green", fill_color="green", fill_alpha=0.5)
        elif pair[0] == 8.0:
            p.circle(74, 7, size=pair[1]*25, line_color="green", fill_color="green", fill_alpha=0.5)
        elif pair[0] == 9.0:
            p.circle(119, 42, size=pair[1]*25, line_color="green", fill_color="green", fill_alpha=0.5)
            
        rankSize += 10
            
    #show(p)
    p.circle(x=50, y=0, fill_alpha = 0, size = 1)
    p.circle(x=110, y=60, fill_alpha = 0, size = 1)
    p.add_layout(Arrow(end=VeeHead(size=35, fill_color = 'red'), line_color="red",
                   x_start=65, y_start=53, x_end=65-math.sin(math.radians(angle)), y_end=53-math.cos(math.radians(angle))))
    speed = Label(x=65, y=56, background_fill_color='white', text='wind speed: ' +str(combinedData[time][-1][3]))
    p.add_layout(speed)
    p.image_url(url=['https://i.imgur.com/Lz7D8KN.jpg'], x=46, y=65, w = 82, h= 70, global_alpha = .5)

    return p
    
# print('yay!!!')
# plt.plot([0,1,2],[0,1,2])
# plt.show()




#first time = 42461.0
currGasPlot = drawGasPlot(combinedData, "Methylosmolene", 42461.0, numToDateHashMap)

timePeriods = []
for time in combinedData.keys():
    timePeriods.append(str(time))
    
sensors = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
chemicals = ["Methylosmolene", "Chlorodinine", "AGOC-3A", "Appluimonia"]







#Selections and Sliders
time_select = Select(title = "Time",
                     value = str(42461.0),
                     width=200,
                     options = timePeriods)

chemical_select = Select(title = "Chemical",
                     value = "Methylosmolene",
                     width=200,
                     options = chemicals)
scan_button = Button(label="Scan", button_type="success")
scan_30_button = Button(label="Scan Next 30", button_type="success")







#functions when selectors and sliders are used
def update(attrname, old, new):
    currTime = time_select.value
    currChemical = chemical_select.value
    newGasPlot = drawGasPlot(combinedData, currChemical, float(currTime), numToDateHashMap)
    layout.children[1] = newGasPlot
    
    
    
    
def scanAllTime():
    print("Went into scanAllTime method")
    for timeFrame in timePeriods:
        time_select.value = timeFrame
        timeLib.sleep(3.0)

    
def scanNext30():
    print("Went into scanNext30 method")
    timeIndex = timePeriods.index(time_select.value)
    for i in range(timeIndex, timeIndex+30):
        time_select.value = timePeriods[i]
        timeLib.sleep(3.0)
    print("Done with scanNext30")
    
    
    
print('working')

#execute these functions when any inputs are changed
time_select.on_change('value', update)
chemical_select.on_change('value', update)
scan_button.on_click(scanAllTime)
scan_30_button.on_click(scanNext30)

inputs = column(widgetbox(time_select, chemical_select, scan_button, scan_30_button, sizing_mode="scale_both"))
layout = row(inputs, currGasPlot)
curdoc().add_root(layout)
curdoc().title = "Gas Plot"
print('working')





