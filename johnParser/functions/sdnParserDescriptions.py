# see /functions/sdnParser.py for more detail
#
# This exists really only for humans. The /functions/sdnParser.py file from 
# which this is called, parses all the information a computer needs. But we 
# (hopefully) aren't computers and this function creates English strings that 
# describe what the parsed data represents. 
#
# This file contains all description subclasses the main 'Packet' class 
# creates.
#
# A way to call the description variable, for example:
# my_Packet = Packet(bytes), where bytes is a packet of type bytes
# my_Packet.ethertype                  | returns a bytes object
#                                      | ex: 0806 (type: bytes)
# my_Packet.desc.ethertype             | returns a string that describes
#                                      | ex: 'Address Resolution Protocol (ARP)'
# my_ARP.opcode                 | returns a bytes object
#                                      | ex: 01 (type: bytes)
# my_ARP.desc.opcode            | returns a string that describes
#                                      | ex: 'Request' (type: string)
# generally:                           |
# my_Packet.variable                   | calls the data of variable
# my_Packet.desc.variable              | calls the description of variable
#
import os
from johnParser.functions import path
PATH = path.PATH

class Packet_desc():
    def __init__(self, Packet):
        # Packet variable is an object of Packet class defined 
        # in /functions/sdnParser.py

        # all self.variables should be strings

        # initialize all Ethernet frame variables to be None.
        # this is done so that if a ethertype description needs to open a file 
        # for say, ARP sender/target mac addresses, then the ARP description 
        # class can open the file once and receive all four mac addresses, (ARP 
        # sender, ARP target, ethernet source, and ethernet destination) 
        # instead of opening the file twice and receive each pair indiviudally
        self.packet = None
        self.source_mac_address = None
        self.destination_mac_address = None
        if Packet.tagged != False:
            self.tagged = None
            self.vlan_id = None
        self.ethertype = None
    
    def finish_descriptions(self, Packet):
        # from reasoning above, if the ethernet frame descriptions haven't been 
        # set, fill them in
        if self.packet == None:
            self.packet = 'Raw packet data.'

        # backslahes mean the expression is continued on the next line
        # this is hard to read, so:
        # if both ethernet mac address descriptions are Nonetype
        if self.destination_mac_address == None and \
            self.source_mac_address == None:

            # then call self.mac_address_lookup with the mac addresses
            mac_addresses = self.mac_address_lookup(
                    Packet.destination_mac_address, Packet.source_mac_address
                )
            # then assign the descriptions to the self.var
            self.destination_mac_address = \
                mac_addresses[Packet.destination_mac_address]
            self.source_mac_address = \
                mac_addresses[Packet.source_mac_address]
        
        if Packet.tagged != False:
            if self.tagged == None:
                self.tagged = 'Customer VLAN Tagged Type.' 
            if self.vlan_id == None:
                self.vlan_id = \
                    self.vlan_id_lookup(Packet.vlan_id)[Packet.vlan_id]

        if self.ethertype == None:
            self.ethertype = \
                self.ethertype_lookup(Packet.ethertype)[Packet.ethertype]

    def vlan_id_lookup(self, *vlan_ids):
        # takes in a number of 2 octet vlan_ids
        # returns a dictionary of the same number of strings with a 
        # configurable description taken from ~/Documents/johnParser/config
        # where '~' is user

        # we shouldn't look up the same vlan_id twice, and since vlan_ids
        # is default a tuple, if we change it to a set, the duplicate values 
        # will be dropped.
        vlan_ids = set(vlan_ids)

        # 'with' closes the file after we are finished with it
        config_file = PATH + 'config.txt'
        with open(config_file, 'r',  encoding='utf-8') as config:

            # shortened vlan_id to vid
            # vid_descs will be returned, will be key = X.desc.X variable 
            # provided, and value = description
            vid_descs = dict()

            # skip the first line of the file as it is:
            # '# Created using johnParser/functions/make_config.py'
            config.__next__()
            

            # this was my first attempt at writing a config file
            found_VLANs = False
            for row in config:
                # so first we search for the line 'VLANS\n'
                if found_VLANs == False and row == 'VLANs\n':
                    # once we have found it, latch this boolean
                    found_VLANs = True
                # now start searching every line for our vlan description
                elif found_VLANs == True:
                    # if the line starts with a tab, then continue
                    if row[0] == '\t':
                        # turn row: '\t0003 This is our vlan description!\n'
                        # into ['0003', 'This is our vlan descrption!\n']
                        row = row.replace('\t','').split(' ', 1)
                        # 'XXXX' I implemented as a general description
                        # it is checked first as the bytes.fromhex() function 
                        # cannot take in 'XXXX'
                        if row[0] == 'XXXX':
                            # if you hit 'XXXX', then fill in remaining 
                            # descriptions to a default
                            for vlan_id in vlan_ids:
                                # if key is not in the dictionary
                                if vlan_id not in vid_descs:
                                    # then create a key value pair
                                    vid_descs[vlan_id] = row[1].replace('\n','')
                        else:
                            # zfill fills in zeros from the left
                            # ex: 3 -> 0003
                            row_0 = bytes.fromhex(row[0].zfill(4))
                            # if the ethertype from the file is in the set of 
                            # ethertypes we are requesting
                            if row_0 in vlan_ids:
                                vid_descs[row_0] = row[1].replace('\n','')
                            
                            # if we have found enough descriptions, break
                            if len(vid_descs) == len(vlan_ids):
                                break


                        
                    # once we reach the end of the VLANs data, break
                    else:
                        break

        return vid_descs

    def mac_address_lookup(self, *addresses):
        # takes in a number of 6 octet mac addresses
        # returns a dictionary of the same number of strings with the 
        # organization that owns each respecitive mac address

        # address_descs will be returned, will be key = X.desc.X variable 
        # provided, and value = description
        address_descs = dict()
        # note that dictionaries do not allow duplicate values, so if 4 
        # addresses are passed, then a dictionary of length 3 is returned
        
        # sets also do not allow duplicate values. This is nice so that we 
        # don't have to lookup the same value twice
        addresses = set(addresses)

        # I compare the length of the dictionary at the end, and if they are 
        # seperate lengths, then I add in default descriptions until the 
        # lengths match
        num_addresses = len(addresses)

        # first check if any address is to broadcast 
        broadcast = bytes.fromhex('FFFFFFFFFFFF')
        if broadcast in addresses:
            # if it is, add it to the descriptions and remove it from the set
            address_descs[broadcast] = 'Broadcast'
            addresses.remove(broadcast)

        # similarly, check if any address is all zero
        no_target = bytes.fromhex('000000000000')
        if no_target in addresses:
            address_descs[no_target] = 'Target not yet known.'
            addresses.remove(no_target)

        # if we still have addresses (which we probably always will)
        if len(addresses) > 0:

            # 'with' closes the file after we are finished with it
            mac_lookup_file = PATH + 'mac_lookup.txt'
            with open(mac_lookup_file, 'r', encoding='utf-8') as mac_lookup:

                # skip the first two lines in the file, since the first two 
                # lines are :
                # '# Created using johnParser/functions/make_lookups.py'
                # and
                # 'Assignment Organization Name'
                mac_lookup.__next__()
                mac_lookup.__next__()

                for row in mac_lookup:
                    # splits each row into a list of two values, first 
                    # value is the address block assigned, and the second 
                    # vlaue is the organization that owns the address block
                    # ex: ['0001C7', 'Cisco Systems, Inc\n'] (type:list)
                    row = row.split(' ', 1)

                    # length of address block assigned to organization
                    # ex: 6 (type: int) (this can only be 6, 7, or 9)
                    assigned_length = len(row[0])

                    # for each remaining address, see if the current row matches
                    for address in addresses:
                        # if the first assigned_length hex numbers match
                        if address.hex().upper()[:assigned_length] == row[0]:
                            # then add the description to the dictionary
                            address_descs[address] = row[1].replace('\n', '')
                        
                    # this break is here and not in the if statement above 
                    # in case there are two (or more) mac addresses from the 
                    # same organization 
                    if len(address_descs) == num_addresses:
                        break

                # if we have gone through the entire file and there are still 
                # some addresses without descriptions, add in a default
                if len(address_descs) != num_addresses:
                    # of the remaining addresses
                    for address in addresses:
                        # if they don't have a description
                        if address not in address_descs:
                            # add this default one
                            address_descs[address] = 'No vendor ID found.'
        
        return address_descs

    def ethertype_lookup(self, *ethertypes):
        # takes in a number of 2 octet ethertypes
        # returns the same number of strings with the 

        # we shouldn't look up the same ethertype twice, and since ethertypes 
        # is default a tuple, if we change it to a set, the duplicate values 
        # will be dropped.
        ethertypes = set(ethertypes)

        # 'with' closes the file after we are finished with it
        ethertype_file = PATH + 'ethertype_lookup.txt'
        with open(ethertype_file, 'r', encoding='utf-8') as ethertype_lookup:

            # arg_desc_dict will be returned, will be key = X.desc.X variable 
            # provided, and value = description
            ethertype_descs = dict()  

            # skip the first two lines in the file, as the first two lines are:
            # '# Created using johnParser/functions/make_lookups.py'
            # and
            # 'sign Protocol' 
            # (sign is Assignment, just cut off bc didn't care to change how I 
            # create the file)
            ethertype_lookup.__next__()
            ethertype_lookup.__next__()


            for row in ethertype_lookup:
                # splits each row into a list of two values, first value is
                # the ethertype, and the second vlaue is the description
                # ex: (type: list)
                # ['0806', 'Address Resolution Protocol - A. R. P.\n']
                row = row.split(' ', 1)
                row_0 = bytes.fromhex(row[0])
                if row_0 in ethertypes:
                    ethertype_descs[row_0] = row[1].replace('\n','')
                
                # if we have found enough descriptions, break
                elif len(ethertypes) == len(ethertype_descs):
                    break
            # if we went through the file and haven't found enough descriptions
            if len(ethertypes) != len(ethertype_descs):
                for ethertype in ethertypes:
                    # if an ethertype doesn't have a description
                    if ethertype not in ethertype_descs:
                        # then set it to this default.
                        ethertype_descs[ethertype] = 'Protocol unavailable.'


        return ethertype_descs
                      
