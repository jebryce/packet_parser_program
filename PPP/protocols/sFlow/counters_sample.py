from PPP.protocols import Ethernet

class counters_sample():
    def __init__(self, Packet):
        Packet.update_widths(8, 28)

class counters_sample_desc():
    def __init__(self, Packet):
        pass
        
class print_counters_sample(Ethernet.print_Ethernet):
    def __init__(self, parent):
        pass
