import socket, sys
import time
import argparse
import signal
from colorama import init, Fore


# Function to handle Ctrl+C signal
def signal_handler(sig, frame):
    print(f'\n{red}[!] Ctrl+C pressed. Exiting...{reset}')
    sys.exit(0)


# Set up signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Initialize colorama for colored output
init()

red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
reset = Fore.RESET

"""
if you want sys library code for command line input 
 target = sys.argv[1]

start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

 if not target or not str(start_port) or not end_port:
     print(usage)
      exit()
target = socket.gethostbyname(target)
"""
# Get target network from command line arguments
argparse = argparse.ArgumentParser(description="This is simple port scanner tool",
                                   usage=" python3 simple_port_scanner.py -t TARGET -s START_PORT -e END_PORT")
print(f"{red}*{reset}{reset}" * 20)
print(f"{red}Python simple port scanner{reset}{reset}")
print(f"{red}*{reset}{reset}" * 20)
argparse.add_argument("-t", "--target", help="Enter the target ip to scan", required=True)
argparse.add_argument("-s", "--start_port", help="Enter the starting port no. from which you want to scan",
                      required=True, type=int)
argparse.add_argument("-e", "--end_port", help="Enter the ending port no. till which you want to scan", required=True,
                      type=int)
args = argparse.parse_args()
target = args.target
start_port = args.start_port
end_port = args.end_port
target = socket.gethostbyname(target)

start_time: float = time.time()

for port in range(start_port, end_port + 1):
    print(f" {blue}Scanning for port {port}...{reset}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    conn = s.connect_ex((target, port))
    # s.connect_ex does not creates any exception if connection is successful it returns 0 and i
    # f it's not successful it returns non-zero number so if conn will be zero connection is successful
    if conn == 0:  # not conn => not 0 which is true
        print(f"{red}[+]Port {port} is open{reset}")
    s.close()

end_time = time.time()
print(f"{green}Time taken: {end_time - start_time}{reset}")
