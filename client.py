import requests
import random
import time

URL = "http://localhost"
MAXNODE = 3
DEFAULTNODEPORT = 14440
REQUESTVALUE = 3
MAXPRIME = 60
WAIT = 2
while True:
	rand = random.randint(0,MAXNODE-1)
	print ("Node requested to = ", str(rand))
	reqPrime = random.randint(2,MAXPRIME-1)
	print("Prime Needed = " + str(reqPrime))
	try:
		r = requests.get(URL + ":" + str(DEFAULTNODEPORT + rand) + "/" + str(REQUESTVALUE) + "/" + str(reqPrime))
		print("Return = " + str(r.text))
	except requests.exceptions.RequestException as e:
	    print ("The node is dead")

	time.sleep(WAIT)
