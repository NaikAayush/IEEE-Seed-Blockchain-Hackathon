from pprint import pprint
from blockchain import invoke, updateTest, updateCertification, updateDist, query, getHistory

ID = "12345678912345678"

pprint(
    invoke(    data = {
        "ID": ID,
        'lotNumber': 'APR19-33-028-117(2)', 'owner': 'OSSC', 'crop': 'Paddy',
        'variety': 'LALATA', 'sourceTagNo': 'F33162200068', 'sourceClass': 'Foundation-1',
        'destinationClass': 'Certified-1', 'sourceQuantity': '20KG',
        'sourceDateOfIssue': '02/05/2020', 'spaName': 'OSSC',
        'sourceStoreHouse': 'KHURDHA, PIN-753011',
        'destinationStoreHouse': 'PURI, PIN-7534511', 'sgName': 'Anand Singh',
        'sgId': 'AA-2345', 'finYear': '2020', 'season': 'Summer',
        'landRecordsKhataNo': '00031', 'landRecordsPlotNo': '1306',
        'landRecordsArea': '1.535', 'cropRegistrationCode': 'Z20-7-9',
        'sppName': 'M/S Brar Seeds Pvt. Ltd.', 'sppId': '33-001',
    }
           )
)


pprint(
    updateTest(ID,
data={'lotNumber': 'APR19-33-028-700', 'sampleSecretCode': 'abcd1234', 'samplePassed': 'Yes', 'sampleTestDate': '22-02-2020', 'stlName': 'admin_sca'})
)
pprint(
    updateCertification(ID,
                        data = {
                            'totalQuantityProduced': '55.5', 'processingDate': '', 'verificationDate': '', 'sampleSecretCode': 'abcd1234', 'sampleTestDate': '', 'certificateNumber': '', 'certificateDate': '', 'tagSeries': 'C7577', 'tagIssuedRangeFrom': 'C7577-4499115', 'tagIssuedRangeTo': 'C7577-4499534', 'noOfTagsIssued': '420', 'cetificateValidityInMonth': '9',
                            'scaName': "some certificate agency"
                        }
    )
)

pprint(
    updateDist(ID,
               data = {
                   "sourceDistributer": "haha",
                   "storeHouseLocation": "abcd",
                   "humidityOfStorage": "10%",
                   "temperatureOfStorage": "100C",
                   "orderId": "1234"
               }
               )
)

pprint(query(ID))

pprint(
    getHistory(ID)
)
