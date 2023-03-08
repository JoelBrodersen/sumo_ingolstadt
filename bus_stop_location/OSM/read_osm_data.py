import pyrosm 
from pyrosm import OSM
import pathlib
import geopandas as gpd


py_path = pathlib.Path(__file__)
osm_path = py_path.with_name("Ingolstadt_OSM-Daten.osm.pbf")
output_path_stops =py_path.with_name("output_bus_nodes_osm.csv")
output_path_platform =py_path.with_name("output_bus_platforms_osm.csv")



osm = OSM(str(osm_path))



data_platform =osm.get_data_by_custom_criteria(custom_filter ={"public_transport":["platform"]},keep_nodes=True,keep_relations=False,keep_ways=False)

print(data_platform.dtypes)
print(data_platform)

nodes,net = osm.get_network(nodes=True)
print(net.dtypes)
print(net)
print("----")
print(nodes.dtypes)
print(nodes)
indeces_pt = []

for i in range(0,len(nodes)):
   
    if nodes.iloc[i]["tags"] == None:
        pass
    elif "public_transport" in nodes.iloc[i]["tags"]:
       print(nodes.iloc[i]["tags"]["public_transport"]) 
       indeces_pt.append(i)



filtered_nodes = nodes.loc[indeces_pt]

## Add Name of Bussstops
names_list =[]
for i in range(len(filtered_nodes)):
    value =filtered_nodes.iloc[i]["tags"]["name"]
    names_list.append(value)

filtered_nodes["name_stop"] = names_list

filtered_nodes.to_csv(output_path_stops, index=False)
data_platform.to_csv(output_path_platform, index=False)