# -*- coding: utf-8 -*-
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


### FILES
def create_file(path):
    if not os.path.exists(path):
        f = open(path,'r')
        f.close()

create_file(payloads_path)


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

