from flask import Flask,render_template,flash, redirect,url_for,session,request,jsonify
from werkzeug.datastructures import ImmutableMultiDict
import logging
import os
import base64
import hashlib
app = Flask(__name__)
log = logging.getLogger(__name__)



@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        #sql query to check login
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("index"))
    
    return render_template("common_login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        agency = request.form['agency']
        agencyMail = request.form['agencyMail']
        agencyType = request.form['agencyType']
        authorizationId = request.form['authorizationId']
        username = request.form['username']
        password = request.form['password']
        
        data = request.form.to_dict(flat=True)
        print(data)

        #currently redirects to login page after you signup
        return redirect((url_for("login")))
        # if request.form['agencyType'] == "SPA":
            
        #     return redirect(url_for("login"))

    return render_template("agency_reg_index.html")


@app.route("/spa", methods=["GET", "POST"])
def spa_create():
    if request.method == "POST":       
        data = request.form.to_dict(flat=True)
        print(data)
        #currently redirects to login page after you signup
        return redirect(url_for("login"))
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




# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')