from __future__ import absolute_import

from threading import Thread, Event

from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.util import asbool
##################################
import subprocess as sp
import yaml
from math import ceil
from apscheduler.schedulers.background import BackgroundScheduler
from __future__ import absolute_import
import sys

from apscheduler.executors.base import BaseExecutor, run_job


try:
    import gevent
except ImportError:  # pragma: nocover
    pass

class GeventExecutor(BaseExecutor):
    """
    Runs jobs as greenlets.
    Plugin alias: ``gevent``
    """

    def _do_submit_job(self, job, run_times):
        def callback(greenlet):
            try:
                events = greenlet.get()
            except BaseException:
                self._run_job_error(job.id, *sys.exc_info()[1:])
            else:
                self._run_job_success(job.id, events)

        gevent.spawn(run_job, job, job._jobstore_alias, run_times, self._logger.name).\
            link(callback)
class BackgroundScheduler(BlockingScheduler):
    """
    A scheduler that runs in the background using a separate thread
    (:meth:`~apscheduler.schedulers.base.BaseScheduler.start` will return immediately).
    Extra options:
    ========== =============================================================================
    ``daemon`` Set the ``daemon`` option in the background thread (defaults to ``True``, see
               `the documentation
               <https://docs.python.org/3.4/library/threading.html#thread-objects>`_
               for further details)
    ========== =============================================================================
    """

    _thread = None

    def _configure(self, config):
        self._daemon = asbool(config.pop('daemon', True))
        super(BackgroundScheduler, self)._configure(config)

    def start(self, *args, **kwargs):
        if self._event is None or self._event.is_set():
            self._event = Event()

        BaseScheduler.start(self, *args, **kwargs)
        self._thread = Thread(target=self._main_loop, name='APScheduler')
        self._thread.daemon = self._daemon
        self._thread.start()

    def shutdown(self, *args, **kwargs):
        super(BackgroundScheduler, self).shutdown(*args, **kwargs)
        self._thread.join()
        del self.
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



