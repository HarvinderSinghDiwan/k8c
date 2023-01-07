import subprocess as sp
from time import sleep
from time import perf_counter
import yaml


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
deployment="""apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "8"
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{"deployment.kubernetes.io/revision":"4"},"creationTimestamp":"2023-01-02T06:53:51Z","generation":8,"labels":{"app":"productpage","version":"v1"},"name":"productpage-v1","namespace":"bi","resourceVersion":"109052","uid":"b7f189a4-601c-4bd6-9bdf-694c952c1646"},"spec":{"progressDeadlineSeconds":600,"replicas":10,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"productpage","version":"v1"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"productpage","version":"v1"}},"spec":{"containers":[{"image":"docker.io/istio/examples-bookinfo-productpage-v1:1.17.0","imagePullPolicy":"IfNotPresent","name":"productpage","ports":[{"containerPort":9080,"protocol":"TCP"}],"resources":{"limits":{"cpu":"1000m","memory":"900Mi"},"requests":{"cpu":"500m","memory":"400Mi"}},"securityContext":{"runAsUser":1000},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","volumeMounts":[{"mountPath":"/tmp","name":"tmp"}]}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"serviceAccount":"bookinfo-productpage","serviceAccountName":"bookinfo-productpage","terminationGracePeriodSeconds":30,"volumes":[{"emptyDir":{},"name":"tmp"}]}}},"status":{"availableReplicas":10,"conditions":[{"lastTransitionTime":"2023-01-02T06:53:51Z","lastUpdateTime":"2023-01-03T20:32:13Z","message":"ReplicaSet \"productpage-v1-7558684fdb\" has successfully progressed.","reason":"NewReplicaSetAvailable","status":"True","type":"Progressing"},{"lastTransitionTime":"2023-01-04T20:43:24Z","lastUpdateTime":"2023-01-04T20:43:24Z","message":"Deployment has minimum availability.","reason":"MinimumReplicasAvailable","status":"True","type":"Available"}],"observedGeneration":8,"readyReplicas":10,"replicas":10,"updatedReplicas":10}}
  creationTimestamp: "2023-01-02T06:53:51Z"
  generation: 33
  labels:
    app: productpage
    version: v1
  name: productpage-v1
  namespace: bi
  resourceVersion: "147145"
  uid: b7f189a4-601c-4bd6-9bdf-694c952c1646
spec:
  progressDeadlineSeconds: 600
  replicas: 3
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: productpage
      version: v1
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: productpage
        version: v1
    spec:
      containers:
      - image: docker.io/istio/examples-bookinfo-productpage-v1:1.17.0
        imagePullPolicy: IfNotPresent
        name: productpage
        ports:
        - containerPort: 9080
          protocol: TCP
        resources:
          limits:
            cpu: "1"
            memory: 1000Mi
          requests:
            cpu: 500m
            memory: 500Mi
        securityContext:
          runAsUser: 1000
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /tmp
          name: tmp
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: bookinfo-productpage
      serviceAccountName: bookinfo-productpage
      terminationGracePeriodSeconds: 30
      volumes:
      - emptyDir: {}
        name: tmp
status:
  availableReplicas: 3
  conditions:
  - lastTransitionTime: "2023-01-05T19:44:09Z"
    lastUpdateTime: "2023-01-06T09:35:15Z"
    message: ReplicaSet "productpage-v1-7bd86b7579" has successfully progressed.
    reason: NewReplicaSetAvailable
    status: "True"
    type: Progressing
  - lastTransitionTime: "2023-01-07T15:19:49Z"
    lastUpdateTime: "2023-01-07T15:19:49Z"
    message: Deployment has minimum availability.
    reason: MinimumReplicasAvailable
    status: "True"
    type: Available
  observedGeneration: 33
  readyReplicas: 3
  replicas: 3
  updatedReplicas: 3"""
def validation(namespace,svc,port):
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
def modValidation(hpa,namespace):
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
def monitorBurstTraffic(server,port,svc,namespace,monitoringInterval,monitoringPeriod,coolDownPeriod,thresholdValue,bandwidth,scaledUtilizationValue,defaultUtilizationValue):
    port=findPort(namespace,svc,port)
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
    port=res[count].split(":")[1].split("/")[0]
    #start=perf_counter()
    while True:
        res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
        sleep(monitoringInterval)
        res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
        if 'k' in res[-1]:
            res=res[:-1]+'000'
        if 'k' in res2[-1]:
            res2=res2[:-1]+'000'
        _thresh=int(res2) - int(res)
        global switch
        if _thresh in range(thresholdValue-bandwidth,thresholdValue+bandwidth):
            res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
            sleep(monitoringPeriod)
            res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
            __thresh=int(res2) - int(res) 
            if __thresh in range(thresholdValue,100):
                _,res=sp.getstatusoutput("kubectl get hpa {} -o yaml -n {}".format(hpa,namespace))
                resyaml=yaml.safe_load(res)
                _=resyaml['spec']
                _=_['metrics']
                _=_[0]
                _=_['resource']
                _=_['target']
                _=_['averageUtilization']
                _=scaledUtilizationValue
                resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']=_
                #resyaml['maxReplicas']=int(resyaml['maxReplicas'])*2
                #resyaml['minReplicas']=int(resyaml['minReplicas'])*2
                resyaml=yaml.safe_dump(resyaml)
                with open("{}.yaml".format(hpa),"wb") as file:
                    file.write(resyaml.encode())
                _,res=sp.getstatusoutput("kubectl apply -f {}.yaml -n {}".format(hpa,namespace))
                if _ != 0:
                    raise Exception("Error Error Error")
                while True:
                    res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
                    sleep(monitoringPeriod)
                    res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
                    ___thresh=int(res2) - int(res)
                    if ___thresh in range(0,thresholdValue-bandwidth):
                        res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
                        sleep(coolDownPeriod)
                        res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(server,port,svc,namespace))[1].split()[43:44][0]
                        ____thresh=int(res2) - int(res)
                        if ____thresh in range(0,thresholdValue-bandwidth):
                            _,res=sp.getstatusoutput("kubectl get hpa {} -o yaml -n {}".format(hpa,namespace))
                            resyaml=yaml.safe_load(res)
                            _=resyaml['spec']
                            _=_['metrics']
                            _=_[0]
                            _=_['resource']
                            _=_['target']
                            _=_['averageUtilization']
                            _=defaultUtilizationValue
                            resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']=_
                            #resyaml['maxReplicas']=int(resyaml['maxReplicas'])*2
                            #resyaml['minReplicas']=int(resyaml['minReplicas'])*2
                            resyaml=yaml.safe_dump(resyaml)
                            with open("{}.yaml".format(hpa),"wb") as file:
                                file.write(resyaml.encode())
                            _,res=sp.getstatusoutput("kubectl apply -f {}.yaml -n {}".format(hpa,namespace))
                            if _ != 0:
                                raise Exception("Error Error Error")
                            break    

if __name__ == "main":
    server="localhost"
    port=9080
    svc="productpage"
    namespace="bi"
    monitoringInterval=2
    monitoringPeriod=4
    coolDownPeriod=10
    thresholdValue=108
    bandwidth=3
    defaultUtilizationValue=60
    scaledUtilizationValue=80

    monitorBurstTraffic(server,port,svc,namespace,monitoringInterval,monitoringPeriod,coolDownPeriod,thresholdValue,bandwidth,scaledUtilizationValue,defaultUtilizationValue)

                
