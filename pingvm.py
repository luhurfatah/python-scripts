import sys
import subprocess

def ping_host(vm_name, ip_address):
    try:
        result = subprocess.run(['ping', '-c', '1', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5, text=True)
        if result.returncode == 0:
            return f"{vm_name} ({ip_address}) is pingable."
        else:
            return f"\033[31m{vm_name} ({ip_address}) is not pingable.\033[0m"
    except subprocess.TimeoutExpired:
        return f"\033[31m{vm_name} ({ip_address}) is not pingable (timed out).\033[0m"
    except Exception as e:
        return f"Error occurred while pinging {vm_name} ({ip_address}): {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ping_vms.py <filename>")
        sys.exit(1)

    vm_ip_file = sys.argv[1]

    try:
        with open(vm_ip_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{vm_ip_file}' not found.")
        sys.exit(1)

    for line in lines:
        vm_name, ip_address = line.strip().split()
        result = ping_host(vm_name, ip_address)
        print(result)
