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
            print(os.listdir(namespace))
        if app not in os.listdir(namespace):
            os.mkdir(namespace+"/"+app)
            print(os.listdir(namespace))
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



def updateCPUThreshold(path,values):
    try:
        with open("default/frontend/hpa.yml","rb") as file:
            data=file.read()
            data = data.replace('targetCPUUtilizationPercentage:'.encode(), 'targetCPUUtilizationPercentage: {} #'.format().encode())

        with open("default/frontend/hpa.yml","wb") as file:
            file.write(data)
        return True
    except:
        return False
def updateHPAReplicas(path,values):
    try:
        with open("default/frontend/hpa.yml","rb") as file:
            data=file.read()
            data = data.replace('minReplicas:'.encode(), 'minReplicas: {} #'.format().encode())
            data = data.replace('maxReplicas:'.encode(), 'maxReplicas: {} #'.format().encode())
        with open("default/frontend/hpa.yml","wb") as file:
            file.write(data)
        return True
    except:
        return False
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
                    return make_response(y,{'time_taken':start-perf_counter()})
    except:
        return "Fatal Error Occured. Please contact your Developer\n"+"time_taken={}".format(start-perf_counter())
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
                    return make_response(y,{'time_taken':start-perf_counter()})
    except:
        return "Fatal Error Occured. Please contact your Developer\n"+"time_taken={}".format(start-perf_counter()) 
@app.route('/updatereplica',methods=["POST"])
def updatereplica():
    start=perf_counter()
    fdict=request.form.to_dict()
    path=fdict['namespace']+"/"+fdict['app']
    try:
        if mkdir(path):
            if updateHPAReplicas(path,fdict):
                x,y=sp.getstatusoutput("echo 'kubectl apply -f {path}/' > {path}/result.txt")
                if x==0:
                    return make_response(y,{'time_taken':start-perf_counter()})
    except:
        return "Fatal Error Occured. Please contact your Developer\n"+"time_taken={}".format(start-perf_counter())
app.run(debug=False,host="0.0.0.0",port="5000",ssl_context="adhoc")
