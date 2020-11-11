import mysql.connector
import uuid

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="nic",
  database="seeds"
)

mycursor = mydb.cursor()

def insertLotNumber(lotNumber):
    id = str(uuid.uuid4())
    sql = "INSERT INTO seed (uuid,lotNumber) VALUES (%s,%s)"
    val = (id, lotNumber)
    mycursor.execute(sql, val)
    mydb.commit()
    return id

def updateSampleSecretCode(lotNumber,sampleSecretCode):
    sql = "UPDATE seed SET sampleSecretCode = %s WHERE lotNumber=%s"
    val = (sampleSecretCode, lotNumber)
    mycursor.execute(sql, val)
    mydb.commit()

def returnUUIDSSC(sampleSecretCode):
    sql = "SELECT uuid FROM seed  WHERE sampleSecretCode=%s"
    val = (sampleSecretCode,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    try:
        myresult = myresult[0][0]
        return myresult
    except:
        return None

def returnUUIDLotNumber(lotNumber):
    sql = "SELECT uuid FROM seed  WHERE lotNumber=%s"
    val = (lotNumber,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    try:
        myresult = myresult[0][0]
        return myresult
    except:
        return None

def updateTagStuff(sampleSecretCode,tagSeries,tagStart,tagEnd):
    sql = "UPDATE seed SET tagSeries=%s,tagStart=%s,tagEnd=%s WHERE sampleSecretCode=%s"
    val = (tagSeries, int(tagStart), int(tagEnd), sampleSecretCode)
    mycursor.execute(sql, val)
    mydb.commit()

def returnUUIDtag(tag):
    arr = tag.split('-')
    tagSeries = arr[0]
    tagNo = int(arr[1])

    sql = "SELECT uuid FROM seed WHERE tagSeries=%s AND %s BETWEEN tagStart AND tagEnd"
    val = (tagSeries, tagNo)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    try:
        myresult = myresult[0][0]
        return myresult
    except:
        return None

def returnLotNumber(tag):
    arr = tag.split('-')
    tagSeries = arr[0]
    tagNo = int(arr[1])

    sql = "SELECT lotNumber FROM seed WHERE tagSeries=%s AND %s BETWEEN tagStart AND tagEnd"
    val = (tagSeries, tagNo)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    try:
        myresult = myresult[0][0]
        return myresult
    except:
        return None