class ARP_desc():
    def __init__(self, ARP, Packet):
        # lookup hardware type description
        self.hardware_type = self.hardware_type_lookup(ARP.hardware_type)

        # this shares the same EtherType numbers/descriptions
        # so lookup all ethertype descriptions
        ethertypes = Packet.desc.ethertype_lookup(
            ARP.protocol_type,
            Packet.ethertype
        )
        # then assign them to the correct variables
        self.protocol_type = ethertypes[ARP.protocol_type]
        Packet.desc.protocol_type = ethertypes[Packet.ethertype]

        self.hardware_size = 'Length of the hardware (MAC) address.'

        self.protocol_size = 'Length of the network protocol (IPv4) address.'

        # lookup opcode description
        self.opcode = self.opcode_lookup(ARP.opcode)

        # lookup mac addresses vendor ids
        mac_addresses = Packet.desc.mac_address_lookup(
            Packet.source_mac_address,
            Packet.destination_mac_address,
            ARP.sender_mac_address,
            ARP.target_mac_address
        )
        # then assign them to the correct variables
        Packet.desc.source_mac_address = \
            mac_addresses[Packet.source_mac_address]
        Packet.desc.destination_mac_address = \
            mac_addresses[Packet.destination_mac_address]
        self.sender_mac_address = mac_addresses[ARP.sender_mac_address]
        self.target_mac_address = mac_addresses[ARP.target_mac_address]

        # TODO implement ip address lookup
        self.sender_ip_address = 'Placeholder for IPv4 address lookup.'
        self.target_ip_address = 'Placeholder for IPv4 address lookup.'

    def opcode_lookup(self, opcode):
        # takes in an ARP opcode, returns it's description

        # 'with' statement closes the file after we are finished with it
        opcode_file = PATH + 'ARP_opcode_lookup.txt'
        with open(opcode_file, 'r', encoding='utf-8') as opcode_lookup:
            # skip the first two lines as they are:
            # '# Created using johnParser/functions/make_lookups.py'
            # and
            # 'Number Operation Code (op)'
            opcode_lookup.__next__()
            opcode_lookup.__next__()
            
            # default description
            opcode_desc = 'Unassigned'

            # we look through the file and try to reassign the variable
            for row in opcode_lookup:
                # splits each row into a list of two values, first value is
                # the opcode, and the second vlaue is the description
                # ex: (type: list) ['1', 'REQUEST\n']
                row = row.split(' ', 1)
                if int.from_bytes(opcode,'big') == int(row[0]):
                    opcode_desc = row[1].replace('\n', '').capitalize()
        return opcode_desc

    def hardware_type_lookup(self, hardware_type):
        hardware_type_file = PATH + 'ARP_hardware_lookup.txt'
        with open(hardware_type_file, 'r', encoding='utf-8') as hardware_lookup:
            hardware_lookup.__next__()
            hardware_lookup.__next__()
            hardware_desc = 'Unassigned'
            for row in hardware_lookup:
                row = row.split(' ',1)
                if int.from_bytes(hardware_type,'big') == int(row[0]):
                    hardware_desc = row[1].replace('\n', '')
        return hardware_desc

