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
from borneo import TableLimits, TableRequest, PutRequest, QueryRequest, PrepareRequest, DeleteRequest
from collections import OrderedDict
import random
import itertools

<<<<<<< HEAD
=======
app.secret_key = "somesecretkey"


#to drop tables
"""
statement = 'drop table USER'
request = TableRequest().set_statement(statement)
result = handle.do_table_request(request, 40000, 3000)

statement = 'drop table SEED_BLOCK'
request = TableRequest().set_statement(statement)
result = handle.do_table_request(request, 40000, 3000)
"""

#to create the registration details table
statement = 'create table if not exists USER(username string, name string, password string, mail string, type string, farmer json, agency json, ' + 'primary key(username))' 
req = TableRequest().set_statement(statement).set_table_limits(
    TableLimits(20, 10, 5))
result = handle.do_table_request(req, 40000, 3000)

statement = 'create table if not exists SEED_BLOCK(lot_no string, seed_data json, ' + 'primary key(lot_no))' 
req = TableRequest().set_statement(statement).set_table_limits(
    TableLimits(20, 10, 5))
result = handle.do_table_request(req, 40000, 3000)

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

def soil_fertility(fi, fs):
    """Obtain Firtility Class from fertility Index"""
    try:
        if fi < 1.67:
            fertility_status = "low"
        if fi<=2.33 and fi>=1.67:
            fertility_status =  "medium"
        
        else:
            fertility_status = "high"
            
        if fertility_status == fs.lower():
            trust = 1
        else:
            if fertility_status == "low" and fs.lower=="high":
                trust = 0
            else:
                trust = 0.5
        return calculatedFertilityStatus, calculatedTrust
     
    except Exception as e:
        return str(e),''

def scoring(score, distributorName, certified,stlName,seedGrowerName):
    """
    score: score provided by farmer
    """
    if score <= 2:
        if certified == 'No':
            stlScore = 2
            distributorScore = 0
            seedGrower = score
        if certified == 'Yes':
            stlScore = 0
            distributorScore = 1
            seedGrower = score
    elif score >= 4:
        if certified == 'Yes':
            stlScore = 5
            distributorScore = 5
            seedGrower = score
        elif certified == 'No':
            stlScore = 2
            distributorScore = 2
            seedGrower = score
    else:
        stlScore = 3
        distributorScore = 3
        seedGrower = 3
        
    return {stlName:stlScore, distributorName:distributorScore, seedGrowerName:seedGrower}


@app.route("/")
def home():
    #vary based of user type , to be done
    if "username" not in session:
        return redirect(url_for("login"))
    
    statement = 'select * from USER where username="{}"'.format(session["username"])
    req = QueryRequest().set_statement(statement)
    results = []
    while True:
        result = handle.query(req).get_results()
        results = results + result # do something with results
        if req.is_done():
            break

    temp = dict(results[0])
    #print(temp)
    name = temp["name"]
    type_login = temp["type"]
    if type_login == "farmer":
        #exec("farmer =" + temp["farmer"])
        #address = farmer["address"]
        session["login_type"]=type_login
        session["name"]=name
        return render_template("index.html",login_type=type_login)
    else:
        agencyType = json.loads(temp["agency"])["agencyType"]
        session["login_type"]=agencyType
        session["name"]=name
        return render_template("index.html",login_type=agencyType)

    
    #return render_template("index.html")

@app.route("/missions")
def missions():
    if "username" not in session:
        return render_template("index.html")
    return render_template("index.html",login_type=session["login_type"])

>>>>>>> d7c01febf854eb13dcc6185ace437985da4d90a5
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
        
<<<<<<< HEAD
        #sql query to check login
        # login = user.query.filter_by(username=uname, password=passw).first()
        # if login is not None:
        return redirect(url_for("common_login"))
    
    return render_template("common_login.html")
=======
        if len(qresults)==0:
            flash("user does not exist")
            return "user does not exist"
>>>>>>> d7c01febf854eb13dcc6185ace437985da4d90a5

        if check_password_hash(qresults[0]["password"],password):
            session['username']=username
            print("logged in as " + str(session['username']))
            return redirect(url_for("home"))
    
    return render_template("login.html")

@app.route("/logout",methods=["GET"])
def sign_out():
    session.pop('username',None)
    session.pop('login_type',None)
    session.pop('name',None)
    return redirect(url_for("login"))

@app.route("/register",methods=["POST","GET"])
def register():
    return render_template("register_options.html")

@app.route("/register_farmer", methods=["GET", "POST"])
def register_farmer():
    if request.method == "POST": 
        #data = request.get_json()

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
            return render_template(url_for("login"))
        else:
            flash("failed")
        
        return render_template("farmer_registration.html")
        
    return render_template("farmer_registration.html")

@app.route("/register_agency",methods=["POST","GET"])
def register_agency():
    if request.method=="POST":

        data = request.form.to_dict(flat=True)
        data["type"]="agency"
        data["agency"]={"agencyType":data["agencyType"]}
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
            return redirect(url_for("login"))
        else:
            flash("failed")

    return render_template("agency_registration.html")

@app.route("/distributor", methods=["POST","GET"])
def distributor_update():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = request.form.to_dict(flat=True)
        lno = data["lotNumber"]

        statement = 'select * from SEED_BLOCK where lot_no = "{}"'.format(lno)
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            results = results + result# do something with results
            if req.is_done():
                break    

        data.pop("lotNumber")
        dict1 = json.loads(dict(results[0])["seed_data"])
        data = {**dict1,**data}

        req = DeleteRequest().set_table_name('SEED_BLOCK')
        req.set_key({'lot_no': lno})

        result = handle.delete(req)
        if result.get_success():
            req = PutRequest().set_table_name('SEED_BLOCK')
            req.set_value({
                'lot_no': lno,
                'seed_data':json.dumps(data)})
            result = handle.put(req)
            
        else:
            print("updation failed")
        return redirect(url_for("home"))
    
    return render_template("distributor_update.html",login_type=session["login_type"],name=session["name"])

