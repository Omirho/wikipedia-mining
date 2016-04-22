import xml.etree.ElementTree as ET
import dateutil.parser as dp
from datetime import datetime, timedelta
import pickle

nsmap = {}
userEdits = {}
idToName = {}

def fixtag(ns, tag):
    return '{' + nsmap[ns] + '}' + tag

def insert_userEdit(userid, dt):
    if userid not in userEdits:
        userEdits[userid] = []
    userEdits[userid].append(dt)

def process(elem):
    dt = dp.parse(elem.find(fixtag('','timestamp')).text)
    dt += timedelta(hours=5, minutes=30)
    usern = (elem.find(fixtag('','contributor'))).find(fixtag('','username'))
    i_d = (elem.find(fixtag('','contributor'))).find(fixtag('','id'))
    if i_d != None:
        ii = int(i_d.text)
        idToName[ii] = usern.text
        insert_userEdit(ii, dt)


i = 0
for event, elem in ET.iterparse('hiwiki-20160305-stub-meta-history.xml', events=('end', 'start-ns')):
    if event == 'start-ns':
        ns, url = elem
        nsmap[ns] = url
    if event == 'end':
        if elem.tag == fixtag('', 'revision'):
            i += 1
            if i%10000 == 0:
                print i
            process(elem)
            elem.clear()
print i

for t in userEdits.keys():
	userEdits[t].sort()

f1_name = '_hi_userEditsPickle.pkl'
f2 = open('hi_idToNamePickle.pkl', 'wb')

pickle.dump(idToName, f2, -1)

count = 0
temp_list = []
item_list = userEdits.items()
ic = 1
for t in item_list:
    count += len(t[1])
    temp_list.append(t)
    if count >= 100000:
        print ic, count
        count = 0
        f = open("pickled/" + str(ic) + f1_name, 'wb')
        pickle.dump(temp_list, f, -1)
        ic += 1
        temp_list = []
        f.close()

if count > 0:
	print ic, count
	f = open("pickled/" + str(ic) + f1_name, 'wb')
	pickle.dump(temp_list, f, -1)
	ic += 1
	temp_list = []
	f.close()

f2.close()