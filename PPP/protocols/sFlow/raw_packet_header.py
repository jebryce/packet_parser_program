from PPP.protocols import Ethernet

class raw_packet_header():
    def __init__(self, Packet):
        Packet.update_widths(8, 28)
        raw_header = Packet.IPv4.UDP.sFlow.flow_sample.raw_header

        self.enterprise = Packet.extract_bits(raw_header[0:3], 0xFFFFF0)
    
        self.format = Packet.extract_bits(raw_header[2:4], 0x0FFF)

        self.flow_data_length = raw_header[4:8]
        self.header_protocol = raw_header[8:12]
        self.frame_length = raw_header[12:16]
        self.payload_stripped = raw_header[16:20]

        self.sampled_header_length = raw_header[20:24]
        
        header_length = int.from_bytes(self.sampled_header_length, 'big')
        self.sampled_packet = raw_header[24:24 + header_length]

        self.switch_data = raw_header[24 + header_length : ]

class raw_packet_header_desc():
    def __init__(self, Packet):
        self.enterprise = ''
        self.format = ''
        self.flow_data_length = ''
        self.header_protocol = ''
        self.frame_length = ''
        self.payload_stripped = 'Number of bytes of the payload that were stripped off.'
        self.sampled_header_length = ''
        
class print_raw_packet_header(Ethernet.print_Ethernet):
    def __init__(self, parent):
        raw_packet_header = \
            parent.Packet.IPv4.UDP.sFlow.flow_sample.raw_packet_header

        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Raw Packet Header',
                '', 
                ''
            ],
            arrow_length = 4,
            line_case = None
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Enterprise',
                raw_packet_header.enterprise, 
                raw_packet_header.desc.enterprise
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Format',
                raw_packet_header.format, 
                raw_packet_header.desc.format
            ],
            arrow_length = 6
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Flow Data Length',
                raw_packet_header.flow_data_length, 
                raw_packet_header.desc.flow_data_length
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Header Protocol',
                raw_packet_header.header_protocol, 
                raw_packet_header.desc.header_protocol
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Frame Length',
                raw_packet_header.frame_length, 
                raw_packet_header.desc.frame_length
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Payload Stripped',
                raw_packet_header.payload_stripped, 
                raw_packet_header.desc.payload_stripped
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sampled Header Length',
                raw_packet_header.sampled_header_length, 
                raw_packet_header.desc.sampled_header_length
            ],
            arrow_length = 6
        )  