@app.route("/track_seed", methods=["POST","GET"])
def track_seed():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = request.form.to_dict(flat=True)
        lno = data["lotNumber"]
        #print(lno)
        statement = 'select seed_data from SEED_BLOCK where lot_no = "{}"'.format(lno)
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            results = results + result# do something with results
            if req.is_done():
                break
        #print(results) 
        seed_data = json.loads(dict(results[0])["seed_data"])
        #print(type(seed_data))        
        return render_template("track_seed.html",data=seed_data,login_type=session["login_type"])
    data={}
    return render_template("track_seed.html",login_type=session["login_type"],data=data)

@app.route("/spa", methods=["GET", "POST"])
def spa_create():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":       
        data = request.form.to_dict(flat=True)
<<<<<<< HEAD
        print(data)
        print(data.keys())
        print(len(list(data.keys())))
        #currently redirects to login page after you signup
        
        return redirect(url_for("login"))
    return render_template("spa_create.html")
=======
        lno = data["lotNumber"]
        
        statement = 'select * from SEED_BLOCK where lot_no = "{}"'.format(lno)
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            results = results + result# do something with results
            if req.is_done():
                break
        
        if len(results)==0:
            data.pop("lotNumber")
            req = PutRequest().set_table_name('SEED_BLOCK')
            req.set_value({'lot_no': lno,'seed_data':json.dumps(data)})
            result = handle.put(req)
            if result.get_version() is not None:
                return redirect(url_for("home"))
               
        else:
            print("insertion failed")

        #print(data)
        #currently redirects to login page after you signup
        #return redirect(url_for("home"))
        return redirect(url_for("home"))
    return render_template("spa_create_seed.html",login_type=session["login_type"])

>>>>>>> d7c01febf854eb13dcc6185ace437985da4d90a5

@app.route("/stl", methods=["GET", "POST"])
def stl_update():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":       
        data = request.form.to_dict(flat=True)
<<<<<<< HEAD
        # print(data)
        print(data.keys())
        # print(len(list(data.keys())))
=======
        print(data)

        lno = data["lotNumber"]

        statement = 'select * from SEED_BLOCK where lot_no = "{}"'.format(lno)
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            results = results + result# do something with results
            if req.is_done():
                break    

        data.pop("lotNumber")
        dict1 = json.loads(dict(results[0])["seed_data"])
        data = {**dict1,**data}

        req = DeleteRequest().set_table_name('SEED_BLOCK')
        req.set_key({'lot_no': lno})

        result = handle.delete(req)
        if result.get_success():
            req = PutRequest().set_table_name('SEED_BLOCK')
            req.set_value({
                'lot_no': lno,
                'seed_data':json.dumps(data)})
            result = handle.put(req)
        else:
            print("updation failed")

>>>>>>> d7c01febf854eb13dcc6185ace437985da4d90a5
        #currently redirects to login page after you signup
        return redirect(url_for("home"))
    #print("hello")
    #print(session["name"])  
    return render_template("stl_update_seed.html",login_type=session["login_type"],name=session["name"])


@app.route("/sca", methods=["GET", "POST"])
def sca_update():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":       
        data = request.form.to_dict(flat=True)
<<<<<<< HEAD
        # print(data)
        print(data.keys())
        # print(len(list(data.keys())))
=======
        #print(data)
        
        lno = data["lotNumber"]

        statement = 'select * from SEED_BLOCK where lot_no = "{}"'.format(lno)
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            results = results + result# do something with results
            if req.is_done():
                break    

        data.pop("lotNumber")
        dict1 = json.loads(dict(results[0])["seed_data"])
        data = {**dict1,**data}

        req = DeleteRequest().set_table_name('SEED_BLOCK')
        req.set_key({'lot_no': lno})

        result = handle.delete(req)
        if result.get_success():
            print("hello")
            req = PutRequest().set_table_name('SEED_BLOCK')
            req.set_value({
                'lot_no': lno,
                'seed_data':json.dumps(data)})
            result = handle.put(req)
        else:
            print("updation failed")

>>>>>>> d7c01febf854eb13dcc6185ace437985da4d90a5
        #currently redirects to login page after you signup
        return redirect(url_for("home"))
    
    return render_template("sca_update_seed.html",login_type=session["login_type"],name=session["name"])

@app.route("/spp",methods=["GET","POST"])
def spp_update():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = request.form.to_dict(flat=True)
            
        lno = data["lotNumber"]

        statement = 'select * from SEED_BLOCK where lot_no = "{}"'.format(lno)
        req = QueryRequest().set_statement(statement)
        results = []
        while True:
            result = handle.query(req).get_results()
            results = results + result# do something with results
            if req.is_done():
                break    

        data.pop("lotNumber")
        dict1 = json.loads(dict(results[0])["seed_data"])
        data = {**dict1,**data}

        req = DeleteRequest().set_table_name('SEED_BLOCK')
        req.set_key({'lot_no': lno})

        result = handle.delete(req)
        if result.get_success():
            req = PutRequest().set_table_name('SEED_BLOCK')
            req.set_value({
                'lot_no': lno,
                'seed_data':json.dumps(data)})
            result = handle.put(req)
        else:
            print("updation failed")

        return redirect(url_for("home"))

    return render_template("spp_update_seed.html",login_type=session["login_type"])
                
             
"""# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
"""
if __name__=="__main__":
    app.debug=True
    app.run()
