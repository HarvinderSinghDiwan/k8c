#!/c/ProgramData/Anaconda3/python
import argparse
import sys
import os
import requests
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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
        parser = argparse.ArgumentParser(usage='create [options] app-name namespace-name',
        description='Creates a new deployment with given requirements on demand')
        parser.add_argument('app', action='store',type=str,nargs=1,help='Name of the deployment for which replica size is to be updated')
        parser.add_argument('namespace', action='store',type=str,nargs=1,help='Name of the namespace unedr which the deployment is running')
        parser.add_argument('image', action='store',type=str,nargs=1,help="The repository URL from the container's image is to be fetched")
        parser.add_argument('pod-size', action='store',type=str,nargs=1,choices=['small','medium','large'],help='It specifies cpu and ram serources for limits and requests quotas that the pod will be allocated during the creation of the deployment.')
        parser.add_argument('cport', action='store',type=int,nargs=1,default=None,help='The port number of the container to be exposed.')
        parser.add_argument('protocol' ,action='store',type=str,nargs=1,default=None,help='The protocol that the port will be opened on')
        parser.add_argument('-cpu','--cpu-threshold', action='store',default=80,type=int,nargs=1,help='Replication number to be updated in the minimum section of the hpa')
        parser.add_argument('-min','--minimum-replica', action='store',default=3,type=int,nargs=1,help='Replication number to be updated in the minimum section of the hpa')
        parser.add_argument('-max','--maximum-replica', action='store',default=3,type=int,nargs=1,help='Replication number to be updated in the maximum section of the hpa')
        parser.add_argument('-svc','--service-type' action='store',type=str,default='ClusterIP',choices=['ClusterIP','NodePort','LoadBalancer','Headless'],nargs=1,default=None,help='The type of the service that is to be created along with the deployment.')
        
        args = vars(parser.parse_args(sys.argv[2:]))
        if args['cpu_threshold'] is not None and args['cpu_threshold'][0]< 0 :
            logging.error("CPU Threshold percentage must be greater than 0 (Zero). Please correct and try again")
            exit()
        if args['cpu_threshold'] is not None and args['cpu_threshold'][0] > 100:
            logging.error("CPU Threshold percentage must be less than 100 (Hundred). Please correct and try again")
            exit()
        for i in args:
            try:
                args.update({i:args[i][0]})
            except:
                pass
        res=requests.post('https://{}:{}/updatecpu'.format(H,P), args,verify=False)
        print(res.text)
    def updatecpu(self):
        parser = argparse.ArgumentParser(usage='updatecpu [options]  app-name namespace-name',
        description='Updates the cpu size of a deployment')
        parser.add_argument('app', action='store',type=str,nargs=1,help='Name of the deployment for which replica size is to be updated')
        parser.add_argument('namespace', action='store',type=str,nargs=1,help='Name of the namespace unedr which the deployment is running')
        parser.add_argument('-cpu','--cpu-threshold', action='store',type=int,nargs=1,help='Replication number to be updated in the minimum section of the hpa')
        args = vars(parser.parse_args(sys.argv[2:]))
        if args['cpu_threshold'] is not None and args['cpu_threshold'][0]< 0 :
            logging.error("CPU Threshold percentage must be greater than 0 (Zero). Please correct and try again")
            exit()
        if args['cpu_threshold'] is not None and args['cpu_threshold'][0] > 100:
            logging.error("CPU Threshold percentage must be less than 100 (Hundred). Please correct and try again")
            exit()
        for i in args:
            try:
                args.update({i:args[i][0]})
            except:
                pass
        res=requests.post('https://{}:{}/updatecpu'.format(H,P), args,verify=False)
        print(res.text)
    def updatereplica(self):
        parser = argparse.ArgumentParser(usage='updatereplica [options] deployment-name app-name namespace-name',
        description='Updates the cpu size of a deployment')
        parser.add_argument('app', action='store',type=str,nargs=1,help='Name of the deployment for which replica size is to be updated')
        parser.add_argument('namespace', action='store',type=str,nargs=1,help='Name of the namespace unedr which the deployment is running')
        parser.add_argument('-min','--minimum-replica', action='store',type=int,nargs=1,help='Replication number to be updated in the minimum section of the hpa')
        parser.add_argument('-max','--maximum-replica', action='store',type=int,nargs=1,help='Replication number to be updated in the maximum section of the hpa')
        args = vars(parser.parse_args(sys.argv[2:]))
        if args['maximum_replica'] is not None and args['minimum_replica'] is not None and args['minimum_replica'][0] > args['maximum_replica'][0]:
            logging.error("Minimum number of replica must always be less than or equal to Maximum number of replica")
            exit()
        for i in args:
            try:
                args.update({i:args[i][0]})
            except:
                pass
        res=requests.post('https://{}:{}/updatereplica'.format(H,P), args,verify=False)
        print(res.text)
    def updatepsnr(self):
        parser = argparse.ArgumentParser(usage='updatepsnr [options] deployment-name hostname port',
        description='Updates the pod size and replica based on observed requests per sec on the deployment')
        parser.add_argument('name', action='store',type=str,nargs=1,help='Name of the deployment for which replica size is to be updated')
        parser.add_argument('-rps','--requests-per-second',action='store',type=str,nargs=1,help='Requests per second upon which the action is to be taken')
        parser.add_argument('-ps','--pod-size', action='store',type=int,nargs=1,help='Size of pod by which it should be updated')
        parser.add_argument('-min','--minimum', action='store',type=int,nargs=1,help='Replication number to be updated in the minimum section of the hpa')
        parser.add_argument('-max','--maximum', action='store',type=int,nargs=1,help='Replication number to be updated in the maximum section of the hpa')
        args = parser.parse_args(sys.argv[2:])

        try:
            res=requests.post('https://{}:{}/updatepsnr'.format(H,P), vars(args))
            pprint(res.text)
        except:
            print('Oops!!! Something went wrong. Please try again rechecking your imputs.')
    def updatepcpu(self):
        parser = argparse.ArgumentParser(usage='updatepcpu [options] app-name namespace-name',
        description='Updates the pod cpu size based on observed requests per sec on the deployment')
        parser.add_argument('app', action='store',type=str,nargs=1,help='Name of the deployment for which replica size is to be updated')
        parser.add_argument('ns', action='store',type=str,nargs=1,help='Name of the namespace in which the app is running')
        parser.add_argument('-rps','--requests-per-second',action='store',type=int,nargs=1,help='Requests per second upon which the action is to be taken')
        parser.add_argument('-cpu','--cpu-size', action='store',type=int,nargs=1,help='Size of cpu by which it should be updated')
        args = parser.parse_args(sys.argv[2:])
        print(vars(args))
        try:
            res=requests.post('https://{}:{}/updatepcpu'.format(H,P), vars(args))
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
class fantasy:
    def _format_actions_usage(self, actions, groups):
        # find group indices and identify actions in groups
        group_actions = set()
        inserts = {}
        for group in groups:
            if not group._group_actions:
                raise ValueError(f'empty group {group}')

            try:
                start = actions.index(group._group_actions[0])
            except ValueError:
                continue
            else:
                end = start + len(group._group_actions)
                if actions[start:end] == group._group_actions:
                    for action in group._group_actions:
                        group_actions.add(action)
                    if not group.required:
                        if start in inserts:
                            inserts[start] += ' ['
                        else:
                            inserts[start] = '['
                        if end in inserts:
                            inserts[end] += ']'
                        else:
                            inserts[end] = ']'
                    else:
                        if start in inserts:
                            inserts[start] += ' ('
                        else:
                            inserts[start] = '('
                        if end in inserts:
                            inserts[end] += ')'
                        else:
                            inserts[end] = ')'
                    for i in range(start + 1, end):
                        inserts[i] = '|'

        # collect all actions format strings
        parts = []
        for i, action in enumerate(actions):

            # suppressed arguments are marked with None
            # remove | separators for suppressed arguments
            if action.help is SUPPRESS:
                parts.append(None)
                if inserts.get(i) == '|':
                    inserts.pop(i)
                elif inserts.get(i + 1) == '|':
                    inserts.pop(i + 1)

            # produce all arg strings
            elif not action.option_strings:
                default = self._get_default_metavar_for_positional(action)
                part = self._format_args(action, default)

                # if it's in a group, strip the outer []
                if action in group_actions:
                    if part[0] == '[' and part[-1] == ']':
                        part = part[1:-1]

                # add the action string to the list
                parts.append(part)

            # produce the first way to invoke the option in brackets
            else:
                option_string = action.option_strings[0]

                # if the Optional doesn't take a value, format is:
                #    -s or --long
                if action.nargs == 0:
                    part = action.format_usage()

                # if the Optional takes a value, format is:
                #    -s ARGS or --long ARGS
                else:
                    default = self._get_default_metavar_for_optional(action)
                    args_string = self._format_args(action, default)
                    part = '%s %s' % (option_string, args_string)

                # make it look optional if it's not required or in a group
                if not action.required and action not in group_actions:
                    part = '[%s]' % part

                # add the action string to the list
                parts.append(part)

        # insert things at the necessary indices
        for i in sorted(inserts, reverse=True):
            parts[i:i] = [inserts[i]]

        # join all the action items with spaces
        text = ' '.join([item for item in parts if item is not None])

        # clean up separators for mutually exclusive groups
        open = r'[\[(]'
        close = r'[\])]'
        text = _re.sub(r'(%s) ' % open, r'\1', text)
        text = _re.sub(r' (%s)' % close, r'\1', text)
        text = _re.sub(r'%s *%s' % (open, close), r'', text)
        text = _re.sub(r'\(([^|]*)\)', r'\1', text)
        text = text.strip()

        # return the text
        return text

    def _format_text(self, text):
        if '%(prog)' in text:
            text = text % dict(prog=self._prog)
        text_width = max(self._width - self._current_indent, 11)
        indent = ' ' * self._current_indent
        return self._fill_text(text, text_width, indent) + '\n\n'

    def _format_action(self, action):
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2,
                            self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)

        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup

        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            tup = self._current_indent, '', action_width, action_header
            action_header = '%*s%-*s  ' % tup
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup
            indent_first = help_position

        # collect the pieces of the action help
        parts = [action_header]

        # if there was help for the action, add lines of help text
        if action.help and action.help.strip():
            help_text = self._expand_help(action)
            if help_text:
                help_lines = self._split_lines(help_text, help_width)
                parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
                for line in help_lines[1:]:
                    parts.append('%*s%s\n' % (help_position, '', line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith('\n'):
            parts.append('\n')

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)
            
