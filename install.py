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

from config_paths import *

### DIRECTORIES
def create_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

create_dir(main_path)
create_dir(git_path)
create_dir(var_path)
create_dir(var_path+"rc")
create_dir(var_path+"ruby")

### FILES
def create_file(path):
    if not os.path.exists(path):
        f = open(path,'w')
        f.close()

create_file(payloads_path)
create_file(moves_path)


### GIT CLONES
miaomiao_url = "https://github.com/marc0l92/MiaoMiao_project.git"
pupy_url = "https://github.com/n1nj4sec/pupy.git"
rspet_url = "https://github.com/panagiks/RSPET.git"
unicorn_url = "https://github.com/trustedsec/unicorn.git"
#BDF_url = "https://github.com/secretsquirrel/the-backdoor-factory.git"

######
os.chdir(git_path)
######

def git_clone(name, url):
    try:
        print "#########################################"
        print "GIT Cloning: "+name
        comando = "git clone "+url+ " "+name
        print comando
        subprocess.check_output(comando, shell=True)
    except subprocess.CalledProcessError as e:
        print name + " could not be downloaded, error connection? (" + url + ")"
    finally:
        print ""

git_clone("MiaoMiao", miaomiao_url)
git_clone("Pupy", pupy_url)
git_clone("RSPET", rspet_url)
git_clone("Unicorn", unicorn_url)
#git_clone("BDF", BDF_url)


###Installations

def execute_comand(cmd):
    try:
        print cmd
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print "FAIL: "+cmd

def install_pupy():
    os.chdir(pupy_path)
    print "#########################################"
    print "Intalling Pupy"
    comando = "git submodule update --init --depth 1 pupy/payload_templates"
    execute_comand(comando)
    comando = "git submodule init"
    execute_comand(comando)
    comando = "git submodule update"
    execute_comand(comando)
    comando = "pip install -r requirements.txt"
    execute_comand(comando)
    os.chdir(pupy_path+"pupy")
    comando = "git clone https://github.com/alxchk/pupy-binaries.git"
    execute_comand(comando)
    comando = "cp pupy-binaries/* payload_templates/"
    execute_comand(comando)

def install_RSPET():
    os.chdir(rspet_path)
    print "#########################################"
    print "Intalling RSPET"
    comando = "python ./setup.py"
    execute_comand(comando)

install_pupy()
install_RSPET()

os.system("chown www-data -R "+main_path)
