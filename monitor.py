from time import sleep
import subprocess as sp
from time import sleep
from time import perf_counter
start=perf_counter()
res=sp.getstatusoutput("curl localhost:32467/stats/prometheus | grep istio_requests_total | grep productpage.bookinfo.svc.cluster.local")[1].split()[43:44][0]
sleep(1)
res2=sp.getstatusoutput("curl localhost:32467/stats/prometheus | grep istio_requests_total | grep productpage.bookinfo.svc.cluster.local")[1].split()[43:44][0]
print(int(res2) - int(res))
print("time_taken: {}".format(perf_counter()-start))
#print(str(res).split(" "))
def monitor(host,port,n):

    prom = PrometheusConnect(url ='http://'+host+':'+port+'/', disable_ssl=True)
    res1=prom.custom_query(query="""istio_requests_total{destination_service="productpage.bookinfo.svc.cluster.local", destination_app="productpage",app="productpage"}""")[0]['value'][1]
    sleep(n)
    res2=prom.custom_query(query="""istio_requests_total{destination_service="productpage.bookinfo.svc.cluster.local", destination_app="productpage",app="productpage"}""")[0]['value'][1]
    return int(res2)-int(res1)

def main():
    host='ec2-13-232-143-131.ap-south-1.compute.amazonaws.com'
    port='31464'
    n=10
    res= monitor(host,port,n)
    print(res)
    return res

print(main())