# inititally, we used the hexdump library to print the raw bytes of a packet
# onto the screen in a human readable way
# import hexdump
# however, the hexdump library could only print to screen (I think)
# instead of looking for another library that we had more control over,
# I felt creating my own was a nice challenge

import math


# the main function to call, this takes in a raw binary packet (of type bytes), 
# then returns a string to be printed to screen
def john_hexdump(
    byte_object: bytes, bytes_per_line: int = 16, 
    column_break_spacing: int = 8, no_character_found: str = '_'
):
    # returns: 
    # a string of the results from make_line_string with newlines 
    # seperating each result
    #
    # input:
    # byte_object - the entire bytes object you'd like to be able to print
    #
    # input:
    # bytes_per_line - the number of bytes you'd like to print per line
    # 
    # input:
    # column_break_spacing - how many bytes to be printed until an extra space 
    # is printed for a visual break
    #
    # input:
    # no_character_found - if the ascii representation is not a standard
    # keyboard key, then print this instead

    if len(no_character_found) != 1:
        # make sure the replacement string is only a single character
        raise ValueError('Expected a no_character_found string of length 1.')

    # initialize string to be returned
    hexdumped = ''

    # find the total number of lines that will be printed
    num_lines = math.ceil( len(byte_object) / bytes_per_line )

    for line in range(num_lines):

        # find the bytes correseponding to the current line
        partial_bytes = byte_object[line*bytes_per_line:(line+1)*bytes_per_line]

        # turn the bytes into a printable string, add it on to the string that 
        # will be returned, with a newline as seperation
        hexdumped += make_line_string(
            line, partial_bytes, bytes_per_line, column_break_spacing, no_character_found
        ) + '\n'

    # when returning, remove the last newline 
    return hexdumped[:-1]


# takes in a number of bytes, returns a printable string
def make_line_string(
    line_number: int, partial_packet: bytes, bytes_per_line: int, column_break_spacing: int, no_character_found: str
):
    # return: row, example:
    # 0010:  08 06 00 01 08 00 06 04  00 01 B8 27 EB 3C 2D 60  ___________'_<-`
    #
    # input: 
    # line_number (represented by the 0010), represents the index (in 
    # hex) of bytes on each row, the program multiples the line_number by the 
    # bytes per line to display correctly (for 0010, input 1 instead of 16)
    #
    # input:
    # partial packet - the bytes to be printed
    #
    # input:
    # bytes_per_line - the number of bytes expected to be printed per line.
    # this in case the last line is not the same length as the others, the 
    # ascii decoding will still be printed inline, example:
    # 00B0:  61 74 20 4D 61 6E 6F 61  2E 00 00 00 00 00 00 00  at Manoa._______
    # 00C0:  00 00 00 00 00 00 00                              _______
    # 
    # input:
    # column_break_spacing - how many bytes to be printed until an extra space 
    # is printed for a visual break
    #
    # input:
    # no_character_found - if the ascii representation is not a standard
    # keyboard key, then print this instead

    if len(no_character_found) != 1:
        # make sure the replacement string is only a single character
        raise ValueError('Expected a no_character_found string of length 1.')

    # initialize placeholder variables
    bytes_characters = ''
    ascii_characters = ''
    column = 0

    for byte in partial_packet:
        # each byte will be an integer from 0-255 (type: int)
        
        # if the current column is a multiple of column_break_spacing
        if column % column_break_spacing == 0:
            # add an extra space for a visual break
            bytes_characters += ' '
        column += 1

        # {:02X} decoded: 
        # 0 -> zero fill
        # 2 -> 2 characters wide
        # X -> represent integer as a hex number with capital letters
        bytes_characters += ' {:02X}'.format(byte)

        # 32 through 126 are ascii encondings for common keyboard keys
        if byte >= 32 and byte <= 126:
            # if the byte is a common keyboard key, add it to the ascii 
            # representation of the bytes
            ascii_characters += chr(byte)
        else:
            # if it isn't, add the default character
            ascii_characters += no_character_found

    
    # once the for loop is done, example values:
    # bytes_characters = '  61 74 20 4D 61 6E 6F 61  2E 00 00 00 00 00 00 00'
    # ascii_characters = 'at Manoa._______'
    line_format = '{line_num:04X}:{hex_chars:{width}}  '

    # the width variable allows for keeping the ascii characters in line with 
    # previous rows
    # int() rounds down to nearest whole number
    row = line_format.format(
        line_num = line_number*bytes_per_line,
        hex_chars = bytes_characters, 
        width = int(bytes_per_line*(3 + 1/column_break_spacing))
    )
    row + ascii_characters
    return row
