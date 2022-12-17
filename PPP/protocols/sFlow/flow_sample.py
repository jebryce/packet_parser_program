from PPP.protocols import Ethernet

class flow_sample():
    def __init__(self, Packet):
        Packet.update_widths(8, 32)
        sFlow = Packet.IPv4.UDP.sFlow

        self.enterprise = (int.from_bytes(sFlow.samples[0:3], 'big') & 0xFFFFF0).to_bytes(3, 'big')

        
        self.sample_type = (sFlow.samples[2] & 0b1111) * 256
        self.sample_type += sFlow.samples[3]
        self.sample_type = self.sample_type.to_bytes(2, 'big')

        self.sample_length = sFlow.samples[4:8]
        self.sequence_number = sFlow.samples[8:12]
        self.source_id_class = sFlow.samples[12:13]
        self.index = sFlow.samples[13:16]
        
        self.sampling_rate = sFlow.samples[16:20]
        self.sample_pool = sFlow.samples[20:24]
        self.dropped_packets = sFlow.samples[24:28]
        self.input_interface = sFlow.samples[28:32]
        
        self.output_interface = sFlow.samples[32:36]
        self.output_interface_format = (sFlow.samples[32] >> 6).to_bytes(1, 'big')
        self.output_interface_value = (int.from_bytes(sFlow.samples[32:36], 'big') & 0x0FFFFFFF).to_bytes(4, 'big')

        self.flow_record = sFlow.samples[36:40]

class flow_sample_desc():
    def __init__(self, Packet):
        self.enterprise = ''

        
        self.sample_type = ''

        self.sample_length = ''
        self.sequence_number = ''
        self.source_id_class = ''
        self.index = ''
        
        self.sampling_rate = ''
        self.sample_pool = ''
        self.dropped_packets = ''
        self.input_interface = ''
        
        self.output_interface = ''
        self.output_interface_format = ''
        self.output_interface_value = ''

        self.flow_record = ''
        
class print_flow_sample(Ethernet.print_Ethernet):
    def __init__(self, parent):
        # so I wouldn't have to type out (or copy) this long ass message
        flow_sample = parent.Packet.IPv4.UDP.sFlow.flow_sample

        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Flow Sample',
                '1', 
                'sFlow flow sample'
            ],
            arrow_length = 2
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Enterprise',
                flow_sample.enterprise.hex().upper(), 
                flow_sample.desc.enterprise
            ],
            arrow_length = 4
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Type',
                flow_sample.sample_type.hex().upper(), 
                flow_sample.desc.sample_type
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Length',
                flow_sample.sample_length.hex().upper(), 
                flow_sample.desc.sample_length
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sequence Number',
                flow_sample.sequence_number.hex().upper(), 
                flow_sample.desc.sequence_number
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Source ID Class',
                flow_sample.source_id_class.hex().upper(), 
                flow_sample.desc.source_id_class
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Index',
                flow_sample.index.hex().upper(), 
                flow_sample.desc.index
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sampling Rate',
                flow_sample.sampling_rate.hex().upper(), 
                flow_sample.desc.sampling_rate
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Pool',
                flow_sample.sample_pool.hex().upper(), 
                flow_sample.desc.sample_pool
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Dropped Packets',
                flow_sample.dropped_packets.hex().upper(), 
                flow_sample.desc.dropped_packets
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Input Interface',
                flow_sample.input_interface.hex().upper(), 
                flow_sample.desc.input_interface
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Output Interface',
                flow_sample.output_interface.hex().upper(), 
                flow_sample.desc.output_interface
            ],
            arrow_length = 4
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Format',
                flow_sample.output_interface_format.hex().upper(), 
                flow_sample.desc.output_interface_format
            ],
            arrow_length = 6
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Value',
                flow_sample.output_interface_value.hex().upper(), 
                flow_sample.desc.output_interface_value
            ],
            arrow_length = 6
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Flow Record',
                flow_sample.flow_record.hex().upper(), 
                flow_sample.desc.flow_record
            ],
            arrow_length = 4
        )
