import subprocess

# Main menu
while True:
    try:
        def main_menu():
            print("Select a script to run:")
            print("1. Information gathering")
            print("2. Packet sniffer")
            print("3. Network scanner")
            print("4. Simple port scanner")
            print("5. Advanced port scanner using multi-threading")
            print("6. Port scanner using tcp connection(scapy) ")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                print("Running Information gathering script...")
                print("This script requires the following arguments:")
                print("-d, --domain: Enter the domain name for footprinting")
                print("-o, --output: Enter the file to write output to (optional)")

                domain = input("Enter the domain name for footprinting: ")
                output = input("Enter the file name to write output to (optional): ")

                command = ["python", "info_gathering.py", "-d", domain]
                if output:
                    command.extend(["-o", output])

                subprocess.run(command)

            elif choice == '2':
                iface = input("Enter the interface through which you want to sniff: ")
                command = ["python", "scapy_sniffer.py", "-i",iface]
                subprocess.run(command)

            elif choice == '3':
                print("Running Network scanner script...")
                print("This script requires the following argument:")
                print("-i, --target_network: Enter the network range or subnet that you want to scan")

                target_network = input("Enter the network range or subnet that you want to scan: ")

                subprocess.run(["python", "network_scanner.py", "-i", target_network])

            elif choice == '4':
                print("Running simple port scanner script...")
                print("This script requires the following arguments:")
                print("-t, --target: Enter the target IP to scan")
                print("-s, --start_port: Enter the starting port no. from which you want to scan")
                print("-e, --end_port: Enter the ending port no. till which you want to scan")

                target = input("Enter the target IP to scan: ")
                start_port = input("Enter the starting port no. from which you want to scan: ")
                end_port = input("Enter the ending port no. till which you want to scan: ")

                subprocess.run(["python", "simple_port_scanner.py", "-t", target, "-s", start_port, "-e", end_port])

            elif choice == '5':
                print("Running advanced port scanner using multi-threading script...")
                print("-t, --target: Enter the target ip to scan")
                print("-s, --start_port: Enter the starting port no. from which you want to scan")
                print("-e, --end_port: Enter the ending port no. till which you want to scan")
                print("--threads :Enter the number of threads you want to run")
                print("-o, --output,: Enter the name and path file to write output to")

                target = input("Enter the target IP to scan: ")
                start_port = input("Enter the starting port no. from which you want to scan:")
                end_port = input("Enter the ending port no. till which you want to scan:")
                threads= input("Enter the number of threads you want to run")
                output = input("Enter the file name to write output to: ")

                command = ["python", "fast_port_scanner.py", "-t", target, "-s", start_port, "-e", end_port,"--threads",threads]
                if output:
                    command.extend(["-o", output])

                subprocess.run(command)

            elif choice == '6':
                print("Running port scanner using scapy script...")
                print("This script requires the following arguments:")
                print("-t, --target: Enter the target IP to scan")
                print("-s, --start_port: Enter the starting port no. from which you want to scan")
                print("-e, --end_port: Enter the ending port no. till which you want to scan")
                print("--threads: Enter the number of threads you want to run")
                print("-o, --output: Enter the name and path file to write output to")

                target = input("Enter the target IP to scan: ")
                start_port = input("Enter the starting port no. from which you want to scan: ")
                end_port = input("Enter the ending port no. till which you want to scan: ")
                threads = input("Enter the number of threads you want to run: ")
                output = input("Enter the name of file to write output to: ")

                command = ["python", "scapy_simple_version.py", "-t", target, "-s", start_port, "-e", end_port, "--threads",
                           threads]
                if output:
                    command.extend(["-o", output])

                subprocess.run(command)

            elif choice == '0':
                print("Exiting...")
            else:
                print("Invalid choice. Please try again.")
                main_menu()


        if __name__ == "__main__":
            main_menu()

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...")
        exit()
    except Exception as e:
        print(f"Error occured : {e}")