import sumolib
import pathlib
import math
import numpy
import xml.etree.ElementTree as ET
import pandas as pd

#this script creates a points of interest .add.xml-file from zHV_10.02.2023_16-08.csv

path_py = pathlib.Path(__file__)
path_net = path_py.with_name('ingolstadt_24h-edit.net.xml')
net = sumolib.net.readNet(path_net)

id_list = []
lat_list = []
lon_list = []
x_list = []
y_list = []

df = pd.read_csv('zHV_10.02.2023_16-08.csv', sep=';')
for i in range(0, len(df)):
    if type(df.iloc[i][4]) != type(3.14):
        if df.iloc[i][4].isnumeric():
            id_list.append(df.iloc[i][2])
            lat_list.append(df.iloc[i][5])
            lon_list.append(df.iloc[i][6])
            x, y = net.convertLonLat2XY(float(df.iloc[i][6].replace(",", ".")), float(df.iloc[i][5].replace(",", ".")))
            x_list.append(x)
            y_list.append(y)

for i in range(0, len(df)):
    if type(df.iloc[i][4]) == type(3.14):
        id_list.append(df.iloc[i][2])
        lat_list.append(df.iloc[i][5])
        lon_list.append(df.iloc[i][6])
        x, y = net.convertLonLat2XY(float(df.iloc[i][6].replace(",", ".")), float(df.iloc[i][5].replace(",", ".")))
        x_list.append(x)
        y_list.append(y)


def append_PoI_XML(add_element,x_PoI,y_PoI,id_PoI, color_PoI="255,0,0",type_PoI="BusStop"):
    poi = ET.Element("poi")
    poi.set("x",str(x_PoI))
    poi.set("y",str(y_PoI))
    poi.set("id", "zHV_" + id_PoI)
    poi.set("color",color_PoI)
    poi.set("type",type_PoI)
    add_element.append(poi)
    return add_element

def create_additional():
    additional = ET.Element("additional")
    return additional

def write_xml(additional):
    py_path = pathlib.Path(__file__)
    path_output = py_path.with_name("poi_zHV.add.xml")
    add_tree = ET.ElementTree(additional)
    add_tree.write(path_output)
 
additional = create_additional()

for i in range(0, len(id_list)):
    append_PoI_XML(additional, x_list[i], y_list[i], id_list[i])
    ET.indent(additional)
    write_xml(additional)