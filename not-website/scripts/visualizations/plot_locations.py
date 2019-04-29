import matplotlib.pyplot as plt  
import csv 
import numpy as np
from argparse import ArgumentParser

'''
SYNOPSIS
python plot_locations.py --infile file.csv --imgfile file.jpg/png...
'''


SECONDS_PER_DAY = 86400
#ffd253
color_dict = {"Uber":"#000000","yellow_taxi":"#ffd253","citi":"#00c8fc","green_taxi":"#90EE90","Lyft":"#ff14bb"}
marker_dict = {"Uber":".","yellow_taxi":".","citi":"X","green_taxi":".","Lyft":"."}
size_dict= {"Uber":3,"yellow_taxi":10,"citi":3,"green_taxi":8,"Lyft":3}
opacity_dict= {"Uber":0.5,"yellow_taxi":1,"citi":0.5,"green_taxi":1,"Lyft":0.5}
staten_island_lat = -74.0553

def plot_dot_fixed_number(dot_count, rides_file,img_file,batch_size):
    '''
    Plot a set number of dots in random order
    '''
    rides_dict = read_rides(rides_file)
    #ext = [-74.05,-73.70,40.43,40.92]
    ext = list(find_extent(rides_dict))
    img = plt.imread(img_file)
    plt.imshow(img,extent=ext,zorder=1)
    plotted = 0
    handles = []
    cmp_batches = [0,0,0,0,0]
    cmp = ["Uber","Lyft","yellow_taxi","green_taxi","citi"]
    while plotted < dot_count:
        idx = np.random.randint(0,len(cmp))
        company = cmp[idx]
        cbatch = cmp_batches[idx]
        locs = rides_dict[company]
        lats = locs[0][cbatch:cbatch + batch_size]
        lngs = locs[1][cbatch:cbatch + batch_size]
        plt.scatter(lngs,lats,s=size_dict[company],marker=marker_dict[company],alpha=opacity_dict[company], label=company.capitalize(),color=color_dict[company],zorder=2)
        plotted += batch_size
        cmp_batches[idx] += batch_size
    aspect=img.shape[0]/float(img.shape[1])*((ext[1]-ext[0])/(ext[3]-ext[2]))
    plt.axis('off')
    #plt.legend(handles=handles,labels=["Yellow Taxi","Green Taxi","Citi","Uber","Lyft"],loc=(-73,41))
    plt.gca().set_aspect(aspect)
    plt.show()
           
def find_extent(rides_dict):
    left = 0
    right = float('-inf')
    bottom = float('inf')
    top = 0
    for locations in rides_dict.values():
        left = min(locations[1])
        right = max(locations[1])
        bottom = min(locations[0])
        top = max(locations[0])
    return left,right,bottom,top

def read_rides(filename):
    with open(filename, 'r') as infile:
        reader = csv.DictReader(infile)
        rides_dict = {"Uber":[[],[]],"yellow_taxi":[[],[]],"citi":[[],[]],"green_taxi":[[],[]],"Lyft":[[],[]]}
        for row in reader: 
            if float(row["lng"]) < staten_island_lat:
                continue
            rides_dict[row["company"]][0].append(float(row["lat"]))
            rides_dict[row["company"]][1].append(float(row["lng"]))
    return rides_dict

def plot_scatter(filename,imgfile=None):
    '''
    Plot all rides per company, plotting in descending order of largest number of rides. 
    '''
    rides_dict = read_rides(filename)
    sorted_rides = sorted(rides_dict.items(), key=lambda kv: -len(kv[1][0]))
    ext = list(find_extent(rides_dict)) #[-74.05,-73.65,40.43,40.95]
    print(ext)
    if imgfile:
        img = plt.imread(imgfile)
        plt.imshow(img,extent=ext,zorder=0,alpha=0.6)
        aspect=img.shape[0]/float(img.shape[1])*((ext[1]-ext[0])/(ext[3]-ext[2]))
        plt.gca().set_aspect(aspect)
    for company,location in sorted_rides:
        #latitudes for y-val 
        lats = location[0]

        #longitudes for x-val 
        lngs = location[1]

        #scatter
        h = plt.scatter(lngs,lats,s=size_dict[company],marker=marker_dict[company],alpha=opacity_dict[company], label=company.capitalize(),color=color_dict[company],zorder=1,linewidths=1)
    plt.axis("off")
    plt.show()

