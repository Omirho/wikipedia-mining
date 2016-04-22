from collections import Counter
import xml.etree.ElementTree as ET

f1 = open('userEditCount1.txt', 'w')
f2 = open('userEditCount2.txt', 'w')
f3 = open('userEditCount_only.txt', 'w')

nsmap = {}
userCount = Counter()
idToName = {}

def fixtag(ns, tag):
    return '{' + nsmap[ns] + '}' + tag

i = 0
for event, elem in ET.iterparse('hiwiki-20160203-stub-meta-history.xml', events=('end', 'start-ns')):
    if event == 'start-ns':
        ns, url = elem
        nsmap[ns] = url
    if event == 'end':
        if elem.tag == fixtag('', 'revision'):
            i += 1
            if i%10000 == 0:
                print i
                
            usern = (elem.find(fixtag('','contributor'))).find(fixtag('','username'))
            i_d = (elem.find(fixtag('','contributor'))).find(fixtag('','id'))
            ip = (elem.find(fixtag('','contributor'))).find(fixtag('','ip'))

            if(i_d != None):
                ii = int(i_d.text)
                idToName[ii] = usern.text
                userCount[ii] += 1
            elif(ip != None):
                userCount[ip.text] += 1

            elem.clear()
print i

a = userCount.items()
a.sort()

b = idToName.items()
b.sort()

for k in a:
    f1.write(str(k[0]) + " " + str(k[1]) + "\n")
    f3.write(str(k[1]) + '\n')

for k in b:
    f2.write(str(k[0]) + " " + k[1].encode("UTF-8") + "\n")
    
f1.close()
f2.close()
f3.close()
