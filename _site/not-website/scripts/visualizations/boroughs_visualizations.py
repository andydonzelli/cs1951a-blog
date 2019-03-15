import matplotlib.pyplot as plt
import csv
from argparse import ArgumentParser
import numpy as np
import pandas as pd


parser = ArgumentParser()
parser.add_argument('--file',nargs='+',dest="files")
args = parser.parse_args()

borough_rides_count = {"Manhattan":0,"Queens":0,"Staten Island":0,"Brooklyn":0,"Bronx":0}
borough_index = {"Manhattan":0,"Queens":1,"Staten Island":2,"Brooklyn":3,"Bronx":4}
cmp_borough_rides_count = {"Uber":[0]*5,"Lyft":[0]*5,"citi":[0]*5,"green_taxi":[0]*5,"yellow_taxi":[0]*5}
for afile in args.files:
    with open(afile,'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            borough_rides_count[row["borough"]] += 1
            cmp_borough_rides_count[row["company"]][borough_index[row["borough"]]] += 1

#print(borough_rides_count)
#print(cmp_borough_rides_count)
N= 5
ind = np.arange(N)
width = 0.4
boroughs = ["Manhattan","Queens","Staten Island","Brooklyn","Bronx"]
companies = ["Uber","Lyft","Citi","Yellow Taxi","Green Taxi"]

uber = np.array(cmp_borough_rides_count["Uber"])
lyft = np.array(cmp_borough_rides_count["Lyft"])
citi = np.array(cmp_borough_rides_count["citi"])
yellow_taxi = np.array(cmp_borough_rides_count["yellow_taxi"])
green_taxi = np.array(cmp_borough_rides_count["green_taxi"])

#fig = plt.figure(figsize=(6,4))
#sub1 = fig.add_subplot(211)

scale = 1e6
p1 = plt.bar(ind,yellow_taxi/scale,color='#FFD740')
p2 = plt.bar(ind,green_taxi/scale,bottom=(yellow_taxi)/scale,color='#5CF193')
p3 = plt.bar(ind,uber/scale,bottom=(green_taxi+yellow_taxi)/scale,color='#09091a')
p4 = plt.bar(ind,lyft/scale,bottom=(green_taxi+yellow_taxi+uber)/scale,color='#FF00bf')
p5 = plt.bar(ind,citi/scale,bottom=(lyft+green_taxi+yellow_taxi+uber)/scale,color='#40C4FF')

plt.ylim(top=25)
plt.ylabel("Number of Rides (in millions)")
plt.title("Ride Services in NYC by Borough")
plt.xticks(ind,(boroughs))
plt.legend((p1[0],p2[0],p3[0],p4[0],p5[0]),('Yellow Taxi','Green Taxi','Uber','Lyft','Citi'))
#plt.show()
plt.savefig("rideshares_by_borough_and_company")

"""
#sub2 = fig.add_subplot(223)
data = pd.DataFrame(cmp_borough_rides_count)
cmp_totals = data.sum(axis=0).values
ttotal = sum(cmp_totals)
bor_totals = data.sum(axis=1).values
cmp_totals= np.append(cmp_totals,ttotal)


celldata = np.hstack((np.transpose(data.values),bor_totals.reshape(bor_totals.shape[0],1)))
celldata = np.vstack((celldata,cmp_totals))
table= plt.table(colLabels=boroughs + ["Total"],rowLabels=companies+["Total"],
        cellText=celldata,loc='bottom')
plt.tick_params(bottom=False,labelbottom=False)
#plt.xlim(0,6)
plt.show()
"""
