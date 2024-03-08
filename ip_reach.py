import sys
import subprocess

# Checking IP Reachability
def ip_reach(list):

    for ip in list:
        ip = ip.rstrip('\n')
        
        # For Windows
        ping_reply = subprocess.call ('ping %s /n 2' %(ip), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # For Mac OS or Linux 
        #ping_reply = subprocess.call("ping %s -c 2" % ip)

        # Extended version for Mac OS or Linux
        #ping_reply = subprocess.call("ping %s -c 2" % ip, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL shell=True)

        if ping_reply == 0:
            print("\n{} is reachable \n".format(ip))
            continue

        else:
            print("\n {} not reachable. Check connectivity and try again".format(ip))
            sys.exit