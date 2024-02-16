"""
we will be using socket library here as it gives access to low level functionality that uses core networking
services that we need our python script to do
"""
import socket


def whois_lookup(domain1: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("whois.iana.org", 43))
    s.send(f"{domain1}\r\n".encode())
    response = s.recv(4096).decode()
    s.close()
    return response






