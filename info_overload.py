import sys
import argparse
import os
import subprocess


#Parse user arguments
parser = argparse.ArgumentParser(description='3ncrypt0R')                                                                                                                                               
parser.add_argument('-ip',
                    metavar='target host',
                    type=str,
                    required=False)

args = parser.parse_args()


#Run initial service discovery via nmap
nmapCommand = ("nmap -sC -sV -T4 -p- -v " + args.ip + " -oN " + args.ip + ".nmap")
#os.system(nmapCommand)

#Grep & cut nmap output for open ports
extract_ports = ("cat " + args.ip + ".nmap" + " | grep \"tcp open\" " + "| cut -d \"/\" -f 1" " > " + args.ip + "_openports.txt")
os.system(extract_ports)

#Grep and cut output for running services
extract_services = ("cat " + args.ip + ".nmap" + " | grep \"tcp open\" " + "| cut -d \" \" -f 4" + " > " + args.ip + "_services.txt")
os.system(extract_services)

# Read nmap output into variables
with open(args.ip + "_openports.txt") as f:
    open_ports = []
    for ports in f:
        open_ports.append(ports.strip())
with open(args.ip + "_services.txt") as f:
    services = []
    for servs in f:
        services.append(servs.rstrip())

#Initial output -> Service discovery results
services_tuple = list(zip(open_ports, services))
print("-------INFO----OVERLOAD------------------")
print("-----------------------------------------")
print("The Target has a total of " + str(len(services)) + " open ports")
print("SYNTAX ([port, service]): " + str(services_tuple))
print("-----------------------------------------")
print("-----------------------------------------")

#The important stuffs! -> NOTE: make more pythonic if idx is not actually needed
for i in range(len(services_tuple)):
    service = services_tuple[i][1]
    port = services_tuple[i][0]
    if "http" in service:
        port =  services_tuple[i][0]
        #Run basic nikto scan -> write to file
        #os.system("nikto -h " + "http://" + args.ip + ":" + str(port) + " > " + args.ip + "p" + port  + "_nikto.txt")
        #Run searchsploit on server version
        get_http_server_version = ("cat " + args.ip + "p" + port  + "_nikto.txt" " | grep \"Server:\"" " | cut -d \" \" -f 3")  
        http_version = subprocess.check_output(get_http_server_version, shell=True)
        print(http_version)
        http_version = http_version.split("/")
        print(http_version)
      
        print(http_version)
        os.system("searchsploit " + str(http_version) + "> " + args.ip + "p" + port + "sploit_http_server.txt") 
    if "ssh" in services_tuple[i]:
        print(services_tuple[i])
    if "netbios-ssn" in services_tuple[i]:
        print("test")
        #smbscan , netstat etc.