class IPv4_desc():
    def __init__(self, IPv4, Packet):
        self.version ='Version of the IP protocol. Should always be 4 for IPv4.'
        self.ihl = 'Length of the IPv4 header in number of 32-bit words. Minimum 5.'
        self.dscp = 'Differentiated Services Code Point. Default 0.'
        self.ecn = 'Explicit Congestion Notification. Is an optional feature.'
        self.total_length = 'Length of the entire packet, from this IPv4 header onwards.'
        self.identification = 'Used for identifying a group of fragments.'
        self.flags = 'Used to control or identify fragments.'
        self.fragment_offset = 'Used to specify the offset of a particular fragment.'
        self.ttl = 'Specified in seconds, but is used in practice as a hop count.'
        self.protocol = 'Placeholder for IPv4 protocol lookup.'
        self.checksum = 'Used for error checking of the IPv4 header.'

        # TODO implement ip address lookup
        self.source_ip_address = 'Placeholder for IPv4 address lookup.'
        self.destination_ip_address = 'Placeholder for IPv4 address lookup.'

class ICMP_desc():
    def __init__(self, ICMP, Packet):
        self.type = 'Placeholder for ICMP type lookup.'
        self.code = 'Placeholder for ICMP code lookup.'
        self.checksum = 'Used for error checking of the ICMP header.'
        self.identifier ='Typically a unique identifier for every ping process.'
        self.sequence_number = 'Typically a counter for each process.'

class UDP_desc():
    def __init__(self, UDP, Packet):
        self.source_port = 'Placeholder for UDP port lookup.'
        self.destination_port = 'Placeholder for UDP port lookup.'
        self.length = 'Length of the UDP header and data.'
        self.checksum = 'May be used for error checking of the UDP header and data.'

class sFlow_desc():
    def __init__(self, sFlow, Packet):
        self.datagram_version = 'Version of the sFlow protocol.'
        if sFlow.agent_address_type.hex() == '00000001':
            self.agent_address_type = 'IPv4'
        else:
            self.agent_address_type = 'IPv6'
        self.agent_address = 'Source IP address for the sFlow message.'
        self.sub_agent_id = 'ID of the sFlow process in the switch/router.'
        self.sequence_number = 'A counter for the number of sFlow datagrams sent.'
        self.system_uptime = 'Uptime of the switch/router in milliseconds.'
        self.number_of_samples = 'Number of sFlow samples sent in the packet.'