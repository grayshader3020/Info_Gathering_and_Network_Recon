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

print(dns_result)
# Geolocation module

print("geo location module")

geo_result = ''

# Implementing socket to get ip from domain
try:
	for_ip = socket.gethostbyname(domain)
except socket.gaierror as e:
	print(f"Error resolving domoin {domain}: {e}")
	exit(1)

try:
    # Correct API endpoint
    response = requests.get(f"https://ipinfo.io/{for_ip}/json").json()
  

    #print all key-value pairs  in the response
    geo_result += json.dumps(response, indent=4)

except requests.exceptions.RequestException as e:
	print(f"Error fetching geolocation data: {e}")

print(geo_result)

if output:
    with open(output, 'w') as file:
        file.write(whois_result + '\n\n')
        file.write(dns_result + '\n\n')
        file.write(geo_result + '\n\n')


