from PPP.protocols import Ethernet

class flow_sample():
    def __init__(self, Packet):
        Packet.update_widths(8, 32)
        sFlow = Packet.IPv4.UDP.sFlow

        self.enterprise = Packet.extract_bits(sFlow.samples[0:3], 0xFFFFF0)
    
        self.sample_type = Packet.extract_bits(sFlow.samples[2:4], 0x0FFF)
    
        self.sample_length = sFlow.samples[4:8]
        self.sequence_number = sFlow.samples[8:12]
        self.source_id_class = sFlow.samples[12:13]
        self.source_id_index = sFlow.samples[13:16]
        
        self.sampling_rate = sFlow.samples[16:20]
        self.sample_pool = sFlow.samples[20:24]
        self.dropped_packets = sFlow.samples[24:28]
        self.input_interface = sFlow.samples[28:32]
        
        self.output_interface_format = \
            Packet.extract_bits(sFlow.samples[32:33], 0b11000000)
        
        
        self.output_interface_value = (int.from_bytes(sFlow.samples[32:36], 'big') & 0x0FFFFFFF).to_bytes(4, 'big')

        self.flow_record = sFlow.samples[36:40]

        self.raw_header = sFlow.samples[40:]

class flow_sample_desc():
    def __init__(self, Packet):
        self.enterprise = 'sFlow structure in use. 0 is standard.'

        
        self.sample_type = 'Flow Sample.'

        self.sample_length = 'Length of the flow sample.'
        self.sequence_number = 'A counter for the number of flow samples.'
        self.source_id_class = ''
        self.source_id_index = ''
        
        self.sampling_rate = 'Number of packets per 1 sample.'
        self.sample_pool = 'Total number of packets.'
        self.dropped_packets = ''
        self.input_interface = ''
        
        self.output_interface_format = ''
        self.output_interface_value = ''

        self.flow_record = ''
        
class print_flow_sample(Ethernet.print_Ethernet):
    def __init__(self, parent, sample_number):
        # so I wouldn't have to type out (or copy) this long ass message
        flow_sample = parent.Packet.IPv4.UDP.sFlow.flow_sample

        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Number',
                sample_number, 
                ''
            ],
            arrow_length = 2
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Enterprise',
                flow_sample.enterprise, 
                flow_sample.desc.enterprise
            ],
            arrow_length = 4
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Type',
                flow_sample.sample_type, 
                flow_sample.desc.sample_type
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Length',
                flow_sample.sample_length, 
                flow_sample.desc.sample_length
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sequence Number',
                flow_sample.sequence_number, 
                flow_sample.desc.sequence_number
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Source ID Class',
                flow_sample.source_id_class, 
                flow_sample.desc.source_id_class
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Source ID Index',
                flow_sample.source_id_index, 
                flow_sample.desc.source_id_index
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sampling Rate',
                flow_sample.sampling_rate, 
                flow_sample.desc.sampling_rate
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Pool',
                flow_sample.sample_pool, 
                flow_sample.desc.sample_pool
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Dropped Packets',
                flow_sample.dropped_packets, 
                flow_sample.desc.dropped_packets
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Input Interface',
                flow_sample.input_interface, 
                flow_sample.desc.input_interface
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Output Interface Format',
                flow_sample.output_interface_format, 
                flow_sample.desc.output_interface_format
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Output Interface Value',
                flow_sample.output_interface_value, 
                flow_sample.desc.output_interface_value
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Flow Record',
                flow_sample.flow_record, 
                flow_sample.desc.flow_record
            ],
            arrow_length = 4
        )