"""
code explanation:
we have imported scapy.all as sender-receiver packets (especially of layer2) another import is of scapy.layers where we have defined
layer(l)2  and import ARP as well as ether ,we have imported ethernet because we have to specify the protocol destination as at the
end arp packets travels through layer 1.... here we specify the whole range by taking as argument an address.the inputted address will
be anded with subnet mask of network which will give us network id of network
also we have defined two variables ether and arp in which we store the commands that we will pass to scapy,probe is just declared
as stack.here in scapy if we check ls(ARP) and ls(Ether) we can understand which layer is declared first we will set Ether's
destination field to broadcast address and pass protocol destination is set to network range.
"""

import sys
from scapy.all import srp, sr1
from scapy.layers.l2 import ARP, Ether
from scapy.layers.inet import IP, ICMP
import ipaddress
from colorama import init, Fore
import signal
import argparse

# Initialize colorama for colored output
init()

red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
reset = Fore.RESET


# Function to handle Ctrl+C signal
def signal_handler(sig, frame):
    print('\n[!] Ctrl+C pressed. Exiting...')
    sys.exit(0)


# Get target network from command line arguments
argparse = argparse.ArgumentParser(description="This is simple network scanner tool", usage="python3 network_scanner.py -i target_network")
argparse.add_argument("-i", "--target_network", help="Enter the network range or subnet that you want to scan", required=True)

args = argparse.parse_args()
target_network = args.target_network

# Print separator line
print(
    f"{red}-----------------------------------------------------------------------------------------------------------{reset}")

# List to store online clients
online_clients = []

# Create Ethernet and ARP packets for network scanning
ether = Ether(dst='ff:ff:ff:ff:ff:ff')
arp = ARP(pdst=target_network)
probe = ether / arp

# Perform ARP scan
result = srp(probe, timeout=3, verbose=0)

# the response of above send-receive function is like list [answered,unanswered] the probe you sent cannot be
# answered by every host ..... also answered consists of [send,receive] our output is stored in format that it is
# stored at 0th index of result variable (which is answered) an then the 1st index of answered (which is receive)

# Extract answered packets
answered = result[0]

# Iterate through answered packets and store online clients
for sent, received in answered:
    online_clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# Print available hosts
print(f"[+] {blue} Available hosts")
print("IP" + " " * 23 + "MAC")

for client in online_clients:
    print("{}\t\t{}".format(client['ip'], client['mac']))

# Print separator line
print( f"{red}--------------------------------------------------------------------------------------------------{reset}")

# Inform about ICMP scanning
print(f"{blue}[+]Scanning with ICMP..{reset}")
print(f"{red}[-] Warning: Scanning with ICMP is time consuming and intensive process{reset}")

# Generate list of IP addresses in the target network
ip_list = [str(ip) for ip in ipaddress.IPv4Network(target_network, False)]
# ipaddress.IPv4Network(target_network, False) return all the ip in the network and false arguement sets host bits to
# 0 when you provide it

# Set up signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Perform ICMP scan
for ip in ip_list:
    probe = IP(dst=ip) / ICMP()
    result = sr1(probe, timeout=3, verbose=0)
    if result:
        print(f"[+]{blue} {ip} is online{reset}")

# Print separator line
print(f"{red}----------------------------------------------------------------------------------------------------{reset}")

