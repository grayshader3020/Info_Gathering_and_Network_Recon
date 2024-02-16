#!/bin/bash

# Install required utilities
echo "Installing utilities..."
sudo apt-get update
sudo apt-get install -y python2
sudo apt-get install -y python3
sudo apt-get install -y update
sudo apt-get install -y upgrade 
sudo apt-get install python3-pip


echo "Utility installation completed."

# Install required dependencies
echo "Installing dependencies..."
pip install requests
pip install queue
pip install threading
pip install socket
pip install sys
pip install whois
pip install dns.resolver
pip install scapy.all
pip install subprocess
pip install argparse
pip install colorama
pip install scapy.layers
pip install signal
pip install ipaddress
pip install time
echo "Dependency installation completed."


