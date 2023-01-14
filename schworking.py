from threading import Thread, Event
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.util import asbool
##################################
import subprocess as sp
import yaml
from math import ceil
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import sys
varDict={
  "recurrence": {
    "second": 0, 
    "hour": 4, 
    "date": "*", 
    "day": "*", 
    "minute": 41, 
    "month": "*"
  }, 
  "averageUtilization": 70, 
  "peakStart": "peaks", 
  "maxReplicas": 9, 
  "peakEnd": "peakend", 
  "resources": {
    "requests": {
      "cpu": "100m", 
      "memory": "100Mi"
    }, 
    "limits": {
      "cpu": "200m", 
      "memory": "400Mi"
    }
  }, 
  "metadata": {
    "containerName": "productpage", 
    "hpa": "productpage-v1", 
    "ns": "bi", 
    "svc": "productpage", 
    "deployment": "productpage-v1"
  }
}
varYaml="""metadata:
  ns:''
  deployment:''
  svc:''
  hpa:''
  containerName:''
peakStart:''
peakEnd:''
recurrence:
  hour:''
  minute:''
  second:''
  day:''
  date:''
  month:''
resources:
  limits:
    cpu:''
    memory:''
  requests:
    cpu:''
    memory:''
maxReplicas:''
averageUtilization:''
"""
class scheduler:
    def __init__(self,config):
        self.config=config
        try:
            sp.getstatusoutput("mkdir {}.{}".format(config['metadata']['ns'],config['metadata']['svc']))
            sp.getstatusoutput("mkdir {}.{}/manifests".format(config['metadata']['ns'],config['metadata']['svc']))
        except: pass
        with open("{}.{}/config.yaml".format(config['metadata']['ns'],config['metadata']['svc']),"wb") as file:
            resyaml=yaml.safe_dump(config)
            file.write(resyaml.encode())
    def peakInc(self):
        ns=self.config['metadata']['ns']
        svc=self.config['metadata']['svc']
        hpa=self.config['metadata']['hpa']
        deployment=self.config['metadata']['deployment']
        containerName=self.config['metadata']['containerName']

        _,res=sp.getstatusoutput("kubectl get deployment {} -o yaml -n {}".format(deployment,ns))
        if _ == 0:
            resyaml=yaml.safe_load(res)
            for i in range(len(resyaml['spec']['template']['spec']['containers'])):
                if resyaml['spec']['template']['spec']['containers'][i]['name']==containerName:
                    oldResource=resyaml['spec']['template']['spec']['containers'][i]['resources']
                    resyaml['spec']['template']['spec']['containers'][i]['resources']={"requests":{"cpu":"{}".format(self.config['resources']['requests']['cpu']),"memory":"{}".format(self.config['resources']['requests']['memory'])},"limits":{"cpu":"{}".format(self.config['resources']['limits']['cpu']),"memory":"{}".format(self.config['resources']['limits']['memory'])}}
                    resyaml=yaml.safe_dump(resyaml)
                    with open("{}.{}/manifests/deployment.yaml".format(ns,svc),"wb") as file:
                        file.write(resyaml.encode())
                    with open("{}.{}/config.yaml".format(self.config['metadata']['ns'],self.config['metadata']['svc']),"rb") as file:
                        yf=yaml.safe_load(file)
                        yf['resources']=oldResource
                        yf=yaml.safe_dump(yf)
                    with open("{}.{}/config.yaml".format(self.config['metadata']['ns'],self.config['metadata']['svc']),"wb") as file:
                        file.write(yf.encode())

                    break
            _,res=sp.getstatusoutput("kubectl get pods  -n {} | grep {}".format(ns,deployment))
            if _ == 0:
                podCount=ceil(len(res.split("\n"))/2)
                _,res=sp.getstatusoutput("kubectl get hpa {} -o yaml -n {}".format(hpa,ns))
                resyaml=yaml.safe_load(res)
                oldMax=resyaml['spec']['maxReplicas']
                oldMin=resyaml['spec']['minReplicas']
                oldAverageUtilization=resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']
                resyaml['spec']['maxReplicas']=self.config['maxReplicas']
                resyaml['spec']['minReplicas']=podCount
                resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']=self.config['averageUtilization']
                resyaml=yaml.safe_dump(resyaml)
                with open("{}.{}/manifests/hpa.yaml".format(ns,svc),"wb") as file:
                    file.write(resyaml.encode())
                with open("{}.{}/config.yaml".format(self.config['metadata']['ns'],self.config['metadata']['svc']),"rb") as file:
                    yf=yaml.safe_load(file)
                    yf['maxReplicas']=oldMax
                    yf['minReplicas']=oldMin
                    yf['averageUtilization']=oldAverageUtilization
                    yf=yaml.safe_dump(yf)
                with open("{}.{}/config.yaml".format(self.config['metadata']['ns'],self.config['metadata']['svc']),"wb") as file:
                    file.write(yf.encode())
                _,res=sp.getstatusoutput("kubectl apply -f {}.{}/manifests/ -n {}".format(ns,svc,ns))
                if _ == 0:
                    return 0
                else:
                    return "Manifest created successfully, but failed to apply."
            else:
                return "Error fetching pod counts"
    def peakDec(self):
        ns=self.config['metadata']['ns']
        svc=self.config['metadata']['svc']
        hpa=self.config['metadata']['hpa']
        deployment=self.config['metadata']['deployment']
        containerName=self.config['metadata']['containerName']
        with open("{}.{}/config.yaml".format(self.config['metadata']['ns'],self.config['metadata']['svc']),"rb") as file:
            yf=yaml.safe_load(file)
            _oldResource=yf['resources']
            _oldMax=yf['maxReplicas']
            _oldMin=yf['minReplicas']
            _oldAverageUtilization=yf['averageUtilization']
            yf=yaml.safe_dump(yf)
        _,res=sp.getstatusoutput("kubectl get deployment {} -o yaml -n {}".format(deployment,ns))
        if _ == 0:
            resyaml=yaml.safe_load(res)
            for i in range(len(resyaml['spec']['template']['spec']['containers'])):
                if resyaml['spec']['template']['spec']['containers'][i]['name']==containerName:
                    oldResource=resyaml['spec']['template']['spec']['containers'][i]['resources']
                    resyaml['spec']['template']['spec']['containers'][i]['resources']=_oldResource
                    resyaml=yaml.safe_dump(resyaml)
                    with open("{}.{}/manifests/deployment.yaml".format(ns,svc),"wb") as file:
                        file.write(resyaml.encode())
                    """with open("{}.{}/config.yaml".format(self.config['metadata']['ns'],self.config['metadata']['svc']),"rb") as file:
                        yf=yaml.safe_load(file)
                        yf['resources']=oldResource
                        yf=yaml.safe_dump(yf)
                    with open("{}.{}/config.yaml".format(self.config['metadata']['ns'],self.config['metadata']['svc']),"wb") as file:
                        file.write(yf.encode())"""
                    break
            #_,res=sp.getstatusoutput("kubectl get pods  -n {} | grep {}".format(ns,deployment))
            #if _ == 0:
                #podCount=ceil(len(res.split("\n"))/2)
            _,res=sp.getstatusoutput("kubectl get hpa {} -o yaml -n {}".format(hpa,ns))
            resyaml=yaml.safe_load(res)
            oldMax=resyaml['spec']['maxReplicas']
            oldMin=resyaml['spec']['minReplicas']
            oldAverageUtilization=resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']
            resyaml['spec']['maxReplicas']=_oldMax
            resyaml['spec']['minReplicas']=_oldMin
            resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']=_oldAverageUtilization
            resyaml=yaml.safe_dump(resyaml)
            with open("{}.{}/manifests/hpa.yaml".format(ns,svc),"wb") as file:
                file.write(resyaml.encode())
            with open("{}.{}/config.yaml".format(self.config['metadata']['ns'],self.config['metadata']['svc']),"rb") as file:
                yf=yaml.safe_load(file)
                yf['maxReplicas']=oldMax
                yf['minReplicas']=oldMin
                yf['averageUtilization']=oldAverageUtilization
                yf['resources']=oldResource
                yf=yaml.safe_dump(yf)
            with open("{}.{}/config.yaml".format(self.config['metadata']['ns'],self.config['metadata']['svc']),"wb") as file:
                file.write(yf.encode())
            _,res=sp.getstatusoutput("kubectl apply -f {}.{}/manifests/ -n {}".format(ns,svc,ns))
            if _ == 0:
                return 0
            else:
                return "Manifest created successfully, but failed to apply."
        else:
            return "Failed getting resource"

schobj=scheduler(varDict)
def inc():
    print(schobj.peakInc())
def dec():
    print(schobj.peakDec())

sched = BackgroundScheduler(daemon=False)
#sched.add_job(sensor,'interval',seconds=3)
sched.add_job(inc, 'cron', day='*' ,week='*' ,month='*',hour=varDict['recurrence']['hour'],minute=varDict['recurrence']['minute'], second=varDict['recurrence']['second'])
sched.add_job(dec, 'cron', hour=4,minute=43,second=0)
sched.start()