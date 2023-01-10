import subprocess as sp
from time import sleep
import yaml
import argparse
import sys
"""
Example: python3 tb.py bi productpage productpage-v1 productpage-v1 11 5 2 4 10 20 3
"""
parser = argparse.ArgumentParser(
            description='TrafficBurst monitors the sudden traffic burst on any kubernetes native application by monitoring the request hits.',
            usage='''tb nsname svcname servername portnumber 60 85 2 5 10 1024 3 where 60,85,2,5,10,1024 and 3 are defaultUtilizationValue, 
            scaledUtilizationValue, monitoringInterval , monitoringPeriod,
            coolDownPeriod,thresholdValue and bandwidth respectively.
''')
host="localhost"
port=15090
parser.add_argument('ns', action='store',type=str,nargs=1,help='Namespace : Name of the namespace in which application is hosted ')
parser.add_argument('svc', action='store',type=str,nargs=1,help='Service : Name of the service binded with the application ')
parser.add_argument('hpa', action='store',type=str,nargs=1,help='HorizontalPodAutoscaler : Name of the hpa binded with the application ')
parser.add_argument('deployment', action='store',type=str,nargs=1,help='Deployment : Name of the deployment binded with the application ')
#parser.add_argument('host', action='store',type=str,nargs=1,help='URL or Domain of the server on which the application is hosted ')
#parser.add_argument('port', action='store',type=int,nargs=1,help='Port number on which the sidecar is running and serving the metrics')
parser.add_argument('duv', action='store',type=int,nargs=1,help='defaultUtilizationValue : The default resource percentage for normal traffic rates')
parser.add_argument('suv', action='store',type=int,nargs=1,help='scaledUtilizationValue : The scaled resource percentage for bursted trafic rates')
parser.add_argument('mi', action='store',type=int,nargs=1,help='monitoringInterval : The time interval between which bursting is to be monitored in sec/min/hour')
parser.add_argument('mp', action='store',type=int,nargs=1,help='monitoringPeriod : The time interval between which the bursting is to be declared in sec/min/hour')
parser.add_argument('cp', action='store',type=int,nargs=1,help='coolDownPeriod : The time interval between scale down should is to be declared in sec/min/hour')
parser.add_argument('tv', action='store',type=int,nargs=1,help='thresholdValue : The threshold value of the traffic per sec/min/hour')
parser.add_argument('bd', action='store',type=int,nargs=1,help='bandwidth : The min and max range near the threshold value')
args = vars(parser.parse_args(sys.argv[1:]))
print(args)
for i in args:
  try:
      args.update({i:args[i][0]})
  except:
      pass
#for i in range(len(args)):
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

 
def monitorBurstTraffic(args,host,port):
    port=findPort(args['ns'],args['svc'],port)
    _,b=sp.getstatusoutput("kubectl get pods -n {} | grep {}".format(args['ns'],args['svc']))
    print(len(b.split("\n")))
    """a,b=sp.getstatusoutput("kubectl get svc -n {} | grep {}".format(args['ns'],args['svc']))
    res=b.split()[-2].split(',')
    count=0
    for i in res:
        if i[:len(port)] == port:
            print("found at {}".format(count))
            break
        count+=1
    port=res[count].split(":")[1].split("/")[0]
    """
    print(port)
    args.update({'port':port})
    #start=perf_counter()
    while True:
        print(sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(host,port,args['svc'],args['ns'])))
        res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(host,port,args['svc'],args['ns']))[1].split()[43:44][0]
        print(res)
        sleep(args['mi'])
        print("ee")
        res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(host,port,args['svc'],args['ns']))[1].split()[43:44][0]
        print(res2)
        if 'k' in res[-1]:
            res=res[:-1]+'000'
        if 'k' in res2[-1]:
            res2=res2[:-1]+'000'
        _thresh=int(res2) - int(res)
        global switch
        if _thresh in range(int(args['tv'])-int(args['bd']),int(args['tv'])+int(args['bd'])):
            res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(host,port,args['svc'],args['ns']))[1].split()[43:44][0]
            sleep(args['mp'])
            res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(host,port,args['svc'],args['ns']))[1].split()[43:44][0]
            if 'k' in res[-1]:
                res=res[:-1]+'000'
            if 'k' in res2[-1]:
                res2=res2[:-1]+'000'
            __thresh=int(res2) - int(res) 
            if __thresh in range(int(args['tv'])+int(args['bd']),100):
                _,res=sp.getstatusoutput("kubectl get hpa {} -o yaml -n {}".format(args['hpa'],args['ns']))
                resyaml=yaml.safe_load(res)
                _=resyaml['spec']
                _=_['metrics']
                _=_[0]
                _=_['resource']
                _=_['target']
                _=_['averageUtilization']
                _=args['suv']
                resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']=_
                #resyaml['maxReplicas']=int(resyaml['maxReplicas'])*2
                #resyaml['minReplicas']=int(resyaml['minReplicas'])*2
                resyaml=yaml.safe_dump(resyaml)
                with open("{}.yaml".format(args['hpa']),"wb") as file:
                    file.write(resyaml.encode())
                _,res=sp.getstatusoutput("kubectl apply -f {}.yaml -n {}".format(args['hpa'],args['ns']))
                if _ != 0:
                    raise Exception("Error Error Error")
                while True:
                    res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(host,port,args['svc'],args['ns']))[1].split()[43:44][0]
                    sleep(args['mp'])
                    res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(host,port,args['svc'],args['ns']))[1].split()[43:44][0]
                    ___thresh=int(res2) - int(res)
                    if ___thresh in range(0,int(args['tv'])-int(args['bd'])):
                        res=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(host,port,args['svc'],args['ns']))[1].split()[43:44][0]
                        sleep(args['cp'])
                        res2=sp.getstatusoutput("curl {}:{}/stats/prometheus | grep istio_requests_total | grep {}.{}.svc.cluster.local".format(host,port,args['svc'],args['ns']))[1].split()[43:44][0]
                        if 'k' in res[-1]:
                            res=res[:-1]+'000'
                        if 'k' in res2[-1]:
                            res2=res2[:-1]+'000'
                        ____thresh=int(res2) - int(res)
                        if ____thresh in range(0,int(args['tv'])-int(args['bd'])):
                            _,res=sp.getstatusoutput("kubectl get hpa {} -o yaml -n {}".format(args['hpa'],args['ns']))
                            resyaml=yaml.safe_load(res)
                            _=resyaml['spec']
                            _=_['metrics']
                            _=_[0]
                            _=_['resource']
                            _=_['target']
                            _=_['averageUtilization']
                            _=args['duv']
                            resyaml['spec']['metrics'][0]['resource']['target']['averageUtilization']=_
                            #resyaml['maxReplicas']=int(resyaml['maxReplicas'])*2
                            #resyaml['minReplicas']=int(resyaml['minReplicas'])*2
                            resyaml=yaml.safe_dump(resyaml)
                            with open("{}.yaml".format(args['hpa']),"wb") as file:
                                file.write(resyaml.encode())
                            _,res=sp.getstatusoutput("kubectl apply -f {}.yaml -n {}".format(args['hpa'],args['ns']))
                            if _ != 0:
                                raise Exception("Error Error Error")
                            break   
monitorBurstTraffic(args,host,port)