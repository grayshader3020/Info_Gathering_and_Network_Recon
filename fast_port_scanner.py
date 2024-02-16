# ADVANCE PORT SCANNER WITH CONCURRENCY AND MULTITHREADING

import socket, sys
import time, queue
import argparse
from colorama import init, Fore
import threading
import signal
import requests


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

# Get target network from command line arguments
argparse = argparse.ArgumentParser(description="This is simple port scanner tool",
                                   usage=" python3 simple_port_scanner.py -t TARGET -s START_PORT -e END_PORT --threads NUMBER_OF_THREADS")
print(f"{red}*{reset}{reset}" * 50)
print(f"{red}Python simple port scanner{reset}{reset}")
print(f"{red}*{reset}{reset}" * 50)
argparse.add_argument("-t", "--target", help="Enter the target ip to scan", required=True)
argparse.add_argument("-s", "--start_port", help="Enter the starting port no. from which you want to scan",
                      required=True, type=int)
argparse.add_argument("-e", "--end_port", help="Enter the ending port no. till which you want to scan", required=True,
                      type=int)
argparse.add_argument("--threads", help="Enter the number of threads you want to run", type=int)
argparse.add_argument("-o", "--output", help="Enter the name and path file  to write output to")
args = argparse.parse_args()
target = args.target
start_port = args.start_port
end_port = args.end_port
thread_no = args.threads
output = args.output

result = "[+] Result:\nPORT\tSTATE\tSERVICE\n"

# Host name resolution
try:
    target = socket.gethostbyname(target)
except:
    print("[-] Host resolution failed.")
    exit()

print(f"{red} [+]Scanning target: {target}{reset}")

"""this is written for receiving connection which has argument the number of bits that has to be obtained generally 
the first bits obtained are banner as exception for port 80, port 80 does not returns any data so we have to handle 
it separately"""


# function to get banner (Receiving Raw Data from an Open Port)
def get_banner(port, s):
    if port == 80:
        response = requests.get('http://' + target)
        return response.headers["Server"]
    try:
        return s.recv(1024).decode()
    except:
        return 'NOT FOUND'


# Method which will run using threads provided below and taking ports from queue
def scan_port(t_no):
    global result
    while not q.empty():
        port = q.get()
        print(f" {blue}Scanning for port {port}...{reset}")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            conn = s.connect_ex((target, port))
            if conn == 0:  # not conn => not 0 which is true so can be written as if not conn also
                banner = get_banner(port, s)  # storing the banner data obtained by get_banner function
                banner = "".join(banner.splitlines())  # to avoid extra \n in output
                result += f"{red}{port}\tOPEN\t{banner}\n{reset}"
            s.close()
        except Exception as e:
            print(f"An error occurred: {e}")
        q.task_done()


# creation of queue
q = queue.Queue()  # This line reassigns q to a new empty queue

# calculating starting_time
start_time: float = time.time()

# adding ports to queue
for j in range(start_port, end_port + 1):
    q.put(j)

# creation of thread  and starting of thread
for i in range(thread_no):
    t = threading.Thread(target=scan_port, args=(i,))
    t.start()

"""
Every program runs main thread first the main thread consists of material that is on zero indent to avoid main thread to run first 
so here our time taken is on 0th indent that means it is on main thread and above method is on another thread so if the main thread
runs first then it will print time taken first and then move to function so to avoid this we use
"""

q.join()

# q.join here specifies that if all the ports are scanned then only you move to lines given below to calculate time
# taken calculating end_time
end_time = time.time()
print(result)
# calculating total time taken
print(f"{green}Time taken: {end_time - start_time}{reset}")

if output:
    with open(output, 'w') as file:
        file.write(f"Port scan result for target {target}\n")
        file.write(result)
    print("[+] Written to file ")
