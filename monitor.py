import subprocess as sp
from time import sleep
from time import perf_counter
import json
patch="""spec:
    template:
        spec:
            containers:
            - name: patch-demo-ctr-2
              resources:
                limits:
                    cpu: 8m
                    memory: 20Mi
                requests:
                    cpu: 6m
                    memory: 10Mi"""
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
""" docker run --rm  skandyla/wrk -t9 -c100  -d120  -H 'Host: www.bookinfo.co.in' 'http://ec2-13-232-143-131.ap-south-1.compute.amazonaws.com:32052/productpage'
Running 2m test @ http://ec2-13-232-143-131.ap-south-1.compute.amazonaws.com:32052/productpage"""

def monitor():
    start=perf_counter()
    res=sp.getstatusoutput("curl localhost:32467/stats/prometheus | grep istio_requests_total | grep productpage.bookinfo.svc.cluster.local")[1].split()[43:44][0]
    sleep(n)
    res2=sp.getstatusoutput("curl localhost:32467/stats/prometheus | grep istio_requests_total | grep productpage.bookinfo.svc.cluster.local")[1].split()[43:44][0]
    print(res,res2)
    if 'k' in res[-1]:
        res=res[:-1]+'000'
    if 'k' in res2[-1]:
        res2=res2[:-1]+'000'
    return   int(res2) - int(res)
    #return json.dumps({"Requests/second" : "{}".format(int(res2) - int(res)),
    #"time_taken": "{}".format(perf_counter()-start)})


host='ec2-13-232-143-131.ap-south-1.compute.amazonaws.com'
port='32467'
n=59
x= None
while True:
    res= monitor()
    if res >= x :
        sp.getstatusoutput("kubectl patch deployment {} --patch-file patch.yml".format(depname))
    elif res < x:
        sp.getstatusoutput("kubectl patch deployment {} --patch-file patch2.yml".format(depname))