import pktSTR2BYT, sdnParser, printPKTinfo



'''
data = open('data.txt','r').read().replace('-','').replace('\n\n','\n')
data2 = open('data2.txt','w')
data2.write(data)
'''


pkt_str_list = open('data2.txt','r').readlines()
ct = 0
for pkt_str in pkt_str_list:
    ct += 1
    pkt = pktSTR2BYT.pktSTR2BYT(pkt_str) 
    
    pkt_object = sdnParser.Packet(pkt)

    printPKTinfo.printPKTinfo(pkt_object)