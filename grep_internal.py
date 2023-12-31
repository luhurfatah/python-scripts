import sys
import subprocess
import re

def execute_openstack_command(host_name):
    try:
        cmd = f"openstack server list --host {host_name} --all -c Name -c Networks"
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error occurred while executing the command: {result.stderr}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

def filter_vm_with_non_10_16_ip(output):
    lines = output.strip().split('\n')
    vm_list = []

    for line in lines[3:]:  # Skip the header rows
        match = re.match(r'\| (.+?) \| (.+?) \|', line)
        if match:
            vm_name = match.group(1).strip()
            networks = match.group(2).strip()

            # Use regular expression to find all IP addresses
            ip_addresses = re.findall(r'\d+\.\d+\.\d+\.\d+', networks)

            for ip in ip_addresses:
                if not ip.startswith('10.16.'):
                    vm_list.append((vm_name, ip))

    return vm_list

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 openstack_server_list.py <host_name>")
        sys.exit(1)

    host_name = sys.argv[1]
    output = execute_openstack_command(host_name)
    filtered_vm_list = filter_vm_with_non_10_16_ip(output)

    if not filtered_vm_list:
        print(f"No VMs with IP addresses not starting with 10.16 found on host '{host_name}'.")
    else:
        for vm_name, ip_address in filtered_vm_list:
            print(f"{vm_name} {ip_address}")
