import shutil
from simple_colors import *
import requests
import json
url="https://localhost:5000/userdata"
columns = shutil.get_terminal_size().columns
print(blue("FAL INTERNATIONAL PROBLEMS AND SOLUTIONS".center(columns),['bold']))
print("\n")
print(blue("Hello Fella!!!! Welcome to K8c's Customer Orchestration Platform. Please answer the below questions to make it work for you".center(columns),'italic'))
print("\n")
_res={}

while True:
    print("Please Pik Your Deployment Target")
    print("S : SMALL \nM : Medium\nL : Large")
    res=input()
    if res.lower() == "s":
        _res.update({"target":"small"})
        break
    elif res.lower() == "m":
        _res.update({"target":"medium"})
        break
    elif res.lower() == "l":
        _res.update({"target":"large"})
        break
    else: print(red("Please enter a valid input"))
print("Do you want us to perform TRAFFIC BURST monitoring for your application? (yes/y or no/n) ") 
res=input()

if res.lower() == "yes" or res.lower() == 'y':
    _res.update({"tb":1})
else:
    _res.update({"tb":0})
print("Do you want us to perform SCHEDULED TRAFFIC monitoring for your application? (yes/y or no/n) ")
res=input()
if res.lower() == "yes" or res.lower() == 'y':
    print("Please enter the start-time of the PEAK HOURS in the format %H:%M:%S")
    while True:
        _h=input("Please describe the starting HOUR in range of 1-24 :  ")
        if _h.isnumeric() and int(_h) in range(1,25):
            break
        else: print(red("Please enter a valid integer value for hour between 1 - 24"))
    while True:
        _m=input("Please describe the starting MINUTES in range of 0-59 :  ")
        if _m.isnumeric() and int(_m) in range(0,60):
            break
        else: print(red("Please enter a valid integer value for minutes between 0 - 59"))
    while True:
        _s=input("Please describe the starting SECONDS in range of 0-59 :  ")
        if _s.isnumeric() and int(_s) in range(0,60):
            break
        else: print(red("Please enter a valid interger value for seconds between 0 - 59"))
    if len(str(_h)) is 1:
        _h="0"+_h
    if len(str(_m)) is 1:
        _m="0"+_m
    if len(str(_s)) is 1:
        _s="0"+_s
    if _m is not 0 and _s is not 0:
        _res.update({"st":{"start-time":str(_h)+":"+str(_m)+":"+str(_s)}})

    elif _m is 0:
        _res.update({"st":{"start-time":str(_h)+":00:"+str(_s)}})

    else: 
        _res.update({"st":{"start-time":str(_h)+":"+str(_m)+":00:"}})
    print(_res)
    print("Please enter the end-time of the PEAK HOURS in the format %H:%M:%S")
    while True:
        _h=input("Please describe the ending HOUR in range of 1-24 :  ")
        if _h.isnumeric() and int(_h) in range(1,25):
            break
        else: print(red("Please enter a valid integer value for hour between 1 - 24"))
    while True:
        _m=input("Please describe the ending MINUTES in range of 0-59 :  ")
        if _m.isnumeric() and int(_m) in range(0,60):
            break
        else: print(red("Please enter a valid integer value for minutes between 0 - 59"))
    while True:
        _s=input("Please describe the ending SECONDS in range of 0-59 :  ")
        if _s.isnumeric() and int(_s) in range(0,60):
            break
        else: print(red("Please enter a valid interger value for seconds between 0 - 59"))
    if len(str(_h)) is 1:
        _h="0"+_h
    if len(str(_m)) is 1:
        _m="0"+_m
    if len(str(_s)) is 1:
        _s="0"+_s
    if int(_m) is not 0 and int(_s) is not 0:
        _res['st'].update({"end-time":str(_h)+":"+str(_m)+":"+str(_s)})
    elif int(_m) is 0:
        _res['st'].update({"end-time":str(_h)+":00:"+str(_s)})
    else:
        _res['st'].update({"end-time":str(str(str(_h)+":"+str(_m)+":00:"))})#["end-time"]=str(_h)+":"+str(_m)+":00:"
        #_res.update({"st":[1,{"end-time":str(_h)+":"+str(_m)+":00:"}]})
    print(_res)
else: _res.update({"st":0})
print(_res)
res=requests.post(url=url,json=json.dumps(_res),verify=False)
print(res.text)