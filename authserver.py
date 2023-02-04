from flask import Flask ,request, jsonify, Response, stream_with_context
from flask_cors import CORS
import time
import base64
from functools import wraps
import json
#from asgiref.wsgi import WsgiToAsgi
import pymongo
mongoHost="ec2-52-66-189-107.ap-south-1.compute.amazonaws.com"
mongoPort=27017
client=pymongo.MongoClient("mongodb://{}:{}/".format(mongoHost,mongoPort))
db=client['faldb']
usdoc=db['users']
sesdoc=db['sessions']
app = Flask(__name__)
CORS(app)
def checkuserexistenceforFalse(func):
    @wraps(func)
    def inner():
        data=request.json
        id=data['emailid']
        passwd=data['passwd']
        if usdoc.find({"emailid":id}).collection.count_documents({"emailid":id})==0:
            return func()
        else: return "UserAlreadyExists"
    return inner
def checkuserexistenceforTrue(func):
    @wraps(func)
    def inner():
        data=request.json
        id=data['emailid']
        passwd=data['passwd']
        if usdoc.find({"emailid":id}).collection.count_documents({"emailid":id})==1:
            return func()
        else: return "UserDoesNotExist"
    return inner

@app.route('/createaccount',methods=["POST"])
@checkuserexistenceforFalse
def createaccount():
    data=request.json
    id=data['emailid']
    passwd=data['passwd']
    try:
        res=usdoc.insert_one({"emailid":id,"passwd":passwd})
        print(dir(res))
        if res.acknowledged is True :
            return "AccountSuccessfullyCreated"
    except:
        return "WritingToDatabaseFailed"
@app.route('/deleteaccount',methods=["POST"])
@checkuserexistenceforTrue
def deleteaccount():
    data=request.json
    id=data['emailid']
    try:
        res=usdoc.delete_one({"emailid":id})
        print(dir(res))
        if res.acknowledged is True and res.deleted_count==1:
            return "AccountSuccessfullyDeleted"
    except:
        return "WritingToDatabaseFailed"
@app.route('/updateaccount/id',methods=["POST"])
@checkuserexistenceforTrue
def updateid():
    data=request.json
    id=data['emailid']
    newmail=data['newmail']
    try:
        res=usdoc.update_one({"emailid":id},{"$set":{"emailid":newmail}})
        print(dir(res))
        if res.acknowledged is True and res.matched_count == 1 and res.modified_count ==1 :
            return "EmailIDSuccessfullyUpdated"
    except:
        return "WritingToDatabaseFailed"

@app.route('/updateaccount/passwd',methods=["POST"])
@checkuserexistenceforTrue
def updatepasswd():
    data=request.json
    id=data['emailid']
    oldpass=data['passwd']
    newpass=data['newpass']
    try:
        res=usdoc.update_one({"emailid":id,"passwd":oldpass},{"$set":{"passwd":newpass}})
        print(dir(res))
        if res.acknowledged is True and res.matched_count == 1 and res.modified_count ==1 :
            return "PasswdSuccessfullyUpdated"
    except:
        return "WritingToDatabaseFailed"
app.run(debug=False,host="0.0.0.0",port="5000",ssl_context="adhoc")