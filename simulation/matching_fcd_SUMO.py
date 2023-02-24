import sumolib
import pathlib
import xml.etree.ElementTree as ET
import pandas as pd

def get_paths(path_type):
    py_path = pathlib.Path(__file__)
    net_path = py_path.with_name("ingolstadt_24h.net.xml")
    fcd_path = py_path.with_name("output.csv")
    if path_type == "py":
        return py_path
    elif path_type =="net":
        return net_path
    elif path_type == "fcd":
        return fcd_path
    else:
        print("invalid path type")


def create_additional():
    additional = ET.Element("additional")
    return additional

def append_PoI_XML(add_element,x_PoI,y_PoI,id_PoI="0", color_PoI="153,50,204",type_PoI="Edge_Match",param_key=None,param_value=None):
    poi = ET.Element("poi")
    poi.set("x",str(x_PoI))
    poi.set("y",str(y_PoI))
    poi.set("id",id_PoI)
    poi.set("color",color_PoI)
    poi.set("type",type_PoI)
    if param_key != None
        param_element = ET.Element("param")
        param_element.set("key",param_key)
        param_element.set("value",param_value)
    add_element.append(poi)
    return add_element


def write_xml(additional):
    py_path = get_paths("py")
    path_output = py_path.with_name("PoI_sumo_edges.add.xml")
    add_tree = ET.ElementTree(additional)
    ET.indent(add_tree)
    add_tree.write(path_output)

additional = create_additional()
net = sumolib.net.readNet(get_paths("net"))
fcd_df = pd.read_csv(get_paths("fcd"))
print(fcd_df.loc[0,"FR1A__PSD_06_location_last.lon"])
prior_lon = 0
prior_lat = 0
for index, row in fcd_df.iterrows():
    lon = row["FR1A__PSD_06_location_last.lon"]
    lat = row["FR1A__PSD_06_location_last.lat"]
    if (lon,lat) == (prior_lon,prior_lat):
        pass
    else:
        x, y = net.convertLonLat2XY(lon, lat)
        id = "fcd_data" + str(index) 
        append_PoI_XML(additional,x,y,id)
    prior_lon = lon
    prior_lat = lat
write_xml(additional)

breakpoint()

radius = 2

#48.775422, 11.410851
#48.776164471689206, 11.408601599470137
#48.77542029862346, 11.410842077750965




print(x,y)

edges = net.getNeighboringEdges(x, y, radius)
# pick the closest edge
if len(edges) > 0:
    distancesAndEdges = sorted([(dist, edge) for edge, dist in edges])
    print(distancesAndEdges)
    dist, closestEdge = distancesAndEdges[0]


additional =create_additional()
append_PoI_XML(additional,x,y)
write_xml(additional)



### Concernate Data with sumolib.route