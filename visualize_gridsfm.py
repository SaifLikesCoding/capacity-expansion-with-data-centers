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

    buses[row]["pd"] = load["pd"]

ca_buses = [bus for bus in buses if 32.5 <= bus["lat"] <= 40.5 and -124.5 <= bus["lon"] <= -114] 
lats = [bus["lat"] for bus in ca_buses]
lons = [bus["lon"] for bus in ca_buses]
print(len(ca_buses))
pd_values = [bus["pd"] for bus in ca_buses]
bus_type = bus_array [:,1]

plt.scatter(lons,lats,c=pd_values)
plt.xlabel("longtitude")
plt.ylabel("latitude")
plt.colorbar(label='Load Demand (MW)')
plt.title("Bus Locations by Demand")
plt.show()

