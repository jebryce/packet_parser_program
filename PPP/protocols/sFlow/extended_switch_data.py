from PPP.protocols import Ethernet

class extended_switch_data():
    def __init__(self, Packet):
        Packet.update_widths(8, 33)
        switch_data = Packet.IPv4.UDP.sFlow.flow_sample.raw_packet_header.switch_data

        self.enterprise = \
            Packet.extract_bits(switch_data[0:3], 0xFFFFF0)

        self.format = Packet.extract_bits(switch_data[2:4], 0x0FFF)

        self.flow_data_length = switch_data[4:8]
        self.incoming_vlan = switch_data[8:12]
        self.incoming_priority = switch_data[12:16]
        self.outgoing_vlan = switch_data[16:20]
        self.outgoing_priority = switch_data[20:24]

class extended_switch_data_desc():
    def __init__(self, Packet):
        self.enterprise = ''
        self.format = ''
        self.flow_data_length = ''
        self.incoming_vlan = ''
        self.incoming_priority = ''
        self.outgoing_vlan = ''
        self.outgoing_priority = ''
        
class print_extended_switch_data(Ethernet.print_Ethernet):
    def __init__(self, parent):
        extended_switch_data = \
            parent.Packet.IPv4.UDP.sFlow.flow_sample.extended_switch_data

        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Extended Switch Data',
                '', 
                ''
            ],
            arrow_length = 4,
            line = 0b11
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Enterprise',
                extended_switch_data.enterprise, 
                extended_switch_data.desc.enterprise
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Format',
                extended_switch_data.format, 
                extended_switch_data.desc.format
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Flow Data Length',
                extended_switch_data.flow_data_length, 
                extended_switch_data.desc.flow_data_length
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Incoming VLAN',
                extended_switch_data.incoming_vlan, 
                extended_switch_data.desc.incoming_vlan
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Incoming Priority',
                extended_switch_data.incoming_priority, 
                extended_switch_data.desc.incoming_priority
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Outgoing VLAN',
                extended_switch_data.outgoing_vlan, 
                extended_switch_data.desc.outgoing_vlan
            ],
            arrow_length = 6
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Outgoing Priority',
                extended_switch_data.outgoing_priority, 
                extended_switch_data.desc.outgoing_priority
            ],
            arrow_length = 6
        )  
