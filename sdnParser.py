import pktSTR2BYT
import hexdump
'''
data = open('data.txt','r').read().replace('-','').replace('\n\n','\n')
data2 = open('data2.txt','w')
data2.write(data)
'''

a = open('data2.txt','r').readline()
print(a)

b = pktSTR2BYT.pktSTR2BYT(a)
#print(b)

#hexdump.hexdump(b)
