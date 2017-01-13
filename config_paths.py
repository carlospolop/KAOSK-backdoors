import os
import re
import socket
#Folders
main_path = "/var/www/html/back/"
KAOSK_path = os.path.dirname(os.path.abspath(__file__))+"/"
git_path = KAOSK_path + "GIT/"
config_path = KAOSK_path + "config/"
var_path = KAOSK_path + "var/"

#Files
payloads_path = config_path + "payloads.txt"

#Backdoors
miaomiao_path = git_path+"MiaoMiao/"
pupy_path = git_path+"Pupy/"
rspet_path = git_path+"RSPET/"
unicorn_path = git_path+"Unicorn/"









#Functions
def autoLHOST():
    LHOST = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
        if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    return LHOST

def ip_validator(ip):
    if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', ip):
        print "Valid IP: "+ip
        return True
    else:
        print "Invalid IP: "+ip
        return False
