"""
scapy port scanner differs from fast port scanner with changing only socket programming code which creates
connection
"""
import argparse
import queue
import signal

from colorama import init, Fore
from scapy.all import *
from scapy.layers.inet import IP, TCP


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

result = "[+] Result:\nPORT\tSTATE\t\n"

# Host name resolution
try:
    target = socket.gethostbyname(target)
except:
    print("[-] Host resolution failed.")
    exit()

print(f"{red} [+]Scanning target: {target}{reset}")


# Method which will run using threads provided below and taking ports from queue
def scan_port(t_no):
    global result
    while not q.empty():
        port = q.get()
        print(f" {blue}Scanning for port {port}...{reset}")
        conf.verb = 0  # conf.verb is set to 0 to exclude all the unwanted content
        try:
            """
            here source port consists of randshort() ,here if we are performing full scan server sometime whenever there
            is same port number blocks the ip or port so to overcome this scapy's volatile package consist of Randshort function
             which generates random numbers from 0-65535
             the keyword to set flag is flags and to set 's' denotes syn  'R' denotes reset 'A' to ack
             the result or response we will require only first response as the port if its open it will send syn+ack or if
             it closed it will send rst, so we will use sr1 function
             so accordingly our synprobe consists of result we have to only check if the layer 4 of response has syn set or
              syn+ack so the port is open and if rst or rst+ack is set the port is closed  
             """
            #SYN SCAN
            synprobe = sr1(IP(dst=target) / TCP(sport=RandShort(), dport=port, flags='S'))
            respflags = synprobe.getlayer(
                TCP).flags  # now respflags consists of the flags that are set but its in hex form
            if respflags == 0x12:
                result += f"{red}{port}\tOPEN\t\n{reset}"

        except Exception as e:
            print(f"An error occurred: {e}")

        rstprobe = IP(dst=target) / TCP(sport=RandShort(), dport=port, flags='R')
        send(rstprobe)
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
    t = threading.Thread(target=scan_port, args=(i,),daemon=True)
    t.start()

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
