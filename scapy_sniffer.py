from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.http import HTTPRequest, TCP
from colorama import init, Fore
import argparse

init()

red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
yellow = Fore.YELLOW
reset = Fore.RESET


def sniff_packets(iface, output=None):
    if iface:
        if output:
            sniff(prn=process_packet, iface=iface, store=True, offline=output)
        else:
            sniff(prn=process_packet, iface=iface, store=True)
    else:
        if output:
            sniff(prn=process_packet, store=True, offline=output)
        else:
            sniff(prn=process_packet, store=True)


def process_packet(packet):
    output_lines = []  # Accumulate output lines to write to the file

    if packet.haslayer(Ether):
        src_mac = packet[Ether].src
        dst_mac = packet[Ether].dst
        ether_type = packet[Ether].type

        print(f"{blue}[+] Ethernet Frame:")
        print(f"{blue}    |- Source MAC: {src_mac}")
        print(f"{blue}    |- Destination MAC: {dst_mac}")
        print(f"{blue}    |- Ether Type: {hex(ether_type)}{reset}")

        output_lines.append(f"{blue}[+] Ethernet Frame:")
        output_lines.append(f"{blue}    |- Source MAC: {src_mac}")
        output_lines.append(f"{blue}    |- Destination MAC: {dst_mac}")
        output_lines.append(f"{blue}    |- Ether Type: {hex(ether_type)}{reset}")

    if packet.haslayer(TCP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        print(f"{blue}[+]{src_ip} is using port {src_port} to connect to {dst_ip} at port {dst_port}{reset}")
        output_lines.append(f"{blue}[+]{src_ip} is using port {src_port} to connect to {dst_ip} at port {dst_port}{reset}")

    if packet.haslayer(HTTPRequest):
        src_ip = packet[IP].src  # Moved inside the if block
        url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
        method = packet[HTTPRequest].Method.decode()
        print(f"{green}[+]{src_ip} is making a HTTP request to {url} with {method} method{reset}")
        print("[+] HTTP Data")
        print(f"{yellow}{packet[HTTPRequest].show()}{reset}")
        output_lines.append(f"{yellow}{packet[HTTPRequest].show()}{reset}")
        if packet.haslayer(Raw):
            print(f"{red}[+]Useful raw data: {packet.getlayer(Raw).load.decode()}{reset}")
            output_lines.append(f"{red}[+]Useful raw data: {packet.getlayer(Raw).load.decode()}{reset}")

    # Write the accumulated output to the file
    if output:
        with open(output, 'w') as file:
            for line in output_lines:
                file.write(line + '\n')
        print("Packet details written to the output file.")


argparse = argparse.ArgumentParser(description="This is simple packet sniffer tool", usage="python3 scapy_sniffer.py -i interface ")
argparse.add_argument("-i", "--interface", help="Enter the interface through which you want to sniff", required=True)
argparse.add_argument("-o", "--output", help="Enter the file to write output to")
args = argparse.parse_args()
iface = args.interface
output = args.output
sniff_packets(iface)
