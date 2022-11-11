#!/usr/bin/python3
import subprocess as sp
import os
import yaml
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


def mkfiles(path,values):
    lcpu=None
    rcpu=None
    rmem=None
    if values['pod-size']=="small":
        lcpu='100m'
        rcpu='100m'
        rmem='200Mi'
    elif values['pod-size']=="medium":
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

def updateCPUThreshold(path,values):
    __=path.split('/')
    if __[0] not in os.listdir():
        return "Namespace not found. Please check your Namespace name again."
    if __[1] not in os.listdir(__[0]+'/'):
        return "Application not found. Please check your Application name again."
    try:
        with open(path+"/hpa.yml",'rb') as file:
            yf=yaml.safe_load(file)
            if values.get('cpu_threshold'):
                yf['spec']['targetCPUUtilizationPercentage']=int(values['cpu_threshold'])
            yf=yaml.safe_dump(yf)
        with open(path+"/hpa.yml","wb") as file:
            file.write(yf.encode())
        return "True"
    except:
        return "Failure: Your namespce directory and application directory is there in the server, but there is no file named 'hpa.yml'. Please contact your administrator."
def updateHPAReplicas(path,values):
    print(values)
    __=path.split('/')
    if __[0] not in os.listdir():
        return "Namespace not found. Please check your Namespace name again."
    if __[1] not in os.listdir(__[0]+'/'):
        return "Application not found. Please check your Application name again."
    try:
        with open(path+"/hpa.yml",'rb') as file:
            print(path+"/hpa.yml")
            yf=yaml.safe_load(file)
            if values.get('maximum_replica') :
                yf['spec']['maxReplicas']=int(values['maximum_replica'])
            if values.get('minimum_replica'):
                yf['spec']['minReplicas']=int(values['minimum_replica'])
            yf=yaml.safe_dump(yf)
        with open(path+"/hpa.yml","wb") as file:
            file.write(yf.encode())
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
                x,y=sp.getstatusoutput("echo 'kubectl apply -f {}/' > {}/result.txt".format(path,path))
                if x==0:
                    return "Result: Application Creation Successful\n"+"Metadata: "+y+"\nTime_taken : {}".format(perf_counter()-start)+" nanoseconds"
                else: 
                    return "Result: Application Creation Failed\n"+"Description: Files created successfully, but unfortunately we failed to run 'kubectl apply -f ...' command. Please contact your admin"+"\nTime_taken : {}".format(perf_counter()-start)+" nanoseconds"
                    
    except:
        return "Result: Failed\n Description: Fatal Error Occured. Please contact your Developer\n"+"Time_taken:={}".format(start-perf_counter())
@app.route('/updatecpu',methods=["POST"])
def updatecpu():
    start=perf_counter()
    fdict=request.form.to_dict()
    path=fdict['namespace']+"/"+fdict['app']
    res=updateCPUThreshold(path,fdict)
    try: 
        if  res=="True":
            x,y=sp.getstatusoutput("echo 'kubectl apply -f {}/' > {}/result.txt".format(path,path))
            if x==0:
                return "Result: CPU Update Successful\nMetadata: "+y+"\nTime_taken : {}".format(perf_counter()-start)+" nanoseconds"
            else:
                return "Result: CPU Update Failed\n"+"Description: Files created successfully, but unfortunately we failed to run 'kubectl apply -f ...' command. Please contact your admin"+"\nTime_taken : {}".format(perf_counter()-start)+" nanoseconds" 
        else:
            return res
    except:
        return "Result: Failed\n Description: Unkown Error Occured. Please contact your Developer"+"\nTime_taken : {}".format(perf_counter()-start)+" nanoseconds"
@app.route('/updatereplica',methods=["POST"])
def updatereplica():
    start=perf_counter()
    fdict=request.form.to_dict()
    path=fdict['namespace']+"/"+fdict['app']
    print(fdict)
    res=updateHPAReplicas(path,fdict)
    try: 
        if  res=="True":
            x,y=sp.getstatusoutput("echo 'kubectl apply -f {}/' > {}/result.txt".format(path,path))
            if x==0:
                return "Result: Updating Replication Factor Successful\nMetadata: "+y+"\nTime_taken : {}".format(perf_counter()-start)+" nanoseconds"
            else:
                return "Result: Updating Replication Factor Failed\n"+"Description: Files created successfully, but unfortunately we failed to run 'kubectl apply -f ...' command. Please contact your admin"+"\nTime_taken : {}".format(perf_counter()-start)+" nanoseconds" 
        else:
            return res
    except:
        return "Result: Failed\n Metadata: Unkown Error Occured. Please contact your Developer"+"\nTime_taken : {}".format(perf_counter()-start)+" nanoseconds"

app.run(debug=False,host="0.0.0.0",port="5000",ssl_context="adhoc") 
