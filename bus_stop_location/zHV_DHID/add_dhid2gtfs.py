import sumolib
import pathlib
import math
import numpy
import xml.etree.ElementTree as ET
import pandas as pd

#import data from poi_gtfs.add.xml
path_py = pathlib.Path(__file__)
poi_gtfs = path_py.with_name("poi_gtfs.add.xml")
poi = ET.parse(poi_gtfs)
additional = poi.getroot()
gtfs_id_list = []
gtfs_x_list = []
gtfs_y_list = []
for poi in additional.findall("poi"):
    gtfs_id_list.append(poi.attrib["id"])
    gtfs_x_list.append(poi.attrib["x"])
    gtfs_y_list.append(poi.attrib["y"])


#import data from zHV.add.xml
path_py = pathlib.Path(__file__)
poi_zHV = path_py.with_name("poi_zHV.add.xml")
poi = ET.parse(poi_zHV)
additional = poi.getroot()
zHV_id_list = []
zHV_x_list = []
zHV_y_list = []
for poi in additional.findall("poi"):
    zHV_id_list.append(poi.attrib["id"])
    zHV_x_list.append(poi.attrib["x"])
    zHV_y_list.append(poi.attrib["y"])


#get nearest point to poi_gtfs.add.xml
id_list = []
dhid_list = []
#nx_list = []
#ny_list = []
distance_list = []
for gtfs_id, gtfs_x, gtfs_y in zip(gtfs_id_list, gtfs_x_list, gtfs_y_list):
    for zHV_id, zHV_x, zHV_y in zip(zHV_id_list, zHV_x_list, zHV_y_list):
        distance_list.append(sumolib.geomhelper.distance(p1 = [float(gtfs_x), float(gtfs_y)], p2 = [float(zHV_x), float(zHV_y)]))
    id_list.append(gtfs_id)
    nearest_point = distance_list.index(min(distance_list))
    dhid_list.append(zHV_id_list[nearest_point])
    #nx_list.append(zHV_x_list[nearest_point])
    #ny_list.append(zHV_y_list[nearest_point])
    distance_list.clear()

def write_xml(additional):
    py_path = pathlib.Path(__file__)
    path_output = py_path.with_name("gtfs_with_dhid.add.xml")
    add_tree = ET.ElementTree(additional)
    ET.indent(add_tree)
    add_tree.write(path_output, encoding="utf-8", xml_declaration=True)

#next step: insert additional param to gtfs_with_dhid.add.xml
#todo: for id in id_list add param with dhid
path_py = pathlib.Path(__file__)
#poi_gtfs = path_py.with_name("gtfs_with_dhid.add.xml")
poi = ET.parse(poi_gtfs)
additional = poi.getroot()
for elem in additional.findall('busStop'):
    param = ET.SubElement(elem, "param")
    param.set("key", "DHID") ### key 
    param.set("value", str(dhid_list[id_list.index(elem.attrib["id"])]))
    print("HALLO")
write_xml(additional)