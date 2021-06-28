import xch, requests
from xch.models.inject.parse_ip import parse_ip
from stopforumspam_api import query

def ip_check_tor_exit(ip):
    tor = requests.get('https://check.torproject.org/exit-addresses', verify=False, timeout=5, stream=True)
    
    tor_lines = ""
    
    for line in tor.iter_lines():
        if line: tor_lines += str(line)
    
    for ip_tor in tor_lines:
        ip_tor = ip_tor.replace("\n","")
        if "ExitAddress" in ip_tor:
            ip_tor = ip_tor.split(" ")[1]
            if ip == ip_tor:
                return "You seem to be using Tor or an open proxy."
    return False
                
def ip_check_forum_spam(ip):
    response = query(ip=ip)
    if response.ip.appears == True:
        return "You seem to be using Tor or a proxy, or your IP is listed for spam."
    return False