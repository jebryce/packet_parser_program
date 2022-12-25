from PPP.protocols import Ethernet

class counters_sample():
    def __init__(self, Packet):
        Packet.update_widths(8, 28)
        samples = Packet.IPv4.UDP.sFlow.samples
        self.enterprise = Packet.extract_bits(samples[0:3], 0xFFFFF0)
    
        self.sample_type = Packet.extract_bits(samples[2:4], 0x0FFF)
        self.sample_length = samples[4:8]
        self.sequence_number = samples[8:12]

        self.source_id_class = samples[12:13]
        self.source_id_index = samples[13:16]
        self.counters_records = samples[16:20]


class counters_sample_desc():
    def __init__(self, Packet):
        self.enterprise = ''
        self.sample_length = ''
        self.sample_type = ''
        self.sequence_number = ''

        self.source_id_class = ''
        self.source_id_index = ''
        self.counters_records = ''
        
class print_counters_sample(Ethernet.print_Ethernet):
    def __init__(self, parent):
        pass
