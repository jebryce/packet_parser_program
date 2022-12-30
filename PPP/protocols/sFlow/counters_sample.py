from PPP.protocols import Ethernet

class counters_sample():
    def __init__(self, Packet, index):
        Packet.update_widths(8, 28)
        samples = Packet.IPv4.UDP.sFlow.samples[index:]
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
        
        self.sample_type = ''
        self.sample_length = ''
        self.sequence_number = ''

        self.source_id_class = ''
        self.source_id_index = ''
        self.counters_records = ''
        
class print_counters_sample(Ethernet.print_Ethernet):
    def __init__(self, parent, sample_number):
        counters_sample = parent.Packet.IPv4.UDP.sFlow.counters_sample
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Number',
                str(sample_number), 
                ''
            ],
            arrow_length = 2,
            line_case = '_'
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Enterprise',
                counters_sample.enterprise, 
                counters_sample.desc.enterprise
            ],
            arrow_length = 4
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Type',
                counters_sample.sample_type, 
                counters_sample.desc.sample_type
            ],
            arrow_length = 4
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Length',
                counters_sample.sample_length, 
                counters_sample.desc.sample_length
            ],
            arrow_length = 4
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sequence Number',
                counters_sample.sequence_number, 
                counters_sample.desc.sequence_number
            ],
            arrow_length = 4
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Source ID Class',
                counters_sample.source_id_class, 
                counters_sample.desc.source_id_class
            ],
            arrow_length = 4
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Source ID Index',
                counters_sample.source_id_index, 
                counters_sample.desc.source_id_index
            ],
            arrow_length = 4
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Counters Records',
                counters_sample.counters_records, 
                counters_sample.desc.counters_records
            ],
            arrow_length = 4
        )  
