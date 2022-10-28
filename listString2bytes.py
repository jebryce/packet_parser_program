

def listString2bytes(byte_string):
    byte_list = []
    string_list = byte_string.split()
    for byte in string_list:
        byte_list.append(int(byte))
    return bytes(byte_list)