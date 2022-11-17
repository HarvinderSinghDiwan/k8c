import subprocess as sp
from time import sleep
from time import perf_counter


def monitor(host,port,n):
    start=perf_counter()
    res=sp.getstatusoutput("curl localhost:32467/stats/prometheus | grep istio_requests_total | grep productpage.bookinfo.svc.cluster.local")[1].split()[43:44][0]
    sleep(n)
    res2=sp.getstatusoutput("curl localhost:32467/stats/prometheus | grep istio_requests_total | grep productpage.bookinfo.svc.cluster.local")[1].split()[43:44][0]
    return "Requests/second : {}".format(int(res2) - int(res))+"\n"+"time_taken: {}".format(perf_counter()-start)



host='ec2-13-232-143-131.ap-south-1.compute.amazonaws.com'
port='32467'
n=1
while True:
    res= monitor(host,port,n)
    print(res)