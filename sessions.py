from flask import Flask ,request, jsonify, Response, stream_with_context
from flask_cors import CORS
import time
import base64
import json
#from asgiref.wsgi import WsgiToAsgi
import pymongo
mongoHost="ec2-52-66-189-107.ap-south-1.compute.amazonaws.com"
mongoPort=27017
client=pymongo.MongoClient("mongodb://{}:{}/".format(mongoHost,mongoPort))
db=client['faldb']
usdoc=db['users']
sesdoc=db['sessions']
duration=120
app = Flask(__name__)
CORS(app)


@app.route('/verifysession',methods=["POST"])
def verifysession():
    session=request.json
    cur=usdoc.find({"emailid":session['emailid']})
    if cur.collection.count_documents({"emailid":session['emailid']})==1:
        cur=sesdoc.find(session)
        if cur.collection.count_documents(session)==1:
            status=cur[0]["status"]
            info=base64.b64decode(str(status).encode()).decode()
            if float(json.loads(info)['age'])<time.time():
                return "SessionExpired"
            else:
                return "SessionAlive"
        else:
            return "SessionExpired"
    else:
        return   "UnregisteredUser"   
    

@app.route('/createsession',methods=["POST"])
def createsession():
    session=request.json
    cur=usdoc.find({"emailid":session['emailid']})
    if cur.collection.count_documents({"emailid":session['emailid']})==1:
        cur=sesdoc.find({"emailid":session['emailid']})
        if cur.collection.count_documents({"emailid":session['emailid']})==1:
            status=base64.b64encode(json.dumps({"id":"{}".format(session['emailid']),"age":"{}".format(time.time()+duration)}).encode()).decode()
            #res=sesdoc.update_one({"emailid":session['emailid']},{"$set":{'status':status}})
            try:
                res=res=sesdoc.update_one({"emailid":session['emailid']},{"$set":{'status':status}})
                if res.acknowledged is True and res.matched_count == 1 and res.modified_count ==1 :
                    return {"SessionStatus":status}
            except:
                return {"SessionStatus":"UpdateFailed"}
        else:
            status=base64.b64encode(json.dumps({"id":"{}".format(session['emailid']),"age":"{}".format(time.time()+duration)}).encode()).decode()
            res=sesdoc.insert_one({"emailid":session['emailid'],'status':status})
            try:
                if res.acknowledged is True:
                    return {"SessionStatus":status}
            except:
                return {"SessionStatus":"InsertionFailed"}
    else:
        return "UnregisteredUser" 

app.run(debug=False,host="0.0.0.0",port="5000",ssl_context="adhoc")