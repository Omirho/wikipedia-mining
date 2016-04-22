import pickle

pickled_file_number = 19
f_name = '_hi_userSessionsPickle.pkl'
f1_name = '_hi_userSessionsPickle_withoutBots.pkl'

f1 = open('hi_bots_number.txt', 'r')
bots = f1.read().splitlines()
f1.close()

for i in xrange(1, pickled_file_number+1):
	print i
	f = open("pickled/sessions/" + str(i) + f_name, 'rb')
	new_list = []
	tmp_list = pickle.load(f)
	for t in tmp_list:
		if str(t[0]) not in bots:
			new_list.append(t)
	f.close()

	f = open("pickled/sessionsWithoutBots/" + str(i) + f1_name, 'wb')
	pickle.dump(new_list, f, -1)
	f.close()