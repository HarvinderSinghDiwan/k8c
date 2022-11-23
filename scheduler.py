import subprocess as sp
import yaml
from math import ceil
from apscheduler.schedulers.background import BackgroundScheduler
patchInc="""spec:
    template:
        spec:
            containers:
            - name: productpage
              resources:
                limits:
                    cpu: 200m
                    memory: 400Mi
                requests:
                    cpu: 100m
                    memory: 200Mi"""
hpa="""apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: productpage-hpa
  namespace: bookinfo
  resourceVersion: "179215"
  uid: 0ce75eb6-7b97-42b2-ab4f-db92face1c46
spec:
  maxReplicas: 10
  metrics:
  - resource:
      name: cpu
      target:
        averageUtilization: 8
        type: Utilization
    type: Resource
  minReplicas: 4
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: productpage-v1"""
patchDec="""spec:
    template:
        spec:
            containers:
            - name: productpage
              resources:
                limits:
                    cpu: 100m
                    memory: 200Mi
                requests:
                    cpu: 50m
                    memory: 100Mi"""
"""def inc():
    with open("inc-patch.yml","wb") as file:
        file.write(patchInc.encode())
    #_,res=sp.getstatusoutput("echo {} > inc-patch.yml".format(patchInc))
    #print(res)
    _,res=sp.getstatusoutput("kubectl get hpa productpage-hpa -o yaml -n bookinfo")
    resyaml=yaml.safe_load(res)
    #print(resyaml)
    resyaml['spec']['maxReplicas']=10 #ceil(int(resyaml['spec']['maxReplicas'])/2)
    resyaml['spec']['minReplicas']=4#ceil(int(resyaml['spec']['minReplicas'])/2)
    resyaml['spec']['targetCPUUtilizationPercentage']=80
    resyaml=yaml.safe_dump(resyaml)
    print(resyaml)
    with open("productpage-hpa.yml","wb") as file:
        file.write(resyaml.encode())
    a,b=sp.getstatusoutput("kubectl patch deployment productpage-v1  --patch-file inc-patch.yml -n bookinfo")
    print(a,b)
    a,b=sp.getstatusoutput("kubectl patch hpa productpage-hpa  --patch-file productpage-hpa.yml -n bookinfo")
    print(a,b)"""
def inc():
    sp.getstatusoutput("echo {} > inc-patch.yml".format(patchInc))
    _,res=sp.getstatusoutput("kubectl get hpa productpage-hpa -o yaml -n bookinfo")
    resyaml=yaml.safe_load(res)
    resyaml['maxReplicas']=ceil(int(resyaml['maxReplicas'])/2)
    resyaml['minReplicas']=ceil(int(resyaml['minReplicas'])/2)
    resyaml=yaml.safe_dump(resyaml)
    with open("productpage-hpa","wb") as file:
        file.write(resyaml.encode())
    sp.getstatusoutput("kubectl patch deployment productpage-v1  --patch-file inc-patch.yml -n bookinfo")
    sp.getstatusoutput("kubectl patch hpa productpage-hpa  --patch-file productpage-hpa.yml -n bookinfo")
def dec():
    sp.getstatusoutput("echo {} > deca-patch.yml".format(patchDec))
    _,res=sp.getstatusoutput("kubectl get hpa productpage-hpa -o yaml -n bookinfo")
    resyaml=yaml.safe_load(res)
    resyaml['maxReplicas']=int(resyaml['maxReplicas'])*2
    resyaml['minReplicas']=int(resyaml['minReplicas'])*2
    resyaml=yaml.safe_dump(resyaml)
    with open("productpage-hpa","wb") as file:
        file.write(resyaml.encode())
    sp.getstatusoutput("kubectl patch deployment productpage-v1  --patch-file dec-patch.yml -n bookinfo")
    sp.getstatusoutput("kubectl patch  hpa productpage-hpa --patch-file productpage-hpa.yml -n bookinfo")
sched = BackgroundScheduler(daemon=False)
#sched.add_job(sensor,'interval',seconds=3)
sched.add_job(inc, 'cron', second='3,9')
sched.add_job(dec, 'cron', second='5,11')
sched.start()
while True:
    pass
    