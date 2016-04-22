from datetime import datetime, timedelta
import pickle

pickled_file_number = 19
f_name = '_hi_userSessionsPickle_withoutBots.pkl'
avg_edit_session_addition = timedelta(0)
edit_session_length_by_month = dict()
edit_session_length_by_weekday = dict()
inter_edit_time_list = list()
extended_edit_sessions_history = dict()
labor_hours_history = dict()
rank_list = dict()

def calculate_average_edit_time():
	global avg_edit_session_addition
	edit_count = 0
	edit_duration_total = timedelta()
	for i in xrange(1, pickled_file_number + 1):
		print i
		f = open("pickled/sessionsWithoutBots/" + str(i) + f_name, 'rb')
		tmp_list = pickle.load(f)
		for t in tmp_list:
			for session in t[1]:
				if len(session) > 1:
					for k in xrange(1, len(session)):
						edit_duration_total += session[k] - session[k-1]
						edit_count += 1

		f.close()
	print edit_count, edit_duration_total.total_seconds(), (edit_duration_total.total_seconds()*1.0) / edit_count
	avg_edit_session_addition = timedelta( seconds = (edit_duration_total.total_seconds()*1.0) / edit_count )
	f = open('average_inter_edit_time_across_sessions_withoutBots.txt', 'w')
	f.write('Total inter edit times: ' + str(edit_count) + '\n')
	f.write('Total inter edit times addtion: ' + str(edit_duration_total.total_seconds()) + '\n')
	f.write('Average inter edit times: ' + str((edit_duration_total.total_seconds()*1.0) / edit_count) + '\n')
	f.close()

def average_edit_session_length_by_month(session):
	global edit_session_length_by_month
	startTime = session[0] - avg_edit_session_addition
	iKey = startTime.date().month
	iValue = (session[-1] - startTime).total_seconds()
	if iKey not in edit_session_length_by_month:
		edit_session_length_by_month[iKey] = []
	edit_session_length_by_month[iKey].append(iValue)

def average_edit_session_length_by_weekday(session):
	global edit_session_length_by_weekday
	startTime = session[0] - avg_edit_session_addition
	iKey = startTime.date().isoweekday()
	iValue = (session[-1] - startTime).total_seconds()
	if iKey not in edit_session_length_by_weekday:
		edit_session_length_by_weekday[iKey] = []
	edit_session_length_by_weekday[iKey].append(iValue)

def generate_inter_edit_time_list(l):
	global inter_edit_time_list
	last = l[0][0]
	for i in xrange(1, len(l[0])):
		inter_edit_time_list.append((l[0][i] - last).total_seconds())
		last = l[0][i]

	for i in xrange(1, len(l)):
		for j in l[i]:
			inter_edit_time_list.append((j - last).total_seconds())
			last = j

def monthly_extended_edit_sessions_history(session):
	global extended_edit_sessions_history
	startTime = session[0] - avg_edit_session_addition
	iKey = startTime.date().year, startTime.date().month
	iValue = (session[-1] - startTime).total_seconds()
	if iValue > 10800:
		if iKey not in extended_edit_sessions_history:
			extended_edit_sessions_history[iKey] = 0
		extended_edit_sessions_history[iKey] += 1

def monthly_labor_hours_history(session):
	global labor_hours_history
	startTime = session[0] - avg_edit_session_addition
	iKey = startTime.date().year, startTime.date().month
	iValue = (session[-1] - startTime).total_seconds()
	if iKey not in labor_hours_history:
		labor_hours_history[iKey] = 0
	labor_hours_history[iKey] += iValue

def create_rank_list(t):
	global rank_list
	edits = 0
	total_time = 0
	for i in t[1]:
		total_time += (i[-1] - i[0] + avg_edit_session_addition).total_seconds()
		edits += len(i)
	rank_list[t[0]] = (total_time, edits)

def write_average_edit_session_length_by_month():
	f = open('average_edit_session_length_by_month_withoutBots.txt', 'w')
	for i, l in edit_session_length_by_month.items():
		sum_of_sessions = sum(l)
		average_session_length = sum_of_sessions*1.0 / len(l)
		f.write(str(i) + ' ' + str(average_session_length) + '\n')
	f.close()

def write_average_edit_session_length_by_weekday():
	f = open('average_edit_session_length_by_weekday_withoutBots.txt', 'w')
	for i, l in edit_session_length_by_weekday.items():
		sum_of_sessions = sum(l)
		average_session_length = sum_of_sessions*1.0 / len(l)
		f.write(str(i) + ' ' + str(average_session_length) + '\n')
	f.close()

def write_monthly_extended_edit_sessions_history():
	f = open('monthly_extended_edit_sessions_history_withoutBots.txt', 'w')
	for i in sorted(extended_edit_sessions_history):
		f.write(str(i[0]) + '-' + str(i[1]) + ' ' + str(extended_edit_sessions_history[i]) + '\n')
	f.close()

def write_monthly_labor_hours_history():
	f = open('monthly_labor_hours_history_withoutBots.txt', 'w')
	for i in sorted(labor_hours_history):
		f.write(str(i[0]) + '-' + str(i[1]) + ' ' + str(labor_hours_history[i]) + '\n')
	f.close()

def write_inter_edit_time_list():
	f = open('inter_edit_time_list_withoutBots.txt', 'w')
	for i in inter_edit_time_list:
		f.write(str(i) + '\n')
	f.close()

def write_rank_list():
	l = rank_list.items()
	l.sort(key = lambda x: x[1], reverse = True)
	f = open('editor_ranks_by_duration_withoutBots.txt', 'w')
	for i in l:
		f.write(str(i[0]) + ' ' + str(i[1][0]) + ' ' + str(i[1][1]) + '\n')
	f.close()
	l.sort(key = lambda x: (-x[1][1], -x[1][0]))
	f = open('editor_ranks_by_edits_withoutBots.txt', 'w')
	for i in l:
		f.write(str(i[0]) + ' ' + str(i[1][0]) + ' ' + str(i[1][1]) + '\n')
	f.close()

def process_data(session):
	monthly_extended_edit_sessions_history(session)
	monthly_labor_hours_history(session)
	# average_edit_session_length_by_month(session)
	# average_edit_session_length_by_weekday(session)

def write_data():
	write_monthly_extended_edit_sessions_history()
	write_monthly_labor_hours_history()
	# write_average_edit_session_length_by_month()
	# write_average_edit_session_length_by_weekday()

def process_user(t):
	# generate_inter_edit_time_list(t[1])
	create_rank_list(t)

def write_user():
	# write_inter_edit_time_list()
	write_rank_list()

def session_data_extraction():
	calculate_average_edit_time()
	print 'Data extraction start'
	global pickled_file_number, f_name, avg_edit_session_addition
	for i in xrange(1, pickled_file_number + 1):
		print i
		f = open("pickled/sessionsWithoutBots/" + str(i) + f_name, 'rb')
		tmp_list = pickle.load(f)
		for t in tmp_list:
			process_user(t)
			# for session in t[1]:
			# 	process_data(session)

		f.close()

	# write_data()
	write_user()
	print 'Data extraction end'

session_data_extraction()