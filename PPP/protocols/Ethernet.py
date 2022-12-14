from PPP.functions.path import PATH
from PPP.functions import print_functions

class Ethernet():
    def __init__(self, packet):
        # packet is a bytes object
        self.packet = packet

        # ex: b'\xff\xff\xff\xff\xff\xff' (type: bytes)
        # in hex this would be: FF:FF:FF:FF:FF:FF
        self.destination_mac_address = packet[0:6]
        self.source_mac_address = packet[6:12]

        # Check if tagged traffic, 
        # the .hex() function converts the bytes object to a string of hex 
        # values, 8100 is the EtherType 802.1Q (aka tagged traffic)
        if packet[12:14].hex()=='8100':
            # 8100 (type: bytes)
            self.tagged = packet[12:14]

            # ex: 0003 (type: bytes)
            self.vlan_id = packet[14:16]

            # the rest of the packet, this is to avoid a seperate variable to 
            # keep track of the differing index due to the 802.1Q header
            partialPacket = packet[16:]
        else:
            self.tagged = False
            partialPacket = packet[12:]

        # ex: 0806 (type: bytes)
        self.ethertype = partialPacket[0:2]

        self.partial_packet = partialPacket[2:]

        
        self.widths = (8, 11)

    def update_widths(self, *new_widths):
        self.widths = (
            max(self.widths[0], new_widths[0]),
            max(self.widths[1], new_widths[1])
        )
    
    def extract_bits(self, raw: bytes, mask: int):
        length = len(raw)
        decimal = int.from_bytes(raw, 'big')
        extracted = decimal & mask
        return extracted.to_bytes(length, 'big')

class Ethernet_desc():
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
        # configurable description taken from ~/Documents/PPP/config
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
            # '# Created using PPP/functions/make_config.py'
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
                # '# Created using PPP/functions/make_lookups.py'
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
            # '# Created using PPP/functions/make_lookups.py'
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
                      
