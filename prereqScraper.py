from bs4 import BeautifulSoup
import requests
from time import sleep
from random import random

def getReqs(crn):
    baseURL = 'https://courselist.wm.edu/courselist/courseinfo/addInfo?fterm=202020&fcrn='
    URL = baseURL + str(crn)
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html5lib')
    table = soup.table
    table_rows = table.find_all('tr')
    fields = [row.text.strip() for row in table_rows]
    return((fields[3], fields[5], fields[7], int(crn)))
    
def reqStack(reqs):
    results = list()
    for req in reqs:
        print('Requesting CRN', req)
        results.append(getReqs(req))
        toSleep = 1. + random() + random()
        print('Sleeping for', toSleep)
        sleep(toSleep)
    return results

if __name__ == '__main__':
    fields = reqStack([22612, 22635])
    for c in fields:
        for i in enumerate(c):
            print(i[0], i[1])