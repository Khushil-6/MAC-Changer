
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help=" Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help=" New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more help")
    elif not options.new_mac:
        parser.error("[-] Please specify an new MAC, use --help for more help")
    return options


def chang_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print(f"[+] Changing MAC address for {interface} to {new_mac}")


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    search_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if search_mac:
        return search_mac.group(0)
    else:
        print("[+] Could not read MAC address")


option = get_arguments()

current_mac = get_current_mac(option.interface)
print(f"Current MAC: {str(current_mac)}")

chang_mac(option.interface, option.new_mac)
current_mac = get_current_mac(option.interface)

if current_mac == option.new_mac:
    print(f"[+] MAC address was successfully changed to {current_mac}")
else:
    print("[+] MAC address did not get changed")





