#!/usr/bin/python3
import subprocess as sp
import os
ns="""apiVersion: v1
kind: Namespace
metadata:
  name: {}
"""
deployment="""apiVersion: apps/v1
kind: Deployment
metadata:
    namespace: {}
    name: {}-deployment
spec:
    template:
        metadata:
        spec:
            containers:
                - name: {}
                    image: {}
                    imagePullPolicy: Always
                    ports:
                            - containerPort: {}
                    resources:
                    limits:
                        cpu: {}
                    requests:
                        cpu: {}
                        memory: {}
"""
hpa="""kind: HorizontalPodAutoscaler
apiVersion: autoscaling/v1
metadata:
  name: {}-hpa
spec:
  maxReplicas: {}
  minReplicas: {}
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {}-deployment
  targetCPUUtilizationPercentage: {}
"""
svc="""
apiVersion: v1
kind: Service
metadata:
    name: {}-service   
spec:
    type: {}
    ports:
        - port: {}
          targetPort: {}
          protocol: {}

"""

def mkdir(path):
    namespace,app=path.split("/")
    try:
        if namespace not in os.listdir():
            os.mkdir(namespace)
        if app not in os.listdir(namespace):
            os.mkdir(namespace+"/"+app)
        return True
    except:
        return False

    with open(path+"/namespace.yml","wb") as file:
        file.write(str(ns.format(path.split('/')[0],values.get('app'),
        values.get('image'),values.get('cport'),lcpu,rcpu,rmem)).encode())
    with open(path+"/namespace.yml","wb") as file:
        file.write(str(ns.format(path.split('/')[0],values.get('app'),
        values.get('image'),values.get('cport'),lcpu,rcpu,rmem)).encode())
    with open(path+"/namespace.yml","wb") as file:
        file.write(str(ns.format(path.split('/')[0],values.get('app'),
        values.get('image'),values.get('cport'),lcpu,rcpu,rmem)).encode())
    with open(path+"/namespace.yml","wb") as file:
        file.write(str(ns.format(path.split('/')[0],values.get('app'),
        values.get('image'),values.get('cport'),lcpu,rcpu,rmem)).encode())
    with open(path+"/namespace.yml","wb") as file:
        file.write(str(ns.format(path.split('/')[0],values.get('app'),
        values.get('image'),values.get('cport'),lcpu,rcpu,rmem)).encode())
    with open(path+"/namespace.yml","wb") as file:
        file.write(str(ns.format(path.split('/')[0],values.get('app'),
        values.get('image'),values.get('cport'),lcpu,rcpu,rmem)).encode())
    with open(path+"/namespace.yml","wb") as file:
        file.write(str(ns.format(path.split('/')[0],values.get('app'),
        values.get('image'),values.get('cport'),lcpu,rcpu,rmem)).encode())
        newvar=vars(args).update({'app':vars(args)['app'][0]})
        print(newvar)
def mkfiles(path,values):
    lcpu=None
    rcpu=None
    rmem=None
    if values['pod_size']=="small":
        lcpu='100m'
        rcpu='100m'
        rmem='200Mi'
    elif values['pod_size']=="medium":
        lcpu='200m'
        rcpu='200m'
        rmem='200Mi'
    else:
        lcpu='400m'
        rcpu='400m'
        rmem='200Mi'

    try:
        with open(path+"/namespace.yml","wb") as file:
            file.write(str(ns.format(path.split('/')[0],values.get('app'),
            values.get('image'),values.get('cport'),lcpu,rcpu,rmem)).encode())
        with open(path+"/deployment.yml","wb") as file:
            file.write(str(deployment.format(path.split('/')[0],values.get('app'),values.get('app'),
            values.get('image'),values.get('cport'),lcpu,rcpu,rmem)).encode())
        with open(path+"/hpa.yml","wb") as file:
            file.write(str(hpa.format(values.get('app'),values.get('minimum_replica'),
            values.get('maximum_replica'),values.get('app'),values.get('cpu_threshold'))).encode())
        with open(path+"/service.yml","wb") as file:
            file.write(str(svc.format(values.get('app'),values.get('service_type'),
            values.get('cport'),values.get('cport'),values.get('protocol'))).encode())
        return True
    except:
        return False

