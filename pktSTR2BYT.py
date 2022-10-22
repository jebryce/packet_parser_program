def pktSTR2BYT(given_string):
    list_of_bytes = given_string[4:len(given_string)-2]
    list_of_bytes = list(list_of_bytes.split('\\x'))
    for i in range(len(list_of_bytes)):
        if len(list_of_bytes[i]) > 2:
            for j in range(len(list_of_bytes[i])-2):
                list_of_bytes.insert(i+1, str(hex(ord(list_of_bytes[i][2+j:])))[2:])
                list_of_bytes[i] = list_of_bytes[i][:2]
    byte_array = bytes([int(list_of_bytes[x],base = 16) for x in range(len(list_of_bytes))])
    return byte_array