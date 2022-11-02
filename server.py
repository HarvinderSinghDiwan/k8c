#!/usr/bin/python3
import subprocess as sp
import os
from unicodedata import name
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
val={'app': 'mydep', 'image': 'myname','pod_size':'small','cport':80,'protocol':'TCP' ,'service_type':'nodeport','cpu_threshold': 80, 'minimum_replica': 3, 'maximum_replica': 3}
print(mkdir("newapp/frontend"))
print(mkfiles("newapp/frontend",val))

