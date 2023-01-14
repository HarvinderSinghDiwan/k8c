import subprocess as sp
from time import sleep
import time
import yaml
import argparse
import sys
"""
Example: python3 tb.py bi productpage productpage-v1 productpage-v1 11 5 2 4 10 700 3
"""
parser = argparse.ArgumentParser(
            description='TrafficBurst monitors the sudden traffic burst on any kubernetes native application by monitoring the request hits.',
            usage='''tb nsname svcname servername portnumber 60 85 2 5 10 1024 3 where 60,85,2,5,10,1024 and 3 are defaultUtilizationValue, 
            scaledUtilizationValue, monitoringInterval , monitoringPeriod,
            coolDownPeriod,thresholdValue and bandwidth respectively.
''')
parser.add_argument('ns', action='store',type=str,nargs=1,help='Namespace : Name of the namespace in which application is hosted ')
parser.add_argument('svc', action='store',type=str,nargs=1,help='Service : Name of the service binded with the application ')
parser.add_argument('hpa', action='store',type=str,nargs=1,help='HorizontalPodAutoscaler : Name of the hpa binded with the application ')
parser.add_argument('deployment', action='store',type=str,nargs=1,help='Deployment : Name of the deployment binded with the application ')
parser.add_argument('duv', action='store',type=int,nargs=1,help='defaultUtilizationValue : The default resource percentage for normal traffic rates')
parser.add_argument('suv', action='store',type=int,nargs=1,help='scaledUtilizationValue : The scaled resource percentage for bursted trafic rates')
parser.add_argument('mi', action='store',type=int,nargs=1,help='monitoringInterval : The time interval between which bursting is to be monitored in sec/min/hour')
parser.add_argument('mp', action='store',type=int,nargs=1,help='monitoringPeriod : The time interval between which the bursting is to be declared in sec/min/hour')
parser.add_argument('cp', action='store',type=int,nargs=1,help='coolDownPeriod : The time interval between scale down should is to be declared in sec/min/hour')
parser.add_argument('tv', action='store',type=int,nargs=1,help='thresholdValue : The threshold value of the traffic per sec/min/hour')
args = vars(parser.parse_args(sys.argv[1:]))
print(args)
for i in args:
  try:
      args.update({i:args[i][0]})
  except:
      pass

#-----------------------------------------------Function that calculates the total rate of traffic-------------------------------------------------------#

def rateTraffic(ns,deployment,svc,port):
    _,res=sp.getstatusoutput("kubectl get pods -n {} -o wide | grep {}".format(ns,deployment))
    _=res.split("\n")
    #print(len(_))
    #s=
    l=[]
    ip=[]
    rate=0
    s=time.perf_counter()
    for i,j in enumerate(_):
        l.append(j.split())
        ip.append(l[i][7])
        res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(ip[i],port,svc,ns))[1].split()[43:44][0]
        if 'k' in res[-1]:
            res=res[:-1]+'000'
        rate+=int(res)
    return rate
def getTraffic(ns,deployment,svc,port):
    _,res=sp.getstatusoutput("kubectl get pods -n {} -o wide | grep {}".format(ns,deployment))
    _=res.split("\n")
    #print(len(_))
    #s=
    l=[]
    for i in _:
        l.append(i.split())
    #print(l)
    ip=[]
    for i in range(len(l)):
        x=l[i][7]
        ip.append(x)
    #print(ip)
    #import time
    rate=0
    for i in ip:
        rate+=int(sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(i,port,svc,ns))[1].split()[43:44][0])
    return rate
#-------------------------------------------------Variables---------------------------------------------------#
host="localhost"
port=15090
ns=args['ns']
svc=args['svc']
hpa=args['hpa']
deployment=args['deployment']
duv=args['duv']
suv=args['suv']
mi=args['mi']
mp=args['mp']
cp=args['cp']
tv=args['tv']
#--------------------------------------------Function that finds port-----------------------------------------#
def findPort(namespace,svc,port):
    _,b=sp.getstatusoutput("kubectl get pods -n {} | grep {}".format(namespace,svc))
    print(len(b.split("\n")))
    a,b=sp.getstatusoutput("kubectl get svc -n {} | grep {}".format(namespace,svc))
    res=b.split()[-2].split(',')
    print(res)
    count=0
    for i in res:
        if i[:len(str(port))] == str(port):
            print("found at {}".format(count))
            break
        count+=1
    return int(res[count].split(":")[1].split("/")[0])

def monitorBurstTraffic(args,port):
    port=findPort(ns,svc,port)
    _,b=sp.getstatusoutput("kubectl get pods -n {} | grep {}".format(ns,svc))
    args.update({'port':port})
    #start=perf_counter()
    while True:
        res=rateTraffic(ns,deployment,svc,port)
        sleep(mi)
        res2=rateTraffic(ns,deployment,svc,port)
        _thresh=int(res2) - int(res)
        print(_thresh)
        global switch
        if _thresh >= int(tv) :
            print("if checked and passsed")
            res=rateTraffic(ns,deployment,svc,port)
            sleep(mp)
            res2=rateTraffic(ns,deployment,svc,port)
            __thresh=int(res2) - int(res) 
            if __thresh >= int(tv):
                print("changed")
                _,res=sp.getstatusoutput("kubectl get hpa {} -o yaml -n {}".format(hpa,ns))
                resyaml=yaml.safe_load(res)
                _=resyaml['spec']
                _=_['metrics']
                _=_[0]
                _=_['resource']
                _=_['target']
                _=_['averageUtilization']
                _=suv
                resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']=_
                resyaml=yaml.safe_dump(resyaml)
                with open("{}.yaml".format(hpa),"wb") as file:
                    file.write(resyaml.encode())
                _,res=sp.getstatusoutput("kubectl apply -f {}.yaml -n {}".format(hpa,ns))
                if _ != 0:
                    raise Exception("Error Error Error")
                while True:
                    res=rateTraffic(ns,deployment,svc,port)
                    sleep(mp)
                    res2=rateTraffic(ns,deployment,svc,port)
                    ___thresh=int(res2) - int(res)
                    if ___thresh < int(tv):
                        res=rateTraffic(ns,deployment,svc,port)
                        sleep(cp)
                        res2=rateTraffic(ns,deployment,svc,port)
                        ____thresh=int(res2) - int(res)
                        if ____thresh < int(tv):
                            _,res=sp.getstatusoutput("kubectl get hpa {} -o yaml -n {}".format(hpa,ns))
                            resyaml=yaml.safe_load(res)
                            _=resyaml['spec']
                            _=_['metrics']
                            _=_[0]
                            _=_['resource']
                            _=_['target']
                            _=_['averageUtilization']
                            _=duv
                            resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']=_
                            #resyaml['maxReplicas']=int(resyaml['maxReplicas'])*2
                            #resyaml['minReplicas']=int(resyaml['minReplicas'])*2
                            resyaml=yaml.safe_dump(resyaml)
                            with open("{}.yaml".format(hpa),"wb") as file:
                                file.write(resyaml.encode())
                            _,res=sp.getstatusoutput("kubectl apply -f {}.yaml -n {}".format(hpa,ns))
                            if _ != 0:
                                raise Exception("Error Error Error")
                            break


monitorBurstTraffic(args,host,port)