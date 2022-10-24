import pktSTR2BYT, printPKTinfo



'''
data = open('data.txt','r').read().replace('-','').replace('\n\n','\n')
data2 = open('data2.txt','w')
data2.write(data)
'''



class Packet:
    def __init__(self, packet):
        self.packet = packet
        self.destination_mac_address = self.packet[0:6]
        self.source_mac_address = self.packet[6:12]
        self.findEtherType()

        


    def findEtherType(self):
        #Check if tagged traffic
        if self.packet[12:14].hex()=='8100':
            self.tagged = True
            self.vlan_id = self.packet[14:16]
            self.i = 4
            
        else:
            self.tagged = False
            self.i = 0
        self.ethertype = self.packet[12+self.i:14+self.i]

        if self.ethertype.hex() == '0806':
            self.arp = arp(self.packet[14+self.i:])
        



class arp(Packet):
    def __init__(self, arp_packet):
        # Decided to chop off the front of the packet as tagged traffic would have different index values
        self.arp_packet = arp_packet

        self.hardware_type = self.arp_packet[0:2]
        self.protocol_type = self.arp_packet[2:4]

        # index [4:5] returns a bytes object, index[5] returns an integer
        self.hardware_size = self.arp_packet[4:5]
        self.protocol_size = self.arp_packet[5:6]

        self.opcode = self.arp_packet[6:8]

        self.sender_mac_address = self.arp_packet[8:14]
        self.sender_ip_address = self.arp_packet[14:18]

        self.target_mac_address = self.arp_packet[18:24]
        self.target_ip_address = self.arp_packet[24:28]




pkt_str_list = open('data2.txt','r').readlines()
ct = 0
for pkt_str in pkt_str_list:
    ct += 1
    pkt = pktSTR2BYT.pktSTR2BYT(pkt_str) 
    
    pkt_object = Packet(pkt)

    printPKTinfo.printPKTinfo(pkt_object)
