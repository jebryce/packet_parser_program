# see documentation on control.py file
#
# Used only for testing at home
#
# converts the string 
# "255 89 163 0 199 99 168 242" 
# to a bytes object containing:
# FF 59 A3 00 C7 63 A8 F2
#

def listString2bytes(byte_string):
    byte_list = []

    # string_list is a list of strings, ex ["255", "89", "163"]
    string_list = byte_string.split()

    # for each string, ex: "255", convert it to type int
    for byte in string_list:
        byte_list.append(int(byte))

    # to match data as in lab, return a bytes object
    return bytes(byte_list)