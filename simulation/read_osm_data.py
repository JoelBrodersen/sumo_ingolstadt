import pyrosm 
from pyrosm import OSM
import pathlib
import geopandas as gpd


py_path = pathlib.Path(__file__)
osm_path = py_path.with_name("Ingolstadt_OSM-Daten.osm.pbf")
output_path =py_path.with_name("output_bus_nodes.csv")




osm = OSM(str(osm_path))


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
        indeces_pt.append(i)

filtered_nodes = nodes.loc[indeces_pt]
filtered_nodes.to_csv(output_path,index=False)
print(filtered_nodes["tags"])
print(len(filtered_nodes))

