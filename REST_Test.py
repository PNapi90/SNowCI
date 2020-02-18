#Need to install requests package for python
 #sudo easy_install requests
import requests
import random
import json


SNowInstance = 'https://dev61319.service-now.com/api/now/table/'



def PutIt(sys_id) -> dict:
    rVAl = random.randint(0,1)
    randVal = 'true' if rVAl else 'false'
    D = {
        'doer': sys_id,
        'did_it': randVal
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


urlPut = SNowInstance + 'x_444043_doit_doit'


url = 'https://dev61319.service-now.com/api/now/table/sys_user'
jsonResponseDoIt = getResponse(url,printIt=False)

n = len(jsonResponseDoIt['result'])
print("")
print(n,"records found\n")

names = [[record['name'],record['sys_id']] for record in jsonResponseDoIt['result']]

DELETE = True

if not(DELETE):
    for i,n in enumerate(names):
        print(i,"->",n[0],n[1])
        if i < 100:
            D = PutIt(n[1])
            tmpString = str(D)
            #print(D)
            POST(urlPut,tmpString)
        else:
            break

else:
    DoIts = getResponse(urlPut)
    sysIDSTuple = [[d['number'],d['sys_id']] for d in DoIts['result']]

    for s in sysIDSTuple:
        tmpID = str(s[0][4:])
        if int(tmpID) - 1000 > 100:
            urlTmp = urlPut + '/' + s[1]
            deleteIt(urlTmp)
            print(s[0],"deleted")





"""
for i in range(n):
    num = jsonResponseDoIt['result'][i]['number']
    doer = jsonResponseDoIt['result'][i]['doer']['link']

    user = getRespone(doer,printIt=False)

    fname = user['result']['first_name']
    lname = user['result']['last_name']

    didArray = ["didn't do it","did it"]

    did = jsonResponseDoIt['result'][i]['did_it']

    correctType = did == 'true' or did == 'false'

    didIt = ""
    if correctType:
        pos = did == 'true'
        didIt = didArray[pos]

    print(num,"->",fname,lname,didIt)

#print(jsonResponse.get('doer'))
"""