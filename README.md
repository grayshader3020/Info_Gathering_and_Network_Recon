# Info_Gathering_and_Network_Recon 
Info_Gathering_and_Network_Recon Suite: Comprehensive framework for penetration testing, Active and passive information gathering and  for conducting network reconnaissance.

# Info_Gathering_and_Network_Recon Suite:
This suite is poweerful framework which consists of  different functionalities like Information Gathering using whois,DNS lookup,geo-location search ,network sniffing using scapy,network scanning,simple to advance port scanners using Multithreading and scapy,banner grabbing .this framework is designed to help automate the network recon activities it also has facility to store and write obtained output in a file.

## Features 
 The descriptions of scripts that are used in this framework are as follows 

- INFORMATION GATHERING:
      This is basically a footprinter.this script can be used for active as well as passive recon.This       script  has three functionalities those are
    1. whois : now this section takes domain and with use of socket programming requests the whois database                       and  provides the result
  
    2. dnslookup: this section takes the domain and scans it with dns.resolver and provides results
  
    3. geo-location: the script also makes a request to web for geolocation info.
                      lastly the script  also stores output to a file as per request.


- NETWORK SNIFFER:
    This is a general network snniffer which when provided with interface sniffes in promiscuous mode.


    
- NETWORK SCANNER:
    This part scans the whole network for online clients using scapy it sends arp requests through out the network and waits for response this script also makes ICMP requests in broadcast mode



- SIMPLE PORT SCANNING:
     Simple port scanner scans for open ports in sequential manner by using socket connections.



- ADVANCED PORT SCANNING USING MULTITHREADING:
    This port scanner uses queue data structure and concept of concurrency in multithreading.It is fast and
  also provies banner which is obtained 

- ADVANCED PORT SCANNING USING SCAPY
    Scapy is very powerful tool incase using this in script is makes this framework much powerful.


## Requirements
- Python 3
- pip package manager
- Additional Python packages:
  - requests
  - queue
  - threading
  - socket
  - sys
  - whois
  - dns.resolver
  - scapy.all
  - subprocess
  - argparse
  - colorama
  - scapy.layers
  - signal
  - ipaddress
  - time


## Installation

Clone the repository:

   git clone https://github.com/grayshader3020/Info_Gathering_and_Network_Recon
   
   cd Info_Gathering_and_Network_Recon

   cd recon
   
   ./requirement.sh
   
   sudo python3 Info_Gathering_and_Network_Recon.py

**Note: This project is in its earlier stages and may contain bugs. 
Please use it with caution and report any issues you encounter on [GitHub](https://github.com/grayshader3020/Info_Gathering_and_Network_Recon/). 
Your feedback and contributions are highly appreciated!**


##Disclaimer:

-This project is provided "as is" without warranty of any kind, either express or implied. The use of this project is at your own risk. The author and contributors will not be held responsible for any 
 damages or liabilities arising from the use or misuse of this project.

-Please note that this project is in its earlier stages and may contain bugs or errors. It is recommended to thoroughly test and review the code before using it in any production environment. 

-Your feedback and contributions are welcome and encouraged. If you encounter any issues or have suggestions for improvement,
 please report them on [GitHub](https://github.com/grayshader3020/Info_Gathering_and_Network_Recon) so that they can be addressed.

-Thank you for your understanding.
