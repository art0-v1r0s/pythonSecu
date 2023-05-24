import pyfiglet
import sys
import socket
from datetime import datetime
import netifaces
from ping3 import ping, verbose_ping


def scan(target, ping):
    # Add Banner
    print("-" * 50)
    print("Scanning Target: " + target)
    print("Scanning started at:" + str(datetime.now()))
    print("-" * 50)

    try:

        if ping is True:
            verbose_ping(target)
        # will scan ports between 1 to 65,535
        for port in range(1, 65535):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            # returns an error indicator
            result = s.connect_ex((target, port))
            if result == 0:
                #    print("Port {} is open".format(port))
                try:
                    banner = s.recv(1024).decode()
                    print("port {} is open with banner {}".format(port, banner))

                except:
                    print("port {} is open ".format(port))
            s.close()

    except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
    except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()


def interface():
    inter = netifaces.interfaces()
    choice = input(f'what interface you wannt to scan ?( 1,2,3 ...)'
                   f'{inter} :')
    print(choice)
    # addrs = netifaces.ifaddresses(inter[int(choice)])
    addrs = netifaces.ifaddresses("wlp0s20f3")
    print(addrs[netifaces.AF_INET])
    target = addrs[netifaces.AF_INET][0]['addr']
    scan(target,ping)


ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)
ping=False
# Defining a target
if len(sys.argv) >= 2:
    if "-h" in sys.argv:
        print("You choose the Hostname argument")
        # translate hostname to IPv4
        target = socket.gethostbyname(sys.argv[1])
    if "-p" in sys.argv:
        print("You choose ping argument")
        # ping allowed
        ping = True

choice = input(f'do you want scan you interface (1) or another ip (2)')
match choice:
    case "1":
        interface()
    case "2":
        target = input(f'Enter the ip to scan :')
        scan(target,ping)