def plot_dot_coordinates(filename,imgfile=None):
    '''
    Hacky method that plots in fixed order per company like plot_scatter but alternates between plotting citi and uber 
    '''
    '''STATEN ISLAND NOT INCLUDED'''
    rides_dict = read_rides(filename)
    
    #sort based on number of rides per company, plot largest first 
    sorted_rides = sorted(rides_dict.items(), key=lambda kv: -len(kv[1][0]))

    #PLOT
    plot_size = 50
    size_scale = 2
    i = 1
    alpha_scale = 1
    ext = [-74.05,-73.70,40.43,40.92]
    if imgfile:
        img = plt.imread(imgfile)
        plt.imshow(img,extent=ext,zorder=1)
    batch_num = 0
    handles = []
    #hacky way of alternating citi and uber but maintaining order of rest 
    '''
    for i in range(len(sorted_rides)):
        company = sorted_rides[i][0]
        location = sorted_rides[i][1]
        if company == "Uber":
            continue 
        if company == "citi":
            citi_batch = 0 
            uber_batch = 0
            batch_size = 10
            uber_locs = sorted_rides[i+1][1]
            citi_locs = sorted_rides[i][1]
            while uber_batch < len(uber_locs[0]):
                if batch_num % 2 == 0:
                    
                    lats = citi_locs[0][citi_batch:citi_batch + batch_size]
                    lngs = citi_locs[1][citi_batch:citi_batch + batch_size]
                    h2=plt.scatter(lngs,lats,s=size_dict["citi"],marker=marker_dict["citi"],alpha=opacity_dict["citi"], label="Citi",color=color_dict["citi"],zorder=2)
                    
                    lats = uber_locs[0][uber_batch:uber_batch + batch_size]
                    lngs = uber_locs[1][uber_batch:uber_batch + batch_size]
                    h3=plt.scatter(lngs,lats,s=size_dict["Uber"],marker=marker_dict["Uber"],alpha=opacity_dict["Uber"], label="Uber",color=color_dict["Uber"],zorder=2)
                    uber_batch += batch_size
                    citi_batch += batch_size
                else: 
                    lats = uber_locs[0][uber_batch:uber_batch + batch_size]
                    lngs = uber_locs[1][uber_batch:uber_batch + batch_size]
                    h3=plt.scatter(lngs,lats,s=size_dict["Uber"],marker=marker_dict["Uber"],alpha=opacity_dict["Uber"], label="Uber",color=color_dict["Uber"],zorder=2)
                    
                    lats = citi_locs[0][citi_batch:citi_batch + batch_size]
                    lngs = citi_locs[1][citi_batch:citi_batch + batch_size]
                    h2=plt.scatter(lngs,lats,s=size_dict["citi"],marker=marker_dict["citi"],alpha=opacity_dict["citi"], label="Citi",color=color_dict["citi"],zorder=2)
                    
                    uber_batch += batch_size
                    citi_batch += batch_size
                batch_num += 1
                if uber_batch >= len(uber_locs[0]):
                    handles.append(h2)
                    handles.append(h3)

            
            while citi_batch < len(citi_locs[0]):
                lats = citi_locs[0][citi_batch:citi_batch + batch_size]
                lngs = citi_locs[1][citi_batch:citi_batch + batch_size]
                plt.scatter(lngs,lats,s=size_dict["citi"],marker=marker_dict["citi"],alpha=alpha_scale, label="citi",color=color_dict["citi"])
                citi_batch += batch_size
            
        else:
            #latitudes for y-val 
            lats = location[0]
        
            #longitudes for x-val 
            lngs = location[1]

            #scatter
            h = plt.scatter(lngs,lats,s=size_dict[company],marker=marker_dict[company],alpha=opacity_dict[company], label=company.capitalize(),color=color_dict[company],zorder=2,linewidths=1)
            size = int(size/size_scale)
            alpha_scale -= 0.1
            handles.append(h)
    '''
    if imgfile:
        aspect=img.shape[0]/float(img.shape[1])*((ext[1]-ext[0])/(ext[3]-ext[2]))
        plt.gca().set_aspect(aspect)
    plt.axis('off')
    plt.legend(handles=handles,labels=["Yellow Taxi","Green Taxi","Citi","Uber","Lyft"],loc=(-73,41))
    plt.show()

def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--infile", dest="infile", help="Input .csv file")
    parser.add_argument("-u","--imgfile",dest="img_file",help="Input img file",required=False)
    args = parser.parse_args()
    #plot_dot_coordinates(args.infile)
    #plot_dot_fixed_number(30000,args.infile,args.img_file,10)
    plot_scatter(args.infile,args.img_file)

if __name__ == "__main__":
    main()