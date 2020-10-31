from pprint import pprint
import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("URL")

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
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def updateTest():

    payload = {
        "args": ["updateTest", ID, json.dumps(data)],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def updateCertification(ID, data):
    payload = {
        "args": ["updateCertification", ID, json.dumps(data)],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def updateDist(ID, data):
    payload = {
        "args": ["updateDist", ID, json.dumps(data)],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return json.loads(response.text.encode('utf8'))['result']['payload']

def getHistory(ID):
    payload = {
        "args": ["getHistory", ID],
        "chaincode": chaincode,
        "channel": channel,
        "chaincodeVer": chaincodeVer,
        "method": "invoke"
    }

    response = requests.request("POST", url, headers=headers, json=payload)

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
