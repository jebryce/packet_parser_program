from PPP.protocols import Ethernet

class sFlow():
    def __init__(self, Packet):

        Packet.update_widths(8, 28)

        self.datagram_version = Packet.IPv4.UDP.payload[0:4]
        self.agent_address_type = Packet.IPv4.UDP.payload[4:8]
        self.agent_address = Packet.IPv4.UDP.payload[8:12]
        self.sub_agent_id = Packet.IPv4.UDP.payload[12:16]
        self.sequence_number = Packet.IPv4.UDP.payload[16:20]
        self.system_uptime = Packet.IPv4.UDP.payload[20:24]
        self.number_of_samples = Packet.IPv4.UDP.payload[24:28]
        self.samples = Packet.IPv4.UDP.payload[28:]

class sFlow_desc():
    def __init__(self, Packet):
        self.datagram_version = 'Version of the sFlow protocol.'
        if Packet.IPv4.UDP.sFlow.agent_address_type.hex() == '00000001':
            self.agent_address_type = 'IPv4'
        else:
            self.agent_address_type = 'IPv6'
        self.agent_address = 'Source IP address for the sFlow message.'
        self.sub_agent_id = 'ID of the sFlow process in the switch/router.'
        self.sequence_number = 'A counter for the number of sFlow datagrams sent.'
        self.system_uptime = 'Uptime of the switch/router in milliseconds.'
        self.number_of_samples = 'Number of sFlow samples sent in the packet.'
        
class print_sFlow(Ethernet.print_Ethernet):
    def __init__(self, parent):
        # so I wouldn't have to type out (or copy) this long ass message
        sFlow = parent.Packet.IPv4.UDP.sFlow

        parent.pf.print_data_bar(parent.widths)
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'sFlow',
                '18C7', 
                'InMon sFlow (sampled flow) Protocol'
            ]
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Version',
                sFlow.datagram_version.hex().upper(), 
                sFlow.desc.datagram_version
            ],
            arrow_length = 3
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Address Type',
                sFlow.agent_address_type.hex().upper(), 
                sFlow.desc.agent_address_type
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Agent Address',
                sFlow.agent_address.hex().upper(),
                sFlow.desc.agent_address
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sub-agent ID',
                sFlow.sub_agent_id.hex().upper(), 
                sFlow.desc.sub_agent_id
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sequence Number',
                sFlow.sequence_number.hex().upper(), 
                sFlow.desc.sequence_number
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'System Uptime',
                sFlow.system_uptime.hex().upper(), 
                sFlow.desc.system_uptime
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Count',
                sFlow.number_of_samples.hex().upper(), 
                sFlow.desc.number_of_samples
            ],
            arrow_length = 3
        )
