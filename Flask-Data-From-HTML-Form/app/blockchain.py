from pprint import pprint
import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# url = os.getenv("URL")
# url = os.getenv("URL")


SPA_URL=os.getenv("SPA_URL")
chaincode="seedBlockk"
chaincodeVer="v7"
channel="orangechannel"
# SPA_CC=os.getenv("SPA_CC")
# SPA=os.getenv("SPA")
# SPA_URL=os.getenv("SPA_URL")
# chaincode=os.getenv("chaincode")
# RET_URL=os.getenv("RET_URL")
# RET=os.getenv("RET")
# FAR_URL=os.getenv("FAR_URL")
# FAR=os.getenv("FAR")
# STL_URL=os.getenv("STL_URL")
# STL=os.getenv("STL")
# chaincodeVer = "v1"

headers = {
  'Content-Type': 'application/json',
  'Authorization': os.getenv("AUTH")
}

spa_keys = ['ID', 'lotNumber', 'owner', 'crop', 'variety', 'sourceTagNo', 'sourceClass', 'destinationClass', 'sourceQuantity', 'sourceDateOfIssue', 'spaName', 'sourceStoreHouse', 'destinationStoreHouse', 'sgName', 'sgId', 'finYear', 'season', 'landRecordsKhataNo', 'landRecordsPlotNo', 'landRecordsArea', 'cropRegistrationCode', 'sppName', 'sppId']

sca_keys = ['scaName', 'totalQuantityProduced', 'processingDate', 'verificationDate', 'sampleSecretCode', 'sampleTestDate', 'certificateNumber', 'certificateDate', 'tagSeries', 'tagIssuedRangeFrom', 'tagIssuedRangeTo', 'noOfTagsIssued', 'cetificateValidityInMonth']

stl_keys = ["stlName", "samplePassed"]

dist_keys = ["sourceDistributer", "storeHouseLocation", "humidityOfStorage", "temperatureOfStorage", "orderId"]

def invoke(data):
    for k in sca_keys:
        data[k] = ""
    for k in stl_keys:
        data[k] = ""
    for k in dist_keys:
        data[k] = ""

    payload = {
        "args": ["invoke", data["ID"], json.dumps(data)],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }
    pprint(payload)

    response = requests.request("POST", SPA_URL, headers=headers, json=payload)

    pprint(json.loads(response.text.encode('utf8')))
    return json.loads(response.text.encode('utf8'))['result']['payload']

def updateTest(ID,data):
    data = {k:v for k,v in data.items() if k in stl_keys}

    payload = {
        "args": ["updateTest", ID, json.dumps(data)],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }
    pprint(payload)

    response = requests.request("POST", SPA_URL, headers=headers, json=payload)

    pprint(json.loads(response.text.encode('utf8')))
    return json.loads(response.text.encode('utf8'))['result']['payload']

def updateCertification(ID, data):
    data = {k:v for k,v in data.items() if k in sca_keys}
    print(data)
    payload = {
        "args": ["updateCertification", ID, json.dumps(data)],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }
    pprint(payload)

    response = requests.request("POST", SPA_URL, headers=headers, json=payload)

    print(json.loads(response.text.encode('utf8')))
    return json.loads(response.text.encode('utf8'))['result']['payload']

def updateDist(ID, data):
    data = {k:v for k,v in data.items() if k in dist_keys}
    payload = {
        "args": ["updateDist", ID, json.dumps(data)],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", SPA_URL, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def getHistory(ID):
    payload = {
        "args": ["getHistory", ID],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", SPA_URL, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def query(ID):
    payload = {
        "args": ["query", ID],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", SPA_URL, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']
