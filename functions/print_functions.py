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

#from functions import wrap_line
import wrap_line
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
        # file option not tested yet, TODO: test this
        if self.file_path != None:
            # 'with' statement closes file after we are finished with it
            with open(self.file_path, 'a') as packet_info_file:
                packet_info_file.write(line+'\n')

        # prints to console
        if self.console == True:
            print(line)


    # ex: '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    def print_bar(self):
        bar = self.bar_length*'%'
        self.optional_print(bar)

    def print_data_bar(self,column_widths):
        # column_widths should be a list of 2 integers, corresponding with the 
        # widths of the first two columns. The third column's width will be 
        # calculated using the bar_length variable passed when calling the class
        # ex = [10,20]
        #
        # cutoff is how many characters wide the third column is
        # the int 7 represents the spaces and '|' characters used in the 
        # print_data() function
        cutoff = self.bar_length - 7 - sum(column_widths)

        # the extra '-' characters printed with the '+' characters are to 
        # account for the forced white space in the print_data() function
        data_bar = column_widths[0]*'-' + '--+-' + \
            column_widths[1]*'-' + '-+-' + cutoff*'-'
        self.optional_print(data_bar)
            


    # ex: '         Type |    MAC Address    | Vendor ID'
    def print_data(self, column_widths, entries, arrow_length = 0):
        # column_widths should be a list of 2 integers, corresponding with the 
        # widths of the first two columns. The third column's width will be 
        # calculated using the bar_length variable passed when calling the class
        # ex = [10,20]
        # entries should be a list of 3 strings, corresponding with the entires 
        # of columns 1, 2, and 3. 
        # ex = ['Type','MAC Address','Vendor ID']
        # arrow_length creates an arrow in the second column
        # ex if arrow_length = 0
        # '       Type | MAC Address          | Vendor ID'
        # ex if arrow_length = 5
        # '       Type |----> MAC Address     | Vendor ID'


        # create the arrow length if passed
        if arrow_length == 0:
            arrows = ''
        elif arrow_length > 0:
            arrows = (arrow_length-1)*'-' + '>'

        # cutoff is how many characters wide the third column is
        # the int 7 represents the spaces and '|' characters used in the 
        # data_format string
        cutoff = self.bar_length - 7 - sum(column_widths)

        # arrow length is subtracted from column_widths for (imo) easier use 
        # for the programmer - it keeps the middle column the same total width 
        # with or without the arrow
        column_widths[1] -= arrow_length

        # at the ends of this function, it calls a custom print function and 
        # passes this string formatted. 
        # (on the internet, lookup python string format() method for more info)
        data_format = ' {type:>{first_column_width}} |' + \
            arrows + ' {data:<{second_column_width}} | ' + '{desc}'

        
        # if the data of the third column fits in the width provided, then 
        # print on one line
        #
        # ex if arrow_length = 5
        # '       Type |----> MAC Address     | Vendor ID'
        if len(entries[2]) < cutoff:
            self.optional_print(data_format.format(
                first_column_width = column_widths[0], 
                second_column_width = column_widths[1],
                type = entries[0], data = entries[1], desc = entries[2]
            ))

        # if it doesn't, then call the function wrap_line I created, which 
        # splits up a string at space characters into smalled strings 
        # see /functions/wrap_line.py for more info
        else:  
            # wrap_line() populates this list that is passed
            print_list = list()
            wrap_line.wrap_line(print_list,entries[2],cutoff)

            # first, print the data that was passed to the start of this 
            # print_data() function and the first string returned from the 
            # wrap_line() function
            #
            # ex if arrow_length = 5
            # '       Type |----> MAC Address     | (pretend this is longer)'
            self.optional_print(data_format.format(
                first_column_width = column_widths[0], 
                second_column_width = column_widths[1],
                type = entries[0], data = entries[1], desc = print_list[0]
            ))

            # then, print the extra strings in the third column, but nothing in 
            # the first two columns
            #
            # note, I added back in the arrow_length to the second column for 
            # prettier printing
            # ex: if arrow_length = 5
            # '            |                      | wrapped around data!'
            for string in print_list[1:]:
                self.optional_print(data_format.format(
                    first_column_width = column_widths[0], 
                    second_column_width = column_widths[1] + arrow_length,
                    type = '', data = '', desc = string
                ))



    # # ex: '-----------------+-------------------+------------------------------'
    # def print_address_line(self):
    #     address_line = 17*'-'+'+'+19*'-'+'+'+(self.bar_length-38)*'-'
    #     self.optional_print(address_line)

    # # ex: '    EtherType | Value (numbers are in hex)     | Description'
    # def print_info(self,type = '', data = '', desc = ''):
    #     # 52 is the width of the screen already taken up by the format string
    #     cutoff = self.bar_length - 52
    #     pkt_info_table = " {type:>15} | {data:<30} | {desc}"
    #     if len(desc) > cutoff:
    #         print_list = list()
    #         wrap_line.wrap_line(print_list,desc,cutoff)
    #         self.optional_print(pkt_info_table.format(
    #             type = type, data = data, desc = print_list[0]
    #         ))
    #         for string in print_list[1:]:
    #             self.optional_print(pkt_info_table.format(
    #                 type ='', data= '', desc = string
    #             ))
    #     else:
    #         self.optional_print(pkt_info_table.format(
    #             type = type, data = data, desc = desc
    #         ))
 


        
    # # ex: '              |--> VLAN ID: 3                  | SDN Production VLAN'
    # def print_info_data(self,type = '', data = '', desc = ''):
    #     # 49 is the width of the screen already taken up by the format string
    #     cutoff = self.bar_length - 52
    #     type_data = type+': '+ data
    #     pkt_info_data_table = 17*' '+"|--> {type_data:<27} | {desc}"
    #     if len(desc) > cutoff:
    #         print_list = list()
    #         print_list = wrap_line.wrap_line(print_list,desc,cutoff)

    #         self.optional_print(pkt_info_data_table.format(
    #             type_data = type_data, desc = print_list[0]
    #         ))
    #         for string in print_list[1:]:
    #             self.print_info(desc = string)
    #     else:
    #         self.optional_print(pkt_info_data_table.format(
    #             type_data = type_data, desc = desc
    #         ))
        



    # # ex: '-----------------+--------------------------------+-----------------'
    # def print_info_line(self):
    #     info_line = 17*'-'+'+'+32*'-'+'+'+(self.bar_length-51)*'-'
    #     self.optional_print(info_line)

