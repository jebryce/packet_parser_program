def pktSTR2BYT(given_string):
    list_of_bytes = given_string[4:len(given_string)-2]
    list_of_bytes = list(list_of_bytes.split('\\x'))
    i = 0
    while len(list_of_bytes) > i :
        if len(list_of_bytes[i]) > 2:
            for j in range(len(list_of_bytes[i])-2):
                list_of_bytes.insert(i+1+j, str(hex(ord(list_of_bytes[i][2+j])))[2:])
            list_of_bytes[i] = list_of_bytes[i][:2]
        i += 1
    my_bytes = bytes(int(byte, base = 16) for byte in list_of_bytes)
    return my_bytes