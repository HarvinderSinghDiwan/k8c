#!/usr/bin/python3
import subprocess as sp
import os
from unicodedata import name
deplopyment="""apiVersion: apps/v1
kind: Deployment
metadata:
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
                        memory: "100Mi"
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
    name: {}-service     #custom-nginx-service1
spec:
    type: {}
    ports:
        - port: {} #80
          targetPort: {}  #80
          protocol: {} #TCP

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

def mkfiles(path,values):
    try:
        with open(path+"/deployment.yml","wb"):
            pass
        with open(path+"/hpa.yml","wb"):
            pass
        with open(path+"/service.yml","wb"):
            pass
        return True
    except:
        return False
val={'name': 'mydep', 'image': 'myname','pod_size':'small','cport':80,'protocol':'tcp' ,'service_type':'nodeport','cpu_threshold': 80, 'minimum_replica': 3, 'maximum_replica': 3}
mkdir("default/frontend")
mkfiles("default/frontend",val)
