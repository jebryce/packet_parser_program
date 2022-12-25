#   In order to write this parser at home, I needed bytes objects (in the 
# formatting as seen in lab). The easiest way I found to do this was to save 
# the bytes object as a string (using bytes.hex() function) to a text file. 
# There are better ways to do this, but this was for testing only and is 
# not meant for production use.
#
# The sdnParser and printPKTinfo libraries will be used just as 
# they would be in lab, taking in bytes objects
#
# please see each imported library for more information
#
# This is used for testing only
#
from PPP.functions import print_Packet
from PPP.functions import Packet_Parser
from PPP.functions import make_library
from PPP.functions import john_hexdump
import os

# uncomment this make_library function to create files at ~/Documents/PPP/ that 
# contain descriptions for MAC addresses and other data values
# make_library.make_library()



location = 'PPP/library/tests.txt'
packets = open(location,'r').readlines()


# for each line in the text file, 
# ex hex_string = 'ff59a300c763a8f2' (type: string)
for hex_string in packets[2:]:
    os.system('clear')

    # convert the line into it's intended bytes object
    pkt = bytes.fromhex(hex_string)

    # create an object with the packet's information parsed
    Packet = Packet_Parser.Parser(pkt)

    # print the objects information to console
    print_Packet.Printer(Packet)

    # print(john_hexdump.john_hexdump(pkt,32,8,'_'))

    break
    
#     input('Press enter to continue.')
# print('End of file reached.')




