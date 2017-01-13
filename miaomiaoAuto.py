# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
from config_paths import *

main_save_path = main_path+"MiaoMiao/"

def main_directory():
    if os.path.exists(main_save_path):
        shutil.rmtree(main_save_path)
    os.makedirs(main_save_path)


main_directory()

print ""
print "#################################################"
print "MOVING MiaoMiao:"
print "-------------------------------------------------"
print "DEFAULT PORT: 55555"
try:
    os.chdir(git_path)
    comando = "zip -r "+ main_save_path +"miaomiao.zip "+miaomiao_path
    print comando
    subprocess.check_output(comando, shell=True)
except subprocess.CalledProcessError as e:
    print "Couldn't compress and move the folder"
print "_________________________________________________"

os.system("chown www-data -R "+main_save_path)
