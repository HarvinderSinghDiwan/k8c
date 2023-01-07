import subprocess as sp
from time import sleep
from time import perf_counter
import yaml
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
def findPort(namespace,svc,port):
    _,b=sp.getstatusoutput("kubectl get pods -n {} | grep {}".format(namespace,svc))
    print(len(b.split("\n")))
    a,b=sp.getstatusoutput("kubectl get svc -n {} | grep {}".format(namespace,svc))
    res=b.split()[-2].split(',')
    count=0
    for i in res:
        if i[:len(port)] == port:
            print("found at {}".format(count))
            break
        count+=1
    return res[count].split(":")[1].split("/")[0]
def mod(hpa,namespace):
    _,res=sp.getstatusoutput("kubectl get hpa {} -o yaml -n {}".format(hpa,namespace))
    resyaml=yaml.safe_load(res)
    _=resyaml['spec']
    _=_['metrics']
    _=_[0]
    _=_['resource']
    _=_['target']
    _=_['averageUtilization']
    _=82
    resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']=_
    #resyaml['maxReplicas']=int(resyaml['maxReplicas'])*2
    #resyaml['minReplicas']=int(resyaml['minReplicas'])*2
    resyaml=yaml.safe_dump(resyaml)
    with open("{}.yaml".format(hpa),"wb") as file:
        file.write(resyaml.encode())
    _,res=sp.getstatusoutput("kubectl apply -f {}.yaml -n {}".format(hpa,namespace))
    if _ == 0:
        return 0
    else:
        return 1  
def perMinMon(server,port,svc,namespace,oneDuration,twoDuration,threshold):
    port=findPort(namespace,svc,port)
    start=perf_counter()
    res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
    sleep(oneDuration)
    res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
    if 'k' in res[-1]:
        res=res[:-1]+'000'
    if 'k' in res2[-1]:
        res2=res2[:-1]+'000'
    th=int(res2) - int(res)
    global switch
    if th in range(threshold-3,threshold+3):
        res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
        sleep(twoDuration)
        res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
        th2=int(res2) - int(res) 
        if th2 in range(threshold,100):
            sp.getstatusoutput("kubectl patch deployment {} --patch-file patch.yml".format(deployment))
            
            while True:
                res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
                sleep(1)
                res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
                th3=int(res2) - int(res)
                if th3 in range(normal,threshold-3):
                    #"backtoNormal"
                    break
                
