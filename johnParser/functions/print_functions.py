# moved into new file in case we want to print something else with the same 
# formatting. Saved as a class for ease of importing. 
# 
# example usage:
# from functions import print_functions
# pf = print_functions.print_functions()
# pf.print_bar()

from johnParser.functions import wrap_line
# see /functions/wrap_line.py for more information on what it does (but it 
# basically just takes a long string and breaks it (at space characters) into 
# shorter strings)



class print_functions():
    def __init__(self,console=True, file_path=None,bar_length=150):
        # defaults to printing to console (console=True)
        # defualts to not printing to a file (file_path=None)
        # Note: you can print to both
        # bar_length defaults to 150 - it is the (max) number of characters
        # wide everything prints
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

    # ex: '--------------+-------------------+---------------------------------'
    def print_data_bar(self,column_widths):
        # column_widths should be a list of 2 integers, corresponding with the 
        # widths of the first two columns. The third column's width will be 
        # calculated using the bar_length variable passed when calling the class
        # ex = [10,20]
        #
        # cutoff is how many characters wide the third column is
        # the int 7 represents the spaces and '|' characters used in the 
        # print_data() function - it is one less character for presentation
        cutoff = self.bar_length - 7 - sum(column_widths)

        # the extra '-' characters (why it is '--+-' instead of '+') are to 
        # account for the forced white space in the print_data() function
        data_bar = column_widths[0]*'-' + '--+-' + \
            column_widths[1]*'-' + '-+-' + cutoff*'-'
        self.optional_print(data_bar)
            


    # '              VLAN ID | 3                 | SDN Production'
    # '                      |--> VLAN ID: 3     | SDN Production'
    # (function combines first 2 columns in event of a passed arrow length)
    def print_data(self, column_widths, entries, arrow_length = 0, just = '<'):
        # column_widths should be a list of 2 integers, corresponding with the 
        # widths of the first two columns. The third column's width will be 
        # calculated using the bar_length variable passed when calling the class
        # ex = [10,20]
        #
        # entries should be a list of 3 strings, corresponding with the entires 
        # of columns 1, 2, and 3. 
        # ex = ['VLAN ID','3','SDN Production']
        #
        # arrow_length creates an arrow in the second column and moves the 
        # string in entries[0] to be combined with entries[1] (this is done 
        # because it looks better imo, (especially with multiple rows))
        # ex if arrow_length = 0
        # '              VLAN ID | 3                 | SDN Production'
        # ex if arrow_length = 3
        # '                      |--> VLAN ID: 3     | SDN Production'
        #
        # just is the justification of the second column
        # ex if just = '<' then: 
        # '        Type | MAC Address       | Vendor ID ' 
        # ex if just = '^' then:
        # '        Type |    MAC Address    | Vendor ID '


        # at the ends of this function, it calls a custom print function and 
        # passes this string formatted. 
        # (on the internet, lookup python string format() method for more info)
        data_format = ' {first_entry:>{first_column_width}} |{arrow}' + \
            ' {second_entry:{just}{second_column_width}} | {third_entry} '


        # if arrow length is passed, creates the arrow and combines entries 1 
        # and 2 into the second column. 
        # (this is done bc I think it looks better)
        if arrow_length == 0:
            arrow = ''

        elif arrow_length > 0:
            # ex: '----->'
            arrow = (arrow_length-1)*'-' + '>'

            # imo, instead of printing:
            # ex: '              VLAN ID |--> 3              | SDN Production'
            # it looks better to print: 
            # ex: '                      |--> VLAN ID: 3     | SDN Production'
            entries[1] = entries[0]+': '+entries[1]
            entries[0] = ''


        # cutoff is how many characters wide the third column is
        # the int 8 represents the spaces and '|' characters used in the 
        # data_format string
        cutoff = self.bar_length - 8 - sum(column_widths)

        # arrow length is subtracted from column_widths for (imo) easier use 
        # for the programmer - it keeps the second column the same total width 
        # with or without the arrow
        second_column_width = column_widths[1] - arrow_length

        
        # if the data of the third column fits in the width provided, then 
        # print on one line
        #
        # ex:
        # '              VLAN ID | 3                 | SDN Production'
        if len(entries[2]) < cutoff:
            self.optional_print(data_format.format(
                first_entry = entries[0],
                first_column_width = column_widths[0], 
                arrow = arrow,
                second_entry = entries[1],
                just = just,
                second_column_width = second_column_width,
                third_entry = entries[2]
            ))

        # if it doesn't, then call the function wrap_line I created, which 
        # splits up a string at space characters into smaller strings 
        # see /functions/wrap_line.py for more info
        else:  
            # wrap_line() populates this list that is passed
            print_list = list()
            wrap_line.wrap_line(print_list,entries[2],cutoff)

            # first, print the data that was passed to the start of this 
            # print_data() function and the first string returned from the 
            # wrap_line() function
            #
            # ex:
            # '                |--> VLAN ID: 3     | (pretend this is longer)'
            self.optional_print(data_format.format(
                first_entry = entries[0],
                first_column_width = column_widths[0], 
                arrow = arrow,
                second_entry = entries[1],
                just = just,
                second_column_width = second_column_width,
                third_entry = print_list[0]
            ))


            # then, print the extra strings in the third column, but nothing in 
            # the first two columns
            #
            # ex
            # '                |                   | wrapped around text!'
            for string in print_list[1:]:
                self.optional_print(data_format.format(
                    first_entry = '',
                    first_column_width = column_widths[0], 
                    arrow = '',
                    second_entry = '',
                    just = '',
                    second_column_width = column_widths[1],
                    third_entry = string
                ))
        #



# pf = print_functions()
# pf.print_bar()
# widths = [20,17]
# ents = ['Destination','FF.FF.FF.FF.FF.FF','Broadcast, but thsis is super long to test out the wrap line function, tbh and holy crud his ofirst part wasnt long enoiuguh either to fully test  iahsdfhi jasdfhj aksjdhf kjahsdf kjhasdfkj hashkjdf kjahsdfk jhasdkf jhaskjd fhaksdjhf kasdhf kjahsdf kjhasfk jhaskdjf haksjdhf kajsdhfkajnbrsjhbeqrjha sbdsjhb ajshebr ugyaesbruy gabajdhfkajdhsfkjhasdomgthiswasntevenclosetobeinglongenoughwtfhowmanycharactersis150characetsjesuswellthissurelyis150charactersnowfhjkaskdhjfhjkathisistotestoutthehyphenatefunction!!!!!!!!abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ']
# ents2 = ['VLAN ID', '3','SDN Production']
# pf.print_data_bar(column_widths=widths)
# pf.print_data(column_widths=widths,entries=ents)
# pf.print_data(column_widths=widths,entries=ents,arrow_length = 3)


