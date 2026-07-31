import json as js
import numpy as np
import matplotlib.pyplot as plt

with open ("c:/Users/spoonawa/Desktop/New folder/gridsfm_western.json" , "r") as f :
    data = js.load(f)

bus_id_to_row = {}
buses = list(data["bus"].values())
bus_array = np.zeros((len(buses),13))

for i, bus in enumerate(buses):
    bus_id_to_row[bus["bus_i"]] = i
    bus_array[i,0] = bus["bus_i"] # only columns 0 and 2 are read by our capacity code however the other columns would be usefull if we ever switch to AC flow

loads = list(data["load"].values())
for i, load in enumerate(loads):
    row = bus_id_to_row[load["load_bus"]]

    bus_array[row,2] = load["pd"]

lats = [bus["lat"] for bus in buses]
lons = [bus["lon"] for bus in buses]
pd_values = bus_array[:,2]
bus_type = bus_array [:,1]

plt.scatter(lons,lats,c=pd_values)
plt.xlabel("longtitude")
plt.ylabel("latitude")
plt.colorbar(label='Load Demand (MW)')
plt.title("Bus Locations by Demand")
plt.show()

