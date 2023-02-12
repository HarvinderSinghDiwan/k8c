from flask import Flask ,request, jsonify, Response, stream_with_context
from flask_cors import CORS
import time
import base64
from functools import wraps
import json
#from asgiref.wsgi import WsgiToAsgi
import pymongo
mongoHost="ec2-13-235-103-193.ap-south-1.compute.amazonaws.com"
mongoPort=27017
client=pymongo.MongoClient("mongodb://{}:{}/".format(mongoHost,mongoPort))
db=client['faldb']
appdoc=db['apps']
sesdoc=db['sessions']
app = Flask(__name__)
CORS(app)
def checkappexistenceforFalse(func):
    @wraps(func)
    def inner():
        data=request.json
        id=data['emailid']
        domain=data['app']['id']
        if appdoc.find({"emailid":id}).collection.count_documents({"emailid":id,"apps.id":domain})==0:
            return func()
        else: return "AppAlreadyExists"
    return inner
def checkappexistenceforTrue(func):
    @wraps(func)
    def inner():
        data=request.json
        id=data['emailid']
        domain=data['app']['id']
        if appdoc.find({"emailid":id}).collection.count_documents({"emailid":id,"apps.id":domain})==1:
            return func()
        else: return "AppDoesNotExist"
    return inner

@app.route('/createapp',methods=["POST"])
@checkappexistenceforFalse
def createaapp():
    data=request.json
    id=data['emailid']
    domain=data['app']['id']
    app=data['app']
    try:
        if appdoc.find({"emailid":id}).collection.count_documents({"emailid":id})==0:
            res=appdoc.insert_one({"emailid":id,"apps":[app]})
            print(dir(res))
            if res.acknowledged is True :
                return "appSuccessfullyCreated"
        else:
            res=appdoc.update_one({"emailid":id},{"$push":{"apps":app}})
            print(dir(res))
            return "appSuccessfullyCreated"
    except:
        return "WritingToDatabaseFailed"
@app.route('/deleteapp',methods=["POST"])
@checkappexistenceforTrue
def deleteapp():
    data=request.json
    id=data['emailid']
    domain=data['app']['id']
    res=appdoc.update_one({"emailid":id},{"$pull":{"apps":{"id":domain}}})
    print(dir(res))
    return "appSuccessfullyCreated"

@app.route('/updateapp',methods=["POST"])
@checkappexistenceforTrue
def updateapp():
    data=request.json
    id=data['emailid']
    domain=data['app']['id']
    s=[]
    
    try:
        if data['app']['server_size'] is not None:
            s.append('server_size')
    except:
        pass
    try:
        if data['app']['tb'] is not None:
            s.append('tb')
    except:
        pass    
    try:    
        if data['app']['st'] is not None:
            s.append('st')
    except:
        pass
    res={}
    _res=[res.update({"apps.$."+str(i):data['app'][i]}) for i in s]
    print(s)
    print(res)
    try:
        res=appdoc.update_one({"emailid":id,"apps.id":domain},{"$set":res})
        print(res.raw_result)
        if res.acknowledged is True and res.matched_count == 1 and res.modified_count ==1 :
            return "AppSuccessfullyUpdated"
        else:
            return "FailedToUpdateApp"
    except:
        return "WritingToDatabaseFailed" 
app.run(debug=False,host="0.0.0.0",port="5000",ssl_context="adhoc")