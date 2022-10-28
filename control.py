#   In order to write this parser at home, I needed bytes objects (in the 
# formatting as seen in lab). The easiest way I found to do this was to save 
# the bytes object to a text file. There are 100% better ways to do this, but 
# this was for testing only and is not meant for production use.
# 
#   In Lab, I first saved the output of 'print(list(bytes))' to a file, for 
# example: 'listdata.txt'. Then at home, I converted this initial text file to 
# a more usable one using the following code:
"""
listdata = open('listdata.txt','r').read()
listdata.replace(',','').replace('[','').replace(']','')
editted_listdata = open('editted_listdata.txt','w')
editted_listdata.write(listdata)
"""
# This reads the original file, which for example, has multiple (long) lines of 
# strings like:     "[255, 89, 163, 0, 119]"
# then creates a new file, which for example, has multiple (long) lines of 
# strings like:     "255 89 163 0 199"
#
# Then it calls function listString2bytes, which converts the string 
# "255 89 163 0 199 99 168 242" to a bytes object containing:
# FF 59 A3 00 C7 63 A8 F2
#
# After this, the sdnParser and printPKTinfo libraries will be used just as 
# they would be in lab, taking in bytes objects
#
# please see each imported file for more information
#
# This is used for testing only
#
import functions.listString2bytes as listString2bytes
import functions.sdnParser as sdnParser
import functions.printPKTinfo as printPKTinfo


pkt_list = open('editted_listdata.txt','r').readlines()


# for each line in the text file
for byte_string in pkt_list:
    
    # convert the line into it's intended bytes object
    pkt = listString2bytes.listString2bytes(byte_string)
    
    # create an object with the packet's information parsed
    pkt_object = sdnParser.Packet(pkt)

    # print the objects information to console
    printPKTinfo.printPKTinfo(pkt_object)

    break
