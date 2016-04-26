from datetime import datetime, timedelta
import pickle

session_gap = timedelta(hours=1)



# Reconstruction start

f1_name = '_hi_userEditsPickle.pkl'
f_name = '_hi_userSessionsPickle.pkl'
pickled_file_number = 19


def list_to_session(l):
	session_list = []
	curr_session = []
	curr_session.append(l[0])
	for i in xrange(1, len(l)):
		if (l[i] - curr_session[-1]) > session_gap:
			session_list.append(curr_session)
			curr_session = []
		curr_session.append(l[i])

	session_list.append(curr_session)
	return session_list

for i in xrange(1, pickled_file_number+1):
	userEdits = {}
	f = open("pickled/edits/" + str(i) + f1_name, 'rb')
	tmp_list = pickle.load(f)
	for t in tmp_list:
		l = list_to_session(t[1])
		userEdits[t[0]] = l
	f.close()

	item_list = userEdits.items()
	f = open("pickled/sessions/" + str(i) + f_name, 'wb')
	pickle.dump(item_list, f, -1)
	f.close()

# Reconstruction end