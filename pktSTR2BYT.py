def pktSTR2BYT(given_string):
    list_of_bytes = given_string.replace('"\n','').replace("'",'').replace('i','')
    list_of_bytes = list(list_of_bytes.split('\\x')).pop(0)
    byte_array = bytes([int(list_of_bytes[x],base = 16) for x in range(len(list_of_bytes))])
    return byte_array



    


    
    

