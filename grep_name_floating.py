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

def grep_floatingip(output):
    lines = output.strip().split('\n')
    vm_list_with_floating_ip = []

    for line in lines[3:]:  # Skip the header rows
        match = re.match(r'\| (.+?) \| (.+?) \|', line)
        if match:
            vm_name = match.group(1).strip()
            networks = match.group(2).strip()

            # Use regular expression to find IP addresses starting with "10.16"
            ip_addresses = re.findall(r'10\.16\.\d+\.\d+', networks)

            if ip_addresses:
                vm_list_with_floating_ip.append((vm_name, ip_addresses[0]))  # Only include the first IP address

    return vm_list_with_floating_ip

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 openstack_server_list.py <host_name>")
        sys.exit(1)

    host_name = sys.argv[1]
    output = execute_openstack_command(host_name)
    vms_with_floating_ip = grep_floatingip(output)

    if len(vms_with_floating_ip) != 0:
        for vm_name, ip_address in vms_with_floating_ip:
            print(f"{vm_name} {ip_address}")
    else:
         print(f"All VMs in {host_name} doesn't have Floating IP")


