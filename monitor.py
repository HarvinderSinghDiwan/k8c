from time import sleep
from prometheus_api_client import PrometheusConnect
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