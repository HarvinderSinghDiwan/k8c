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
