from flask import Flask,render_template,flash, redirect,url_for,session,request,jsonify
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user,login_user,logout_user,login_required
import logging
import os
import json
import base64
import hashlib
app = Flask(__name__)
#log = logging.getLogger(__name__)
from conn import handle
from borneo import TableLimits, TableRequest, PutRequest, QueryRequest, PrepareRequest
from collections import OrderedDict
import random
import  itertools

app.secret_key = "somesecretkey"

def uniqueid():
    """Generates a unique ID. Tested it for 1000 numbers, all of them were unique"""
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

def get_uniqueid(number_of_ids=1):
    """Wrapper for the above function
    params number_of_ids: int, enter the number of ids you want to generate
    Return: List of ids"""       
    unique_sequence = uniqueid()
    ids = list(itertools.islice(unique_sequence, number_of_ids))
    return ids

#to create the registration details table
statement = 'create table if not exists USER(username string, name string, password string, mail string, type string, farmer json, agency json, ' + 'primary key(username))' 
req = TableRequest().set_statement(statement).set_table_limits(
    TableLimits(20, 10, 5))
result = handle.do_table_request(req, 40000, 3000)

statement = 'create table if not exists SEED_BLOCK(lot_no string, seed_data json, ' + 'primary key(lot_no))' 
req = TableRequest().set_statement(statement).set_table_limits(
    TableLimits(20, 10, 5))
result = handle.do_table_request(req, 40000, 3000)


"""
#to drop tables
statement = 'drop table USER'
request = TableRequest().set_statement(statement)
result = handle.do_table_request(request, 40000, 3000)"""

#query
"""statement = 'select * from SG'
req = QueryRequest().set_statement(statement)
results = []
while True:
    result = handle.query(req).get_results()
    # handle results
    results = results + result
    # do something with results
    if req.is_done():
        break

for i in results:
    print(dict(i))
"""


@app.route('/profile')
def profile():
    return 'Profile'

@app.route("/")
def home():
    #vary based of user type , to be done
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        #print(username) 

        statement = 'declare $name string; select password from USER where username = $name'
        prequest = PrepareRequest().set_statement(statement)
        presult = handle.prepare(prequest)

        pstatement = presult.get_prepared_statement()
        pstatement.set_variable('$name', username)
        qrequest = QueryRequest().set_prepared_statement(pstatement)
        qresults = []
        while True:
            qresult = handle.query(qrequest).get_results()
            qresults = qresults + qresult # do something with results
            if qrequest.is_done():
                break
        
        if len(qresults)==0:
            flash("user does not exist")
            return "user does not exist"

        if check_password_hash(qresults[0]["password"],password):
            session['username']=username
            print("logged in as " + str(session['username']))

        #sql query to check login
        #login = user.query.filter_by(username=uname, password=passw).first()
        #if login is not None:
            #return redirect(url_for("index"))
    
    return render_template("common_login.html")

@app.route("/logout",methods=["GET"])
def logout():
    session.pop('username',None)
    return redirect(url_for("login"))

@app.route("/register",methods=["POST","GET"])
def register():
    return render_template("registration.html")

@app.route("/register_farmer", methods=["GET", "POST"])
def register_farmer():
    if request.method == "POST": 
        #data = request.get_json()
        required_fields = ["userid","name","password","email","phone","address","authid","agencytype"]

        data = request.form.to_dict(flat=True)
        #print(data)
        data["type"]="farmer"
        data["farmer"]={"phoneNumber":data["phoneNumber"],"address":data["address"]}
        data["agency"]={}

        statement = 'select username from USER'
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            # handle results
            results = results + result # do something with results
            if req.is_done():
                break

        for i in results:
            if data["username"] == i["username"]:
                flash("username already exists, please enter another username")
                return render_template("farmer_registration.html")

        req = PutRequest().set_table_name('USER')
        req.set_value({
            'username': data["username"],
            'name': data["name"],
            'password': generate_password_hash(data["password"]),
            'mail': data["mail"],
            'type':data["type"],
            'farmer':json.dumps(data["farmer"]),
            'agency':json.dumps(data["agency"])})
        result = handle.put(req)
        if result.get_version() is not None:
            #return "successful"
            return render_template("common_login.html")
        else:
            flash("failed")

        
        #currently redirects to login page after you signup
        #return redirect((url_for("login")))
        # if request.form['agencyType'] == "SPA":
            
        #     return redirect(url_for("login"))

    return render_template("farmer_registration.html")

@app.route("/register_agency",methods=["POST","GET"])
def register_agency():
    if request.method=="POST":

        data = request.form.to_dict(flat=True)
        data["type"]="agency"
        data["agency"]={"authorizationId":data["authorizationId"],"agencyType":data["agencyType"]}
        data["farmer"]={}
        
        statement = 'select username from USER'
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            # handle results
            results = results + result # do something with results
            if req.is_done():
                break

        for i in results:
            if data["username"] == i["username"]:
                flash("username already exists, please enter another username")
                return render_template("agency_registration.html")

        req = PutRequest().set_table_name('USER')
        req.set_value({
            'username': data["username"],
            'name': data["name"],
            'password': generate_password_hash(data["password"]),
            'mail': data["mail"],
            'type':data["type"],
            'farmer':json.dumps(data["farmer"]),
            'agency':json.dumps(data["agency"])})
        result = handle.put(req)
        if result.get_version() is not None:
            return render_template("common_login.html")
        else:
            flash("failed")

    return render_template("agency_registration.html")


