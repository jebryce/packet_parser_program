def listString2bytes(listString):
    byte_list = []
    list_pkt = listString.split()
    for byte in list_pkt:
        byte_list.append(int(byte))
        
    return bytes(byte_list)

