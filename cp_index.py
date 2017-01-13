import os
from shutil import copyfile
from config_paths import *

php = "index.php"
main_save_path = main_path

def dir_walk(path):
    directories = []
    for base, dirs, files in os.walk(path):
        for name in dirs:
            directories.append(os.path.join(base,name))
    return directories

dirs = dir_walk(main_save_path)
copyfile(php, main_save_path+php)
for directorio in dirs:
    copyfile(php, directorio+"/"+php)
os.system("chown www-data -R "+main_save_path)
