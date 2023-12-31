import sys
import subprocess
import re

def execute_openstack_command(host_name):
    try:
        cmd = f"openstack server list --host {host_name} --all --limit -1 -c Name -c Networks"
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error occurred while executing the command: {result.stderr}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

def grep_external_ip(output, site):
    lines = output.strip().split('\n')
    vm_list_external_ip = []
    vm_list_internal_ip = []
    no_external_ip = []
    total_vms = 0

    for line in lines[3:]:  # Skip the header rows
        match = re.match(r'\| (.+?) \| (.+?) \|', line)
        if match:
            total_vms = total_vms + 1
            vm_name = match.group(1).strip()
            networks = match.group(2).strip()
            external_check = vm_list_external_ip[:]

            # Use regular expression to find all IP addresses
            ip_addresses = re.findall(r'\d+\.\d+\.\d+\.\d+', networks)
            for ip_address in ip_addresses:
                if ip_address.startswith('10.16') and site == 'jkt':
                    vm_list_external_ip.append((vm_name, ip_address))
                elif ip_address.startswith('10.0') and site == 'sby':
                    vm_list_external_ip.append((vm_name, ip_address))
                else:
                    vm_list_internal_ip.append((vm_name,ip_address))

            if len(vm_list_external_ip) == len(external_check):
                no_external_ip.append(vm_name)
            
    return vm_list_external_ip, vm_list_internal_ip, no_external_ip, total_vms

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 openstack_server_list.py <host_name>")
        sys.exit(1)

    host_name = sys.argv[1]
    site = re.match(r'sf-(jkt|sby)', host_name).group(1).strip()
    output = execute_openstack_command(host_name)
    vm_list_external_ip, vm_list_internal_ip, no_external_ip, total_vms = grep_external_ip(output, site)

    print("VMs external IP")
    for vm_name, ip_address in vm_list_external_ip:
        print(f"{vm_name} {ip_address}")

    print("\nVMs Without external")
    for vm_name in no_external_ip:
        print(f"{vm_name}")

    print("\nVMs Internal IP")
    for vm_name, ip_address in vm_list_internal_ip:
        print(f"{vm_name} {ip_address}")

    print(f"\nTotal VMs with external IP {len(vm_list_external_ip)}")
    print(f"Total VMs Internal IP {len(vm_list_internal_ip)}")
    print(f"Total VMs {total_vms}")
