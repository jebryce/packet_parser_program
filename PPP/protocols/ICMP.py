from PPP.protocols import Ethernet

class ICMP():
    def __init__(self, Packet):

        Packet.update_widths(8, 24)
        
        self.type = Packet.IPv4.partial_packet[0:1]
        self.code = Packet.IPv4.partial_packet[1:2]
        self.checksum = Packet.IPv4.partial_packet[2:4]
        self.identifier = Packet.IPv4.partial_packet[4:6]
        self.sequence_number = Packet.IPv4.partial_packet[6:8]
        self.payload = Packet.IPv4.partial_packet[8:]

class ICMP_desc():
    def __init__(self, Packet):
        self.type = 'Placeholder for ICMP type lookup.'
        self.code = 'Placeholder for ICMP code lookup.'
        self.checksum = 'Used for error checking of the ICMP header.'
        self.identifier ='Typically a unique identifier for every ping process.'
        self.sequence_number = 'Typically a counter for each process.'

class print_ICMP(Ethernet.print_Ethernet):
    def __init__(self, parent):  
        parent.pf.print_data_bar(parent.widths)
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'ICMP',
                '01', 
                'Internet Control Message Protocol'
            ]
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Type',
                parent.Packet.IPv4.ICMP.type.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.type
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Code',
                parent.Packet.IPv4.ICMP.code.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.code
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Checksum',
                parent.Packet.IPv4.ICMP.checksum.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.checksum
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Identifier',
                parent.Packet.IPv4.ICMP.identifier.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.identifier
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sequence Number',
                parent.Packet.IPv4.ICMP.sequence_number.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.sequence_number
            ],
            arrow_length = 3
        )
