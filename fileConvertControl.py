# meant to be a code history of me converting data sources from internet into 
# library data we can use


# converting ethertype csv to a file with a dict I like 
# (completely personal preference)
'''
EtherTypes_csv = open('EtherType.csv','r').readlines()
EtherTypes = dict()
ranged_EtherTypes = dict()
for line in EtherTypes_csv:
    line = line[:-1]
    line_as_a_list = line.split(',')
    if len(line_as_a_list[0]) == 4:
        EtherTypes[line_as_a_list[0]] = line_as_a_list[1]
    else:
        # maxEtherType = int(line_as_a_list[0][5:],base=16)
        # minEtherType = int(line_as_a_list[0][:4],base=16)
        # dif = maxEtherType-minEtherType
        # for offset in range(dif+1):
        #     newKey = hex(minEtherType+offset)[2:].upper().zfill(4)
        #     print(newKey)
        ranged_EtherTypes[line_as_a_list[0]] = line_as_a_list[1]



EtherType = open('EtherType.py','w')
writeString = ''



writeString += '# Located from:\n'
writeString += '# https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml\n'
writeString += '# Editted to suit our needs.\n\n'
writeString += 'ethertypes = {\n'
for pair in EtherTypes:
    writeString += "\t'"+pair+"':'"+EtherTypes[pair]+"',\n"
writeString += '}'

writeString += '\n\nranged_ethertypes = {\n'
for pair in ranged_EtherTypes:
    writeString += "\t'"+pair+"':'"+ranged_EtherTypes[pair]+"',\n"
writeString += '}'

EtherType.write(writeString)
'''