def config():
    global H
    global P
    isfound=[False,False]
    if ".k8config" in os.listdir():
        if os.stat("./.k8config").st_size == 0:
            return '''The Configuration file is Empty.\nPlease configure you application first with HOSTNAME and PORT variable refering to hostname and portnuimber of the server.'''
        else:
            with open(".k8config","rb") as file:
                    metadata=[i.decode().strip() for i in file]
                    for i in metadata:
                        data=i.split('=')
                        if data[0].upper()=='HOSTNAME':
                            isfound[0]=True
                            H=data[1]
                        elif data[0].upper()=='PORT':
                            isfound[1]=True
                            P=data[1]
                        else:
                            return '''Alert!!!!!! Configuration corrupted.\nThe configuration file does not contain HOSTNAME and PORT variable.\nPlease configure you Application.'''

    if isfound[0]==True and isfound[1]==True:
        return True
    else:
        return '''The configuration file does not contain HOSTNAME and PORT variable.\nPlease configure you Application.'''
    """isConfigured=config()
    if isConfigured is True:
        k8c()
    else:
        global H
        global P
        print("\n"*2)
        print(isConfigured)
        print("\n")
        res=input("Do You Want To Configure Now? Press 'y' or 'yes' to continue else press 'n'or 'no' to EXIT :   ")
        if res=='y' or res=='yes':
            H=HOSTNAME=input("Please enter server's ip or fqdn . Eg: 13.26.128.30 or api.server.example.com :   ")
            P=PORT=input("Please enter the port number of the server on the the receiver program is running. Eg: 8080 :   ")
            with open(".k8config","wb") as file:
                file.write(str('HOSTNAME='+HOSTNAME+"\n"+"PORT="+PORT).encode())
            print("Configuration successful. Please proceed with ahead.")
            k8c()
        else:
            exit('Thanks .......... But unless you configure, i wil not allow to to use me. Either configure using the client program or manually make entries of HOSTNAME and PORT variable in the .k8config file in the current directory.')



        from flask import Flask ,request, make_response
        from flask_cors import CORS
        app = Flask(__name__)
        CORS(app)
        @app.route('/create',methods=["POST"])
        def create():
            
            request.form.to_dict()
            a=request.form.get('app')
            print(a)
            resp = make_response(a)
            #resp.headers["Set-Cookie"] = "myfirstcookie=somecookievalue"
            resp.set_cookie('userID', 'kooooooooooooooooooo')
            return resp
        app.run(host="0.0.0.0",port="5000",ssl_context="adhoc")"""


def updateCPUThreshold(path,values):
    try:
        with open("default/frontend/hpa.yml","rb") as file:
            data=file.read()
            data = data.replace('targetCPUUtilizationPercentage:'.encode(), 'targetCPUUtilizationPercentage: {} #'.format().encode())

        with open("default/frontend/hpa.yml","wb") as file:
            file.write(data)
        return True
    except:
        return False['minimum_replica']
def updateHPAReplicas(path,values):
    __=path.split('/')
    if __[0] not in os.listdir():
        return "Namespace not found. Please check your Namespace name again."
    if __[1] not in os.listdir(__[0]+'/'):
        return "Application not found. Please check your Application name again."
    try:
        with open(path+"/hpa.yml","rb") as file:
            data=file.read()
            if values['minimum_replica'] is not None:
                data = data.replace('minReplicas:'.encode(), str('minReplicas: {} #'.format(values['minimum_replica'])).encode())
            if values['minimum_replica'] is not None:
                data = data.replace('maxReplicas:'.encode(), 'maxReplicas: {} #'.format(values['maximum_replica']).encode())
        with open(path+"/hpa.yml","wb") as file:
            file.write(data)
        return "True"
    except:
        return "Failure: Your namespce directory and application directory is there in the server, but there is no file named 'hpa.yml'. Please contact your administrator."
############### Application Programming Interface ######################
from flask import Flask ,request, make_response, jsonify
from flask_cors import CORS
import subprocess as sp
from time import perf_counter
app = Flask(__name__)
CORS(app)
@app.route('/create',methods=["POST"])
def create():
    start=perf_counter()
    fdict=request.form.to_dict()
    path=fdict['namespace']+"/"+fdict['app']
    try:
        if mkdir(path):
            if mkfiles(path,fdict):
                x,y=sp.getstatusoutput("echo 'kubectl apply -f {path}/' > {path}/result.txt")
                if x==0:
                    return make_response(y,{'Time_taken:':start-perf_counter()})
    except:
        return "Fatal Error Occured. Please contact your Developer\n"+"Time_taken:={}".format(start-perf_counter())
@app.route('/updatecpu',methods=["POST"])
def updatecpu():
    start=perf_counter()
    fdict=request.form.to_dict()
    path=fdict['namespace']+"/"+fdict['app']
    try:
        if mkdir(path):
            if updateCPUThreshold(path,fdict):
                x,y=sp.getstatusoutput("echo 'kubectl apply -f {path}/' > {path}/result.txt")
                if x==0:
                    return make_response(y,{'Time_taken:':start-perf_counter()})
    except:
        return "Unknown Error Occured. Please contact your Developer\n"+"Time_taken:={}".format(start-perf_counter()) 
@app.route('/updatereplica',methods=["POST"])
def updatereplica():
    start=perf_counter()
    fdict=request.form.to_dict()
    path=fdict['namespace']+"/"+fdict['app']
    res=updateHPAReplicas(path,fdict)
    try: 
        if  res=="True":
            x,y=sp.getstatusoutput("echo 'kubectl apply -f {}/' > {}/result.txt".format(path,path))
            if x==0:
                return y+"\nTime_taken:':{}".format(perf_counter()-start)+" nanoseconds"
            else:
                return "Files created successfully, but unfortunately we failed to run 'kubectl apply -f ...' command. Please contact your admin"+"\nTime_taken:':{}".format(perf_counter()-start)+" nanoseconds" 
        else:
            return res
    except:
        return "Unkown Error Occured. Please contact your Developer"+"\nTime_taken:':{}".format(perf_counter()-start)+" nanoseconds"

app.run(debug=False,host="0.0.0.0",port="5000",ssl_context="adhoc")
