import psutil
import requests
import time
import random
import sys

PORT = 12220;
DEFAULTNODEPORT = 14440;
WORKERPORT = 13330;
CPUSTATUS = 2
URL = "http://localhost";
ID = 0;
MAXNODE = 3
MAXID = 3
WAIT = 5;

def sendStatus():
    load = getCpuLoad();
    for i in range(MAXNODE):
        try:
            r = requests.get(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(CPUSTATUS)+"/"+str(ID)+"/"+str(load))
            print(str(r.text))
        except requests.exceptions.RequestException as e:
            print()

def getCpuLoad():
    return psutil.cpu_percent(interval=1)

#init
if len(sys.argv)!=2:
    sys.exit("Please put 1 argument for ID")
ID = int(sys.argv[1])
if ID > MAXID or ID < 0:
    sys.exit("Please put ID in range of 0 - MAXID")
print("You have ID:"+str(ID))

while True:
    print (ID)
    sendStatus()
    print(str(getCpuLoad()))
    time.sleep(WAIT)
