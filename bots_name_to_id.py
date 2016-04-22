import pickle

f = open('hi_bots.txt', 'r')

# bots = [i.encode('UTF-8') for i in f.read().splitlines()]
bots = f.read().splitlines()

f.close()

f = open('pickled/hi_idToNamePickle.pkl', 'rb')

idToName = pickle.load(f)

f1 = open('hi_bots_number.txt', 'w')
f2 = open('hi_bots_names.txt', 'w')

for i, n in idToName.items():
	for j in bots:
		s = j.decode('UTF-8')
		if n == s:
			f1.write(str(i) + '\n')
			f2.write(j +'\n')
			break

f.close()
f1.close()