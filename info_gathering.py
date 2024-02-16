import dns.resolver
import requests
import argparse
import socket
from package.self_made_whoistool import whois_lookup

"""
At first we have taken argparse module and created instance of argparse to display commandline arguments
while running the script we have declare two variables here so whenever the user gives --help switch both
the variables are shown i.e the description and usage
After that we have add switches by add_arguement attribute
then we have declared args variable which will get the user input by parsing the arg
then we have created domain and ip variables to store the real values passed through arg parse

"""
argparse = argparse.ArgumentParser(description="This is simple info gathering tool",
                                   usage="python3 info_gathering.py -d DOMAIN ")
argparse.add_argument("-d", "--domain", help="Enter the domain name for footprinting", required=True)
argparse.add_argument("-o", "--output", help="Enter the file to write output to")

args = argparse.parse_args()

# Accessing domain and IP from parsed arguments
domain = args.domain
output = args.output

# who is module
print("[+] Getting whois info..")
try:
    domain = socket.gethostbyname(domain)
except:
    print("[-] Host resolution failed.")
    exit()
whois_result = whois_lookup(domain)
print(whois_result)

# DNS Module
print("[+] Getting DNS info..")
dns_result = ''
# Implementing dns.resolver from dnspython which gives us dns info of various records
try:
    for a in dns.resolver.resolve(domain, 'A'):
        dns_result += "[+] A Record: {}\n".format(a.to_text())
    for ns in dns.resolver.resolve(domain, 'NS'):
        dns_result += "[+] NS Record: {}\n".format(ns.to_text())
    for mx in dns.resolver.resolve(domain, 'MX'):
        dns_result += "[+] MX Record: {}\n".format(mx.to_text())
    for txt in dns.resolver.resolve(domain, 'txt'):
        dns_result += "[+] TXt Record: {}\n".format(txt.to_text())
except:
    pass
print(dns_result)

# Geolocation module
print("[+] Getting Geolocation info..")
geo_result = ''

"""
implementing  requests for web request, creating a web request by concatenating ip to it  the gethostbyname fuction in 
socket library resolves the given domain to ip  
so that it makes requests through ip and returns the location of given ip 
for e.g
https://geolocation-db.com/json/193.68.201.200
output: {"country_code":"BG","country_name":"Bulgaria","city":null,"postal":null,"latitude":42.7,"longitude":23.3333,"IPv4":"193.68.201.200","state":null}
"""
try:
    response = requests.request('GET', 'https://geolocation-db.com/json/' + socket.gethostbyname(domain)).json()
    geo_result += "[+] Country: {}\n".format(response['country_name'])
    geo_result += "[+] Latitude: {}\n".format(response['latitude'])
    geo_result += "[+] Longitude: {}\n".format(response['longitude'])
    geo_result += "[+] City: {}\n".format(response['city'])
    geo_result += "[+] State: {}\n".format(response['state'])
except:
    pass
print(geo_result)

if output:
    with open(output, 'w') as file:
        file.write(whois_result + '\n\n')
        file.write(dns_result + '\n\n')
        file.write(geo_result + '\n\n')


