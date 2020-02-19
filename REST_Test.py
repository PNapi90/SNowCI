#Need to install requests package for python
 #sudo easy_install requests
import requests

import numpy as np
from numpy import random
import json


def PutIt(sys_id) -> dict:
    rVAl = random.randint(0,10000) % 2
    randVal = 'true' if rVAl == 1 else 'false'
    x = np.abs(random.normal(0,3) + 5)
    xInt = int(x) if rVAl == 1 else 0
    D = {
        'doer': sys_id,
        'did_it': randVal,
        'doit_score': str(xInt)
    }
    return D


def getResponse(url,user="admin",pwd="admin",printIt = False):
     # Set proper headers
    headers = {"Accept":"application/json"}
    
    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    if printIt:
        print(response.json())
    return response.json()


def POST(url,D,user='admin',pwd='admin'):
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    
    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers ,data=D)
    
    # Check for HTTP codes other than 200
    if response.status_code != 201: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    #print(response.json())


def deleteIt(url,user="admin",pwd="admin"):    
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    
    # Do the HTTP request
    response = requests.delete(url, auth=(user, pwd), headers=headers)
    
    # Check for HTTP codes other than 204
    if response.status_code != 204: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()


def updateIt(url,D,user="admin",pwd="admin"):
    tmpDic = {
        'did_it': D['did_it'],
        'doit_score': D['doit_score']
    }
    sendStr = str(tmpDic)
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    
    # Do the HTTP request
    response = requests.put(url, auth=(user, pwd), headers=headers ,data=sendStr)
    
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()




def main():

    nmax = 10


    SNowInstance = 'https://dev61319.service-now.com/api/now/table/'
    urlPut = SNowInstance + 'x_444043_doit_doit'


    url = 'https://dev61319.service-now.com/api/now/table/sys_user'
    jsonResponseDoIt = getResponse(url,printIt=False)

    n = len(jsonResponseDoIt['result'])
    print("")
    print(n,"records found\n")

    names = [[record['name'],record['sys_id']] for record in jsonResponseDoIt['result']]


    UPDATE = False
    
    if UPDATE:
        DoItRecords = getResponse(urlPut,printIt=False)
        sys_ids = [[record['sys_id'],record['number']] for record in DoItRecords['result']]
        n = len(sys_ids)
        for i,s in enumerate(sys_ids):
            sys_id = s[0]
            #print(DoItRecords['result'][i])
            D = PutIt(sys_id)
            urlTmp = urlPut + "/" + sys_id
            #print("Put url ->",urlTmp)
            rel = round((i+1)/n*100,2)
            progressStr = str(i+1) + "/" + str(n)
            print(s[1],"updated ->",D['did_it'],D['doit_score'],"\t->",progressStr,"->",rel,"%")
            updateIt(urlTmp,D)





    else:
        DELETE = False

        if not(DELETE):
            for i,n in enumerate(names):
                print(i,"->",n[0],n[1])
                if i < nmax:
                    D = PutIt(n[1])
                    tmpString = str(D)
                    #print(D)
                    POST(urlPut,tmpString)
                else:
                    break

        else:
            DoIts = getResponse(urlPut,printIt=True)
            sysIDSTuple = [[d['number'],d['sys_id']] for d in DoIts['result']]

            for s in sysIDSTuple:
                tmpID = str(s[0][4:])
                if int(tmpID) - 1000 > 100 or True:
                    urlTmp = urlPut + '/' + s[1]
                    deleteIt(urlTmp)
                    print(s[0],"deleted")



if __name__ == "__main__":
    main()