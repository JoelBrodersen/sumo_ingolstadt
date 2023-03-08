import sumolib
import pathlib
import math
import numpy
import xml.etree.ElementTree as ET
import pandas as pd

#this script converts the gtfs_pt_stops_edit_10_24.add.xml into a csv file with the columns id, lat, lon, x, y (gtfs_stations.csv)




def get_stops_data(): #Converts the XML-Data in the additional file into a Pandas DataFrame, checks for faulty Stops
    path_py = pathlib.Path(__file__)
    path_stops = path_py.parents[2].joinpath("simulation\gtfs_pt_stops_edit_10_24.add.xml") 
    tree_busstops = ET.parse(path_stops)
    additional = tree_busstops.getroot()
    id_list = []
    name_list = []
    lane_list =[]
    start_pos_list =[]
    end_pos_list =[]
    faulty_stops_list =[]
    for busStop  in additional.findall("busStop"):
        id_list.append(busStop.attrib["id"])
        if "name" in busStop.attrib:
            name_list.append(busStop.attrib["name"])
        else: 
            faulty_stops_list.append((busStop.attrib["id"],"name missing"))
            name_list.append("name missing")
        lane_list.append(busStop.attrib["lane"])
        if "startPos" in busStop.attrib:
            start_pos_list.append(busStop.attrib["startPos"])
        else: 
            faulty_stops_list.append((busStop.attrib["id"],"startPos missing"))
            start_pos_list.append("0")
        end_pos_list.append(busStop.attrib["endPos"])
    


    df_busStops = pd.DataFrame({"id":id_list,"name":name_list,"lane":lane_list,"startPos":start_pos_list,"endPos":end_pos_list})
    return df_busStops,faulty_stops_list



path_py = pathlib.Path(__file__)
path_net = path_py.parents[2].joinpath('simulation\ingolstadt_24h-edit.net.xml')

net = sumolib.net.readNet(path_net,**{"withInternal":True})
print(net)

df_busStops,flist = get_stops_data()
print(df_busStops)
x_list = []
y_list = []
lat_list = []
lon_list = []
id_list = []

for index in range(0, len(df_busStops)):
    shape = net.getLane(df_busStops._get_value(index, 'lane')).getShape()
    print(df_busStops._get_value(index, 'startPos'))
    print(df_busStops._get_value(index, 'endPos'))
    offset = (float(df_busStops._get_value(index, 'startPos')) + float(df_busStops._get_value(index, 'endPos')))/2 # mid value startPos and endPos
    x,y = sumolib.geomhelper.positionAtShapeOffset(net.getLane(df_busStops._get_value(index, 'lane')).getShape(), offset)
    lon,lat = net.convertXY2LonLat(x, y)
    x_list.append(x)
    y_list.append(y)
    lon_list.append(lon)
    lat_list.append(lat)
    id_list.append(df_busStops._get_value(index,'id'))

#export collected data to csv file
df_csv = pd.DataFrame({"id":id_list,"lat":lat_list,"lon":lon_list,"x":x_list,"y":y_list})
df_csv.to_csv('gtfs_stations_small.csv', index=False)
    
