#!/usr/bin/env python3
import os
import json
import shutil

##
# Generate Wireguard config for Librenms Wireguard extend
# https://docs.librenms.org/Extensions/Applications/#wireguard
##
# Uses Wireguard config generated by @Nyr Wireguard Road Warrior
# https://github.com/Nyr/wireguard-install
##
configFolder="/etc/wireguard/"
outConfig="/etc/snmp/wireguard.json"
wgCommand=shutil.which('wg')
if wgCommand:
    PeerList={"wg_cmd": wgCommand,"public_key_to_arbitrary_name": {}}
else:
    raise FileNotFoundError

try:
    for filename in os.listdir(configFolder):
        configFile = os.path.join(configFolder, filename)
        if os.path.isfile(configFile) and "conf" in filename:
            infName = filename.split('.')[0]
            print("Processing WG interface - {}".format(infName))
            PeerList["public_key_to_arbitrary_name"][infName] = {}
            with open(configFile, 'r') as file:
                content=file.readlines()
                #print(content)
                for line in content:
                    # print(line)
                    if "BEGIN_PEER" in line:
                        PeerName = line.split()[2]
                        Index=content.index(line)
                        PubKey=content[Index+2].split()[2]
                        PeerList["public_key_to_arbitrary_name"][infName][PubKey] = PeerName
                        print("{} - {}".format(PeerName, PubKey))
except IOError:
    print("Unable to read WireGuard config")
finally:
    file.close()

try:
    print(json.dumps(PeerList))
    with open(outConfig, 'wt') as file:
        file.write(json.dumps(PeerList))

except IOError:
    print("Unable to save config")

finally:
    file.close()
