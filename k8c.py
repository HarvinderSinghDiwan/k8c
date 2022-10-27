import argparse
import sys
from turtle import clear
import requests
import json
class k8c(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Pretends to be git',
            usage='''k8c <command> [<args>]

The available k8c commands are:
   createNewDep   	Creates a new deployment
   updatePodCpu      	Updates the cpu size of a deployment
   updatePodReplica	Updates the number of replication of a deployment 	
''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print ('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()
    def createNewDep(self):
        parser = argparse.ArgumentParser(usage='createNewDep [options] DeploymentName Hostname Port',
            description='Creates a new deployment with given requirements on demand')
        parser.add_argument('name', action='store',type=str,nargs=1,help='Name of the deployment to be created')
        parser.add_argument('image', action='store',type=str,nargs=1,help='Container image repository url ')
        parser.add_argument('hostname', action='store',type=str,nargs=1,help='IP or domain name of the remote server')
        parser.add_argument('port', action='store',type=int,nargs=1,default=5000,help='Port number on which the server side application is running')
        parser.add_argument('-cpu','--cpu-size', action='store',type=int,nargs=1,help='Size of the cpu in a range of 1 to 100')
        parser.add_argument('-min','--minimum', action='store',type=int,nargs=1,help='Minimum number of the replica to be created')
        parser.add_argument('-max','--maximum', action='store',type=int,nargs=1,help='Maximum number of replica to be created')
        args = parser.parse_args(sys.argv[2:])
        print(vars(args))
        try:
            res=requests.post('http://{}:{}'.format(args.hostname[0],args.port[0]), args)
            print(res)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')


    def updatePodCpu(self):
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('repository')
        args = parser.parse_args(sys.argv[2:])
        print ('Running git fetch, repository=%s %args.repository')
    def updatePodReplicas(self):
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('repository')
        args = parser.parse_args(sys.argv[2:])
        print ('Running git fetch, repository=%s %args.repository')

if __name__ == '__main__':
    k8c()