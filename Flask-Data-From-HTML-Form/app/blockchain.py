from pprint import pprint
import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# url = os.getenv("URL")
# url = os.getenv("URL")


SPA_URL=os.getenv("SPA_URL")
SPA_CC=os.getenv("SPA_CC")
SPA=os.getenv("SPA")
SCA_URL=os.getenv("SCA_URL")
SCA=os.getenv("SCA")
RET_URL=os.getenv("RET_URL")
RET=os.getenv("RET")
FAR_URL=os.getenv("FAR_URL")
FAR=os.getenv("FAR")
STL_URL=os.getenv("STL_URL")
STL=os.getenv("STL")
chaincodeVer = "v1"


headers = {
  'Content-Type': 'application/json',
  'Authorization': os.getenv("AUTH")
}

spa_keys = ['ID', 'lotNumber', 'owner', 'crop', 'variety', 'sourceTagNo', 'sourceClass', 'destinationClass', 'sourceQuantity', 'sourceDateOfIssue', 'spaName', 'sourceStoreHouse', 'destinationStoreHouse', 'sgName', 'sgId', 'finYear', 'season', 'landRecordsKhataNo', 'landRecordsPlotNo', 'landRecordsArea', 'cropRegistrationCode', 'sppName', 'sppId']

sca_keys = ['scaName', 'totalQuantityProduced', 'processingDate', 'verificationDate', 'sampleSecretCode', 'sampleTestDate', 'certificateNumber', 'certificateDate', 'tagSeries', 'tagIssuedRangeFrom', 'tagIssuedRangeTo', 'noOfTagsIssued', 'cetificateValidityInMonth']

stl_keys = ["stlName", "samplePassed"]

dist_keys = ["sourceDistributer", "storeHouseLocation", "humidityOfStorage", "temperatureOfStorage", "orderId"]

channel = "orangechannel"
chaincode = "seedBlockk"
chaincodeVer = "v6"

def invoke(data):
    for k in sca_keys:
        data[k] = ""
    for k in stl_keys:
        data[k] = ""
    for k in dist_keys:
        data[k] = ""

    payload = {
        "args": ["invoke", data["ID"], json.dumps(data)],
        "chaincode": SPA_CC,
        "channel": SPA,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", SPA_URL, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def updateTest(ID,data):
    data = {k:v for k,v in data.items() if k in stl_keys}

    payload = {
        "args": ["updateTest", ID, json.dumps(data)],
        "chaincode": STL,
        "channel": STL,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", STL_URL, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def updateCertification(ID, data):
    data = {k:v for k,v in data.items() if k in sca_keys}
    payload = {
        "args": ["updateCertification", ID, json.dumps(data)],
        "chaincode": SCA,
        "channel": SCA,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", SCA_URL, headers=headers, json=payload)
    print(response)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def updateDist(ID, data):
    data = {k:v for k,v in data.items() if k in dist_keys}
    payload = {
        "args": ["updateDist", ID, json.dumps(data)],
        "chaincode": RET,
        "channel": RET,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", RET_URL, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def getHistory(ID):
    payload = {
        "args": ["getHistory", ID],
        "chaincode": FAR,
        "channel": FAR,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", FAR_URL, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def query(ID):
    payload = {
        "args": ["query", ID],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']
