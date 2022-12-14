from PPP.protocols import Ethernet

class raw_packet_header():
    def __init__(self, Packet):
        Packet.update_widths(8, 28)
        

class raw_packet_header_desc():
    def __init__(self, Packet):
        pass
        
class print_raw_packet_header(Ethernet.print_Ethernet):
    def __init__(self, parent):
        pass