class print_Ethernet():
    def __init__(
        self, Packet, console = True, file_path = None, bar_length = 150
    ):
        # Packet variable is an object of Packet class defined 
        # in /functions/sdnParser.py
        # (this is the parsed data)
        self.Packet = Packet

        self.widths = Packet.widths

        # see /functions/print_functions.py for more info. It is just a class 
        # that contains functions that format and print a string to either the 
        # console, a file, or both.
        self.pf = print_functions.print_functions(
            console, file_path, bar_length
        )

        # first print the ethernet frames mac addresses
        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #        Type |    MAC Address    | Vendor ID 
        # ------------+-------------------+-------------------------------------
        #      Source | B8:27:EB:3C:2D:60 | Raspberry Pi Foundation 
        # Destination | FF:FF:FF:FF:FF:FF | Broadcast 
        self.print_mac_address_table(
            'Source', 
            Packet.source_mac_address, 
            Packet.desc.source_mac_address, 
            'Destination',
            Packet.destination_mac_address, 
            Packet.desc.destination_mac_address
        )

    def print_mac_address_table(
       self, source_title, source_mac, source_mac_desc,
       dest_title, dest_mac, dest_mac_desc
    ):
        # from the example below, source_title = 'Source' (type: string)
        # source_mac_address = bB27EB3C2D60 (type: bytes)
        # source_mac_desc = 'Raspberry Pi Foundation' (type: string)
        # dest(ination) variables are similar
        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #        Type |    MAC Address    | Vendor ID 
        # ------------+-------------------+-------------------------------------
        #      Source | B8:27:EB:3C:2D:60 | Raspberry Pi Foundation 
        # Destination | FF:FF:FF:FF:FF:FF | Broadcast 

        mac_widths = [11, 17]

        # Print the table as shown above, each self.pf.print_x call prints a row
        # print mac address column headers
        self.pf.print_bar()
        self.pf.print_data(
            column_widths = mac_widths,
            entries = ['Type', 'MAC Address', 'Vendor ID'],
            just = '^'
        )
        self.pf.print_data_bar(column_widths = mac_widths)
        # print source mac address
        self.pf.print_data(
            column_widths = mac_widths,
            entries = [
                source_title,
                source_mac.hex(':').upper(), 
                source_mac_desc
            ],
            just = '^'
        )
        # print destination mac address
        self.pf.print_data(
            column_widths = mac_widths,
            entries = [
                dest_title,
                dest_mac.hex(':').upper(), 
                dest_mac_desc
            ],
            just = '^'
        )
        
    def print_ipv4_address_table(
        self, source_title, source_ipv4, source_ipv4_desc, 
        dest_title, dest_ipv4, dest_ipv4_desc
    ):
        # from the example below, source_title = 'Source' (type: string)
        # source_ipv4_address = bA9FEB234 (type: bytes)
        # source_ipv4_desc = 'placeholder for IP lookup' (type: string)
        # dest(ination) variables are similar
        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #        Type |   IPv4 Address    | Location 
        # ------------+-------------------+-------------------------------------
        #  ARP Sender |  169.254.178.52   | placeholder for IP lookup 
        #  ARP Target |    128.171.1.1    | placeholder for IP lookup 
        
        ipv4_widths = [11, 17]

        # Honestly am surprised this worked
        # this is convert a 4-octet ipv4 address (in type bytes)
        # to a human-readable ip address in the format int.int.int.int
        bytes2ip = '{}.{}.{}.{}'
        # example: bytes2ip.format(*variable)
        # need the asterisk (the unpacking operator), where variable is a 
        # 4-octet bytes object
    
        # Print the table as shown above, each self.pf.print_x call prints a row
        # print ipv4 column headers
        self.pf.print_bar()
        self.pf.print_data(
            column_widths = ipv4_widths,
            entries = ['Type', 'IPv4 Address', 'Location'],
            just = '^'
        )
        self.pf.print_data_bar(column_widths = ipv4_widths)
        # print source ipv4 address
        self.pf.print_data(
            column_widths = ipv4_widths,
            entries = [
                source_title,
                bytes2ip.format(*source_ipv4), 
                source_ipv4_desc
            ],
            just = '^'
        )
        # print destination ipv4 address
        self.pf.print_data(
            column_widths = ipv4_widths,
            entries = [
                dest_title,
                bytes2ip.format(*dest_ipv4), 
                dest_ipv4_desc
            ],
            just = '^'
        )

    def print_ethertype(self, ethertype_abbreviation):
        # from the example below, column_widths is a list of two integers that 
        # determine the widths of the first two columns. In this example it is 
        # [9, 22] (type: list of two integers)
        # ethertype_abbreviation = 'ARP' (type: string)
        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #  EtherType | Value (hex)            | Description 
        # -----------+------------------------+---------------------------------
        #     802.1Q | 8100                   | Customer VLAN Tagged Type 
        #            |--> VLAN ID: 0003       | SDN Production VLAN 
        # -----------+------------------------+---------------------------------
        #        ARP | 0806                   | Address Resolution Protocol


        # Print EtherType column headers
        self.pf.print_bar()
        self.pf.print_data(
            column_widths=self.widths,
            entries=['Protocol', 'Value (hex)', 'Description']
        )
        self.pf.print_data_bar(column_widths = self.widths)

        # Print if tagged traffic
        if self.Packet.tagged != False:
            self.pf.print_data(
                column_widths = self.widths,
                entries = ['802.1Q', '8100', self.Packet.desc.tagged]
            )
            self.pf.print_data(
                column_widths = self.widths,
                entries = [
                    'VLAN ID', 
                    self.Packet.vlan_id.hex().upper(),
                    self.Packet.desc.vlan_id
                ],
                arrow_length = 3
            )
            self.pf.print_data_bar(column_widths = self.widths)

        # print the ethertype of the packet
        self.pf.print_data(
            column_widths = self.widths,
            entries = [
                ethertype_abbreviation,
                self.Packet.ethertype.hex().upper(), 
                self.Packet.desc.ethertype
                ]
        )
        