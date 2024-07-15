import socket
import re
import sys
from colorama import Fore, Style

def ssh_version_check(hostname, port):
    try:
        # Create a socket connection to the SSH server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Set timeout for socket operations

        # Connect to the SSH server
        sock.connect((hostname, port))

        # Receive up to 1024 bytes of data from the server
        banner_data = sock.recv(1024).decode('utf-8')

        # Close the socket connection
        sock.close()

        # Extract SSH version from banner
        match = re.search(r'OpenSSH_([\d.]+)', banner_data)
        if match:
            ssh_version = match.group(1)
            print(f"Detected OpenSSH version for {hostname}:{port}: {ssh_version}")

            # Check vulnerability based on version
            vuln_status = get_vulnerability_status(ssh_version)
            if vuln_status == "vulnerable":
                print(f"{Fore.YELLOW}OpenSSH version {ssh_version} is potentially vulnerable.{Style.RESET_ALL}")
                return (hostname, port, ssh_version)  # Return tuple for vulnerable hosts
            elif vuln_status == "not_vulnerable":
                print(f"{Fore.GREEN}OpenSSH version {ssh_version} is not vulnerable.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}OpenSSH version {ssh_version} status is unknown.{Style.RESET_ALL}")

        else:
            print(f"{Fore.YELLOW}Unable to parse OpenSSH version from banner for {hostname}:{port}.{Style.RESET_ALL}")

    except socket.error as e:
        print(f"{Fore.RED}Socket Error: {e}{Style.RESET_ALL}")

    except socket.timeout:
        print(f"{Fore.RED}Connection timed out for {hostname}:{port}.{Style.RESET_ALL}")

    except Exception as ex:
        print(f"{Fore.RED}Error occurred for {hostname}:{port}: {ex}{Style.RESET_ALL}")

    return None

def get_vulnerability_status(ssh_version):
    # Remove any trailing letters after the version number (e.g., 'p1')
    ssh_version = re.sub(r'[a-zA-Z]+$', '', ssh_version)

    # Extract major and minor version numbers
    match = re.match(r'(\d+)\.(\d+)', ssh_version)
    if not match:
        return "unknown"

    major_version = int(match.group(1))
    minor_version = int(match.group(2))

    # Check vulnerability based on specified ranges
    if major_version < 4 or (major_version == 4 and minor_version < 4):
        return "vulnerable"
    elif 4 <= major_version < 8 or (major_version == 8 and minor_version < 5):
        return "not_vulnerable"
    elif 8 <= major_version < 9 or (major_version == 9 and minor_version < 8):
        return "vulnerable"
    else:
        return "not_vulnerable"

def read_hosts_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []

def parse_ports(port_str):
    try:
        return [int(port.strip()) for port in port_str.split(',')]
    except ValueError:
        print("Invalid ports specified.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <filename> <ports>")
        print("Example: python script.py hosts.txt 22,2222")
        sys.exit(1)

    filename = sys.argv[1]
    port_str = sys.argv[2]
    hosts = read_hosts_from_file(filename)
    ports = parse_ports(port_str)

    vulnerable_hosts = []  # List to store vulnerable hosts and their versions

    for host in hosts:
        for port in ports:
            print(f"Checking {host}:{port}...")
            result = ssh_version_check(host, port)
            if result:
                vulnerable_hosts.append(result)
            print()

    if vulnerable_hosts:
        print("\nPotentially Vulnerable Hosts and Their OpenSSH Versions:")
        for ip, port, version in vulnerable_hosts:
            print(f"{ip}:{port} - OpenSSH version {version}")
    else:
        print("\nNo potentially vulnerable hosts found.")
