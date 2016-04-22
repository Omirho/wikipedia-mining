import xml.etree.ElementTree as ET
import dateutil.parser as dp
from collections import Counter
from datetime import datetime, timedelta

f1 = open('hi_monthEditCounts.txt', 'w')
f2 = open('hi_weekDayEditCounts.txt', 'w')
f3 = open('hi_hourEditCounts.txt', 'w')
f4 = open('hi_editCountsDay.txt', 'w')
f5 = open('hi_editCountsDayWithDays.txt', 'w')

nsmap = {}
dtEditCounter = Counter()
monthEditCounter = Counter()
weekDayEditCounter = Counter()
hourEditCounter = Counter()

def fixtag(ns, tag):
    return '{' + nsmap[ns] + '}' + tag

def process(elem):
    dt = dp.parse(elem.find(fixtag('','timestamp')).text)
    dt += timedelta(hours=5, minutes=30)
    dtEditCounter[dt.date()] += 1
    monthEditCounter[dt.date().month] += 1
    weekDayEditCounter[dt.isoweekday()] += 1
    hourEditCounter[dt.time().hour] += 1

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
            result = process(elem)
            elem.clear()

print i

for e in sorted(monthEditCounter):
	f1.write(str(e) + ' ' + str(monthEditCounter[e]) + '\n')

for e in sorted(weekDayEditCounter):
	f2.write(str(e) + ' ' + str(weekDayEditCounter[e]) + '\n')

for e in sorted(hourEditCounter):
	f3.write(str(e) + ' ' + str(hourEditCounter[e]) + '\n')

for e in dtEditCounter:
	f4.write(str(dtEditCounter[e]) + '\n')

for e in dtEditCounter:
	f5.write(str(e) + ' ' + str(dtEditCounter[e]) + '\n')