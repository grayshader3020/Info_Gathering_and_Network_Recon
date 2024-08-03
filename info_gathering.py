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
print("[+]Getting whois info... ")
#using whois  website to scrap info
	
whois_result= whois_lookup(domain)

if whois_result:
	print(whois_result)
else:
	print("WHOIS lookup failed")

# DNS Module
print("[+]Getting DNS info... ")

dns_result = ''
try:
	for a in dns.resolver.resolve(domain,'A'):
		dns_result += "[+] A record: {}\n".format(a.to_text())
except Exception as e:
	print(f"[-]Error fetching A record:{e}\n")

try:
	for ns in dns.resolver.resolve(domain,'NS'):
		dns_result += "[+] NS record: {}\n".format(ns.to_text())
except Exception as e:
	print(f"[-]Error fetching NS record:{e}\n")

try: 
	for mx in dns.resolver.resolve(domain,'MX'):
		dns_result +="[+] MX record: {}\n".format(mx.to_text())
except Exception as e:
	print(f"[-]Error fetching MX record:{e}\n")

try:
	for txt in dns.resolver.resolve(domain,'TXT'):
		dns_result +="[+] TXT record: {}\n".format(txt.to_text())
except Exception as e:
	print(f"[-]Error fetching TXT record:{e}\n")

except Exception as e:
	print(e)

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


