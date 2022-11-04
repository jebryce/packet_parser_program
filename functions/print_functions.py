# moved into new file in case we want to print something else with the same 
# formatting. Saved as a class for ease of importing. 
# 
# example usage:
# from functions import print_functions
# pf = print_functions.print_functions()
# pf.print_bar()
# pf.print_address(type = 'Type', data = 'MAC Address', desc='Vendor ID')
# pf.print_address_line()
# pf.print_info(type = '802.1Q', data = '8100', desc = Packet.desc.tagged)
# pf.print_info_data(
#    type = 'VLAN ID',
#    data = Packet.vlan_id.hex().upper().lstrip('0'), 
#    desc = Packet.desc.vlan_id
#    )
# pf.print_info_line()

from functions import wrap_line
# see /functions/wrap_line.py for more information on what it does (but it 
# basically just takes a long string and breaks it (at space characters) into 
# shorter strings)



class print_functions():
    def __init__(self,console=True, file_path=None,bar_length=150):
        # defaults to printing to console (console=True)
        # defualts to not printing to a file (file_path=None)
        # Note: you can print to both
        # bar_length defaults to 150 - it is the number of characters wide 
        # everything prints
        self.console = console
        self.file_path = file_path
        self.bar_length = bar_length

    # prints each line to either the console, a file, or both
    def optional_print(self,line):
        if self.file_path != None:
            with open(self.file_path, 'a') as packet_info_file:
                packet_info_file.write(line+'\n')
        if self.console == True:
            print(line)




    # Initialize string formats
    # I created this functions, as it imo it is more readable to code
    # print_functions.print_address() 
    # instead of print_functions.optional_print(pkt_address_table.format()) 

    # ex: '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    def print_bar(self):
        bar = self.bar_length*'%'
        self.optional_print(bar)

    # ex: '         Type |    MAC Address    | Vendor ID'
    def print_address(self,type = '', data = '', desc = ''):
        cutoff = self.bar_length - 39
        pkt_address_table = " {type:>15} | {data:^17} | {desc}"
        if len(desc) > cutoff:
            print_list = list()
            wrap_line.wrap_line(print_list,desc,cutoff)
            self.optional_print(pkt_address_table.format(
                type = type, data = data, desc = print_list[0]
            ))
            for string in print_list[1:]:
                self.optional_print(pkt_address_table.format(
                    type ='', data= '', desc = string
                ))
        else:
            self.optional_print(pkt_address_table.format(
                type = type, data = data, desc = desc
            ))

    # ex: '-----------------+-------------------+------------------------------'
    def print_address_line(self):
        address_line = 17*'-'+'+'+19*'-'+'+'+(self.bar_length-38)*'-'
        self.optional_print(address_line)

    # ex: '    EtherType | Value (numbers are in hex)     | Description'
    def print_info(self,type = '', data = '', desc = ''):
        cutoff = self.bar_length - 52

        pkt_info_table = " {type:>15} | {data:<30} | {desc}"
        if len(desc) > cutoff:
            print_list = list()
            wrap_line.wrap_line(print_list,desc,cutoff)
            self.optional_print(pkt_info_table.format(
                type = type, data = data, desc = print_list[0]
            ))
            for string in print_list[1:]:
                self.optional_print(pkt_info_table.format(
                    type ='', data= '', desc = string
                ))
        else:
            self.optional_print(pkt_info_table.format(
                type = type, data = data, desc = desc
            ))
 


        
    # ex: '              |--> VLAN ID: 3                  | SDN Production VLAN'
    def print_info_data(self,type = '', data = '', desc = ''):
        # 49 is the width of the screen already taken up by the format string
        cutoff = self.bar_length - 52
        type_data = type+': '+ data
        pkt_info_data_table = 17*' '+"|--> {type_data:<27} | {desc}"
        if len(desc) > cutoff:
            print_list = list()
            print_list = wrap_line.wrap_line(print_list,desc,cutoff)

            self.optional_print(pkt_info_data_table.format(
                type_data = type_data, desc = print_list[0]
            ))
            for string in print_list[1:]:
                self.print_info(desc = string)
        else:
            self.optional_print(pkt_info_data_table.format(
                type_data = type_data, desc = desc
            ))
        



    # ex: '-----------------+--------------------------------+-----------------'
    def print_info_line(self):
        info_line = 17*'-'+'+'+32*'-'+'+'+(self.bar_length-51)*'-'
        self.optional_print(info_line)

