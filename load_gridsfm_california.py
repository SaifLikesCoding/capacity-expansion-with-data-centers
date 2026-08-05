import numpy as np
import json as js

def load_gridsfm_case(json_path):
    with open (json_path , 'r') as f: #open file
        data = js.load(f) #load the open file json data to parsed in data
        print("First bus_i:", list(data["bus"].values())[0]["bus_i"])
        print("First load's load_bus:", list(data["load"].values())[0]["load_bus"])

    buses = list(data["bus"].values())
    ca_buses = [bus for bus in buses if 32.5 <= bus["lat"] <= 40.5 and -124.5 <= bus["lon"] <= -114]
    ca_buses_id = set([bus["bus_i"] for bus in ca_buses])
    bus_array = np.zeros((len(ca_buses),13))
    bus_id_to_row = {}

    for i ,bus in enumerate (ca_buses):
        bus_id_to_row[bus["bus_i"]] = i
        bus_array[i,0] = bus["bus_i"] # only columns 0 and 2 are read by our capacity code however the other columns would be usefull if we ever switch to AC flow
        bus_array[i,1] = bus["bus_type"]
        bus_array[i,2] = bus["pd"]
        bus_array[i,3] = bus["qd"]
        #bus_array[i,4] = bus["area"] #column 4 and 5 are not considered in our matpower
        #bus_array[i,5] = bus["vm"]
        bus_array[i,6] = bus["area"]
        bus_array[i,7] = bus["vm"]
        bus_array[i,8] = bus["va"]
        bus_array[i,9] = bus["base_kv"]
        bus_array[i,10] = bus["zone"]
        bus_array[i,11] = bus["vmax"]
        bus_array[i,12] = bus["vmin"]
    loads = list(data["load"].values())
    for i,load in enumerate (loads):
        if load["load_bus"] in ca_buses_id:
            row = bus_id_to_row[load["load_bus"]]
            bus_array[row,2] = load["pd"]
            bus_array[row,3] = load["qd"]
    gens = list(data["gen"].values())
    ca_gens = [gen for gen in gens if gen["gen_bus"] in ca_buses_id]
    gen_array = np.zeros((len(ca_gens),10))
    for i,gen in enumerate (ca_gens):
        gen_array[i,0] = gen["gen_bus"]
        gen_array[i,1] = gen["pg"]
        gen_array[i,2] = gen["qg"]
        gen_array[i,3] = gen["qmax"]
        gen_array[i,4] = gen["qmin"]
        gen_array[i,5] = gen["vg"]
        gen_array[i,6] = gen["mbase"]
        gen_array[i,7] = gen["gen_status"]
        gen_array[i,8] = gen["pmax"]
        gen_array[i,9] = gen["pmin"]
    branches = list(data["branch"].values())
    ca_branches = [branch for branch in branches if branch["f_bus"] in ca_buses_id and branch["t_bus"] in ca_buses_id]
    branch_array = np.zeros((len(ca_branches),13))
    for i,branch in enumerate (ca_branches):
            branch_array[i,0] = branch["f_bus"]
            branch_array[i,1] = branch["t_bus"]
            branch_array[i,2] = branch["br_r"]
            branch_array[i,3] = branch["br_x"]
            #branch_array[i,4] = branch["br_b"]  ----> not used by the code so redundant
            branch_array[i,5] = branch["rate_a"] 
            branch_array[i,6] = branch["rate_b"]  #from matpower.org/docs/ref/matpower5.0/idx_brch.html
            branch_array[i,7] = branch ["rate_c"]  #from matpower.org/docs/ref/matpower5.0/idx_brch.html
            branch_array[i,8] = branch["tap"]
            branch_array[i,9] = branch["shift"]
            branch_array[i,10] = branch["br_status"]
            branch_array[i,11] = branch["angmin"]
            branch_array[i,12] = branch["angmax"]
    gencost = list(data["gen"].values())
    ca_gencost = [gen for gen in gencost if gen["gen_bus"] in ca_buses_id]
    gencost_array = np.zeros((len(ca_gencost),7))
    for i,gen in enumerate (ca_gencost):
        gencost_array[i,0] = gen["model"]
        gencost_array[i,1] = gen["startup"]
        gencost_array[i,2] = gen["shutdown"]
        gencost_array[i,3] = gen["ncost"]
        if len(gen["cost"]) == 3:
            gencost_array[i,4] = gen["cost"][0]
            gencost_array[i,5] = gen["cost"][1]
            gencost_array[i,6] = gen["cost"][2]
     
    dclines = list(data["dcline"].values())
    ca_dclines = [dcline for dcline in dclines if dcline["f_bus"] in ca_buses_id and dcline["t_bus"] in ca_buses_id]
    dcline_array = np.zeros((len(ca_dclines),17))
    for i, dcline in enumerate (ca_dclines):
        dcline_array[i,0] = dcline["f_bus"]
        dcline_array[i,1] = dcline["t_bus"]
        dcline_array[i,2] = dcline["br_status"]
        dcline_array[i,3] = dcline["pf"]
        dcline_array[i,4] = dcline["pt"]
        dcline_array[i,5] = dcline["qf"]
        dcline_array[i,6] = dcline["qt"]
        dcline_array[i,7] = dcline["vf"]
        dcline_array[i,8] = dcline["vt"]
        dcline_array[i,9] = dcline["pminf"] #reasoning at https://matpower.org/docs/ref/matpower5.0/idx_dcline.html
        dcline_array[i,10] = dcline["pmaxf"] #reasoning at https://matpower.org/docs/ref/matpower5.0/idx_dcline.html
        dcline_array[i,11] = dcline["qminf"]
        dcline_array[i,12] = dcline["qmaxf"]
        dcline_array[i,13] = dcline["qmint"]
        dcline_array[i,14] = dcline["qmaxt"]
        dcline_array[i,15] = dcline["loss0"]
        dcline_array[i,16] = dcline["loss1"]
    baseMVA = data["baseMVA"]

    return{
        "baseMVA":baseMVA,
        "bus":bus_array,
        "branch":branch_array,
        "gen":gen_array,
        "gencost":gencost_array,
        "dcline":dcline_array}

if __name__ == "__main__":
    case = load_gridsfm_case("c:/Users/spoonawa/Desktop/New folder/gridsfm_western.json")
    print("baseMVA:", case["baseMVA"])
    print("bus shape:", case["bus"].shape)
    print("gen shape:", case["gen"].shape)
    print("branch shape:", case["branch"].shape)
    print("gencost shape:", case["gencost"].shape)
    print("dcline shape:", case["dcline"].shape)
    print("pd values:", case["bus"][:,2].sum())
    print("gen cost values:", case["gencost"][:,5].sum())

    