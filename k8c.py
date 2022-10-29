import argparse
import sys
import requests
class k8c(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='K8 client which manipulates your cluster reources',
            usage='''k8c <command> [<args>]

The available k8c commands are:
   create   	    Creates a new deployment
   updatecpu      	Updates the cpu size of any deployment
   updatereplica	Updates the number of replication of any deployment 	
''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print ('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()
    def create(self):
        parser = argparse.ArgumentParser(usage='create [options] deployment-name hostname port',
            description='Creates a new deployment with given requirements on demand')
        parser.add_argument('name', action='store',type=str,nargs=1,help='Name of the deployment to be created')
        parser.add_argument('image', action='store',type=str,nargs=1,help='Container image repository url ')
        parser.add_argument('hostname', action='store',type=str,nargs=1,help='IP or domain name of the remote server')
        parser.add_argument('port', action='store',type=int,nargs=1,default=5000,help='Port number on which the server side application is running')
        parser.add_argument('-cpu','--cpu-size', action='store',type=int,nargs=1,default=80,help='Size of the cpu in a range of 1 to 100')
        parser.add_argument('-min','--minimum', action='store',type=int,nargs=1,default=3,help='Minimum number of the replica to be created')
        parser.add_argument('-max','--maximum', action='store',type=int,nargs=1,default=3,help='Maximum number of replica to be created')
        args = parser.parse_args(sys.argv[2:])
        try:
            res=requests.post('http://{}:{}/create'.format(args.hostname[0],args.port[0]), vars(args))
            print(res.text)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')
    def updatecpu(self):
        parser = argparse.ArgumentParser(usage='updatecpu [options] deployment-name hostname port',
        description='Updates the cpu size of a deployment')
        parser.add_argument('name', action='store',type=str,nargs=1,help='Name of the deployment for which cpu size is to be updated')

        parser.add_argument('hostname', action='store',type=str,nargs=1,help='IP or domain name of the remote server')
        parser.add_argument('port', action='store',type=int,nargs=1,default=5000,help='Port number on which the server side application is running')
        parser.add_argument('-cpu','--cpu-size', action='store',type=int,nargs=1,default=80,help='Size of the cpu in a range of 1 to 100')
        args = parser.parse_args(sys.argv[2:])
        try:
            res=requests.post('http://{}:{}/updatecpu'.format(args.hostname[0],args.port[0]), vars(args))
            print(res.text)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')
    def updatereplica(self):
        parser = argparse.ArgumentParser(usage='updatereplica [options] deployment-name hostname port',
        description='Updates the cpu size of a deployment')
        parser.add_argument('name', action='store',type=str,nargs=1,help='Name of the deployment for which replica size is to be updated')

        parser.add_argument('hostname', action='store',type=str,nargs=1,help='IP or domain name of the remote server')
        parser.add_argument('port', action='store',type=int,nargs=1,default=5000,help='Port number on which the server side application is running')
        replica=parser.add_mutually_exclusive_group()
        replica.add_argument('-min','--minimum', action='store',type=int,nargs=1,default=3,help='Replication number to be updated in the minimum section of the hpa')
        replica.add_argument('-max','--maximum', action='store',type=int,nargs=1,default=3,help='Replication number to be updated in the maximum section of the hpa')
        args = parser.parse_args(sys.argv[2:])
        print(vars(args))
        try:
            res=requests.post('http://{}:{}/updatereplica'.format(args.hostname[0],args.port[0]), vars(args))
            print(res.text)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')

if __name__ == '__main__':
    k8c()