@app.route("/tack_seed", methods=["POST","GET"])
def track_seed():
    if session['username']:
        
    return redirect(url_for("login"))

@app.route("/spa", methods=["GET", "POST"])
def spa_create():
    if request.method == "POST":       
        data = request.form.to_dict(flat=True)
        lno = data["lotNumber"]
        
        statement = 'select * from users where name = "{}"'.format(lno)
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            results = results + result# do something with results
            if req.is_done():
            break
        

        if len(qresults)==0:
            data.pop("lotNumber")
            req = PutRequest().set_table_name('USER')
            req.set_value({
                'lot_no': lno,
                'seed_data':json.dumps(data)})
                    """{"owner":data["owner"],
                    "crop":data["crop"],
                    "variety":data["variety"],
                    "sourceTagNo":data["sourceTagNo"],
                    "sourceClass":data["sourceClass"],
                    "destinationClass":data["destinationClass"],
                    "sourceQuantity":data["SourceQuantity"],
                    "sourceDateOfIssue":data["sourceDateOfIssue"],
                    "spaName":data["spaName"],
                    "sourceStoreHouse":data["sourceStoreHouse"],
                    "destinationStoreHouse":data["destinationStoreHouse"],
                    "sgName":data["sgName"],
                    "sgId":data["sgId"],
                    "finYear":data["finYear"],
                    "season":data["season"],
                    "landRecordsKhataNo":data["landRecordsKhataNo"],
                    "landRecordsPlotNo":data["landRecordsPlotNo"],
                    "landRecordsArea":data["landRecordsArea"],
                    "cropRegistrationCode":data["cropRegistrationCode"],
                    "sppName":data["sppName"],
                    "sppId":data["sppId"]
                    "village":data["village"],
                    "state":data["state"],
                    "temp":data["temp"],
                    "humidity":data["humidity"],
                    "durationOfGrowth":data["durationOfGrowth"],
                    "fertilizerType":data["fertilizerType"],
                    "fertilizerName":data["fertilizerName"],
                    "frequencyOfFertilization":data["frequencyOfFertilization"],
                    "organicPercentageInSoil":data["organicPercentageInSoil"],
                    "soilStructure":data["soilStructure"],
                    "averageSoilTemperature":data["averageSoilTemperature"],
                    "sandPercentage":data["sandPercentage"],
                    "siltPercentage":data["siltPercentage"],
                    "clayPercentage":data["clayPercentage"],
                    "fertilityStatus":data["fertilityStatus"],
                    "cotyledon":data["cotyledon"],
                    "optimalGerminationTemperature":data["optimalGerminationTemperature"],
                    "atmosphericPh":data["atmosphericPh"],
                    "dormancyPercentage":data["dormancyPercentage"],
                    "farmingType":data["farmingType"],
                    "geneticPurity":data["geneticPurity"],
                    "mostVulnerableDiseases":data["mostVulnerableDiseases"]
                    "storeHouseLocation":data["storeHouseLocation"],
                    "humidityOfStorage":data["humidityOfStorage"],
                    "temperatureOfStorage":data["temperatureOfStorage"]
                            }"""

                    #)})
            result = handle.put(req)
            if result.get_version() is not None:
            return render_template("common_login.html")
               
        else:
            



        #print(data)
        #currently redirects to login page after you signup
        
        return redirect(url_for("home"))
    return render_template("spa_create.html")

@app.route("/stl", methods=["GET", "POST"])
def stl_update():
    if request.method == "POST":       
        data = request.form.to_dict(flat=True)
        print(data)
        #currently redirects to login page after you signup
        return redirect(url_for("login"))
    
    return render_template("stl_update.html")


@app.route("/sca", methods=["GET", "POST"])
def sca_update():
    if request.method == "POST":       
        data = request.form.to_dict(flat=True)
        print(data)
        #currently redirects to login page after you signup
        return redirect(url_for("login"))
    
    return render_template("sca_update.html")

@app.route("/spp",methods=["GET","POST"])
def spp_create():
    if request.method == "POST":
        data = request.form.to_dict(flat=True)
            
        lno = data["lotNumber"]

        statement = 'select * from users where name = "{}"'.format(lno)
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            results = results + result# do something with results
            if req.is_done():
            break    

        if len(qresults)==0:
            data.pop("lotNumber")
            req = PutRequest().set_table_name('USER')
            req.set_value({
                'lot_no': lno,
                'seed_data':json.dumps(data)})
        else:
            dict1 = json.loads(dict())
             



# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

if __name__=="__main__":
    app.debug=True
    app.run()
