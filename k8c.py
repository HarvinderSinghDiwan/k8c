#!/c/ProgramData/Anaconda3/python
import argparse
import sys
import os
import requests
def config():
    if ".k8config" in os.listdir():
        isfound=[False,False]
        with open(".k8config","rb") as file:
            metadata=[i.decode().strip() for i in file]
            for i in metadata:
                data=i.split('=')
                if data[0]=='hostname':
                    isfound[0]=True
                elif data[0]=='port':
                    isfound[1]=True
       
                    
            print( metadata[0])
    return False
class k8c(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='K8 client which manipulates your cluster reources',
            usage='''k8c <command> [<args>]

The available k8c commands are:
   create               Creates a new deployment
   updatecpu            Updates the cpu size of any deployment
   updatereplica        Updates the number of replication of any deployment 
   updatepcpu           Updates the pod cpu based on requests per second traffic
   updatepsnr	        Updates the pos size and pod replica based on requests per seconf traffic
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

        parser.add_argument('-cpu','--cpu-size', action='store',type=int,nargs=1,default=80,help='Size of the cpu in a range of 1 to 100')
        parser.add_argument('-min','--minimum', action='store',type=int,nargs=1,default=3,help='Minimum number of the replica to be created')
        parser.add_argument('-max','--maximum', action='store',type=int,nargs=1,default=3,help='Maximum number of replica to be created')
        args = parser.parse_args(sys.argv[2:])
        try:
            res=requests.post('http://{}:{}/create'.format(H,P), vars(args))
            pprint(res.text)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')
    def updatecpu(self):
        parser = argparse.ArgumentParser(usage='updatecpu [options] deployment-name hostname port',
        description='Updates the cpu size of a deployment')
        parser.add_argument('name', action='store',type=str,nargs=1,help='Name of the deployment for which cpu size is to be updated')

        parser.add_argument('-cpu','--cpu-size', action='store',type=int,nargs=1,default=80,help='Size of the cpu in a range of 1 to 100')
        args = parser.parse_args(sys.argv[2:])
        try:
            res=requests.post('http://{}:{}/updatecpu'.format(H,P), vars(args))
            pprint(res.text)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')
    def updatereplica(self):
        parser = argparse.ArgumentParser(usage='updatereplica [options] deployment-name hostname port',
        description='Updates the cpu size of a deployment')
        parser.add_argument('name', action='store',type=str,nargs=1,help='Name of the deployment for which replica size is to be updated')


        replica=parser.add_mutually_exclusive_group()
        replica.add_argument('-min','--minimum', action='store',type=int,nargs=1,help='Replication number to be updated in the minimum section of the hpa')
        replica.add_argument('-max','--maximum', action='store',type=int,nargs=1,help='Replication number to be updated in the maximum section of the hpa')
        args = parser.parse_args(sys.argv[2:])
        print(vars(args))
        try:
            res=requests.post('http://{}:{}/updatereplica'.format(H,P), vars(args))
            pprint(res.text)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')
    def updatepsnr(self):
        parser = argparse.ArgumentParser(usage='updatepsnr [options] deployment-name hostname port',
        description='Updates the pod size and replica based on observed requests per sec on the deployment')
        parser.add_argument('name', action='store',type=str,nargs=1,help='Name of the deployment for which replica size is to be updated')

        parser.add_argument('-rps','--requests-per-second',action='store',type=int,nargs=1,help='Requests per second upon which the action is to be taken')
        parser.add_argument('-ps','--pod-size', action='store',type=int,nargs=1,help='Size of pod by which it should be updated')
        parser.add_argument('-min','--minimum', action='store',type=int,nargs=1,help='Replication number to be updated in the minimum section of the hpa')
        parser.add_argument('-max','--maximum', action='store',type=int,nargs=1,help='Replication number to be updated in the maximum section of the hpa')
        args = parser.parse_args(sys.argv[2:])
        print(vars(args))
        try:
            res=requests.post('http://{}:{}/updatepsnr'.format(H,P), vars(args))
            pprint(res.text)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')
    def updatepcpu(self):
        parser = argparse.ArgumentParser(usage='updatepcpu [options] deployment-name hostname port',
        description='Updates the pod cpu size based on observed requests per sec on the deployment')
        parser.add_argument('name', action='store',type=str,nargs=1,help='Name of the deployment for which replica size is to be updated')

        parser.add_argument('-rps','--requests-per-second',action='store',type=int,nargs=1,help='Requests per second upon which the action is to be taken')
        parser.add_argument('-cpu','--cpu-size', action='store',type=int,nargs=1,help='Size of cpu by which it should be updated')
        args = parser.parse_args(sys.argv[2:])
        print(vars(args))
        try:
            res=requests.post('http://{}:{}/updatepcpu'.format(H,P), vars(args))
            pprint(res.text)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')


def config():
    global H
    global P
    isfound=[False,False]
    if ".k8config" in os.listdir():
        if os.stat("./.k8config").st_size == 0:
            return '''The Configuration file is Empty.\nPlease configure you application first with HOSTNAME and PORT variable refering to hostname and portnuimber of the server.'''
        else:
            with open(".k8config","rb") as file:
                    metadata=[i.decode().strip() for i in file]
                    for i in metadata:
                        data=i.split('=')
                        if data[0].upper()=='HOSTNAME':
                            isfound[0]=True
                            H=data[1]
                        elif data[0].upper()=='PORT':
                            isfound[1]=True
                            P=data[1]
                        else:
                            return '''Alert!!!!!! Configuration corrupted.\nThe configuration file does not contain HOSTNAME and PORT variable.\nPlease configure you Application.'''

    if isfound[0]==True and isfound[1]==True:
        return True
    else:
        return '''The configuration file does not contain HOSTNAME and PORT variable.\nPlease configure you Application.'''


if __name__ == '__main__':

    isConfigured=config()
    if isConfigured is True:
        k8c()
    else:
        global H
        global P
        print("\n"*2)
        print(isConfigured)
        print("\n")
        res=input("Do You Want To Configure Now? Press 'y' or 'yes' to continue else press 'n'or 'no' to EXIT :   ")
        if res=='y' or res=='yes':
            H=HOSTNAME=input("Please enter server's ip or fqdn . Eg: 13.26.128.30 or api.server.example.com :   ")
            P=PORT=input("Please enter the port number of the server on the the receiver program is running. Eg: 8080 :   ")
            with open(".k8config","wb") as file:
                file.write(str('HOSTNAME='+HOSTNAME+"\n"+"PORT="+PORT).encode())
            print("Configuration successful. Please proceed with ahead.")
            k8c()
        else:
            exit('Thanks .......... But unless you configure, i wil not allow to to use me. Either configure using the client program or manually make entries of HOSTNAME and PORT variable in the .k8config file in the current directory.')


