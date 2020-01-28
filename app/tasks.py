from app.config_data import dict_reg_uni_id, dict_id_name_uni, regions
from app import parser
from app import models
from passlib.hash import sha256_crypt
import re
from app.db_api import Worker_Db
from app import db


worker_db = Worker_Db(db)

def register_user(form):
	'''register user'''
	#get row from table users	
	user = worker_db.get_row('users',{'email': form.email.data})
	#check if exist user in our database
	if not user:
		#if not add to table users
		worker_db.alter_into_table('users',{
											'email': form.email.data,
											'password': sha256_crypt.encrypt(str(form.password.data)),
											'first_name': form.first_name.data,
											'second_name': form.second_name.data,
											'birthday': form.birthday.data,
											'verified': False	 				
											})		
		
		return True
	else:
		return False

def signin_user(form):
		'''
		function get form, return False if failed sigin,
			return user<class 'app.models.Users'>

		'''
		#get row from table users
		user = worker_db.get_row('users',{'email': form.email.data})
		#check if user exists in table and password the same
		if user is None or not sha256_crypt.verify(form.password.data,user.password):
			
			return False
			
		return user

def del_choice(form,user_email):
	#get year, base, university, faculty and specialty name
	year = form['year'].strip()
	base = form['base'].strip()
	univer = form['univer'].strip()
	faculty = form['faculty'].strip()
	specialty = form['specialty'].strip()
	#delete row with these keys
	worker_db.delete_row('users_basket',{
										'user_email': user_email,
										'year': year,
										'base': base,
										'univer': univer,
										'faculty': faculty
										})
	return True

def add_query_search(user_email,region,year,univer):
	'''function adds search query to table query search'''
	#delete last record in table users_query_search
	try:
		worker_db.delete_row('users_query_search',{'user_email':current_user.email})
	except:
		pass
	#get region name
	region = worker_db.get_row('regions',{'region_id':region}).region_name
	#add oru query to table users_query_search
	worker_db.alter_into_table('users_query_search',{
													'user_email': user_email,
													'year': year,
													'region': region,
													'univer': univer						
													})

	return True
def add_subj_to_basket(user_email,keys,text):
	'''add user's subject to table users_basket '''
	#get keys, they are fielnames of table 
	keys = format_row_tr(keys)
	#get row, prepared for alter into table
	row = format_data_basket(text,keys)
	
	#add user email
	row['user_email'] = user_email
	#alter into table our row
	worker_db.alter_into_table('users_basket',row)

def delete_subject(user_email, subject_name, subject_score):
	'''delete choosen user's subject '''
	rows = worker_db.get_all_rows('users_scores',{'user_email': user_email})
	for row in rows:
		if row.subject == {'subject_name': subject_name,'subject_score': subject_score}:
			worker_db.delete_row('users_scores',{'id':row.id})
			break
	
	return True

def search_specialty(form):
	'''search list of specialties'''
	#get year,specialty,base education, university, region name and id
	post_year = form['year']
	post_spec = form['spec']
	
	if post_year!='2019' and form['osnova']=="Бакалавр (на основі:Повна загальна середня освіта)":
		post_osnova = form['osnova']	
	else:
		post_osnova = 'Бакалавр (на основі:ПЗСО)'

	post_univer = form['univer']
	post_region_id = form['region']
	post_region = worker_db.get_row('regions',{'region_id':post_region_id}).region_name
	#get result from search
	result_search = parser.search(parser.get_url(post_year,post_univer),post_spec,post_osnova)
	#add to each result univer name and region name
	for r in result_search:
		r['univer'] = post_univer
		r['region'] = post_region

	return result_search if result_search else ['Not found']

def make_recommendation(form,user_email):
	'''make recommendation list of specialties'''
	#get all user's subjects
	user_subjects = worker_db.get_all_rows('users_scores',{'user_email':user_email})
	user_subjects = { i.subject['subject_name'] : float(i.subject['subject_score']) for i in user_subjects}
	#get all specialty which fit to our user's choice (region,specialty,osnova)
	all_recom_specialtys = worker_db.get_all_rows(	'region_%s'%form['region'],
													{
														'specialty':form['spec'],
														'base':form['osnova']
													}
												)
	#validate specialty and user's subjects, can we work with them? 
	recom_specialtys = make_list_recom(user_subjects,all_recom_specialtys)
	#make recomendation list
	recom_list = recommendation(user_subjects,recom_specialtys)
	#prepare recom_list for add into table. create answer_list
	answer_list = []
	for i in recom_list:
		answer = {'user_score':i[0],'user_email':user_email,
				'region':form['region']}
		t = i[1]._asdict()
		answer.update({key:t[key] for key in t.keys() if not key in ['id','average_score_contract']})
		
		answer_list.append(answer)
	#delete previous recommendation
	worker_db.delete_row('users_recom_result',{'user_email':user_email})
	#alter new recommendation
	worker_db.alter_into_table_list('users_recom_result',answer_list)

	return True
def add_user_subj(user_email,subject_name,subject_score):
	#alter into table users_scores with primary key, user email
	worker_db.alter_into_table('users_scores',{
											'user_email': user_email,
											'subject': {
														'subject_name' : subject_name,
														'subject_score' : subject_score
														} 
											})
	return {'subject_name':subject_name,'subject_score':subject_score}

def get_user_basket(user_email):
	'''get user's basket of choices and return them '''
	#get all rows(choices) from table 'users_basket'
	rows_basket = worker_db.get_list_dicts_rows(worker_db.get_all_rows('users_basket',{'user_email':user_email}))
	
	for row in rows_basket:
		del row['user_email']
		del row['id']
		#format the competition subjects
		row['competition_subjects'] = format_competition_subjects(row['competition_subjects'])
	
	return rows_basket

def format_competition_subjects(subjects):
	'''format competition subjects and return them'''
	return 'koef'

def get_user_subjects(user_email):
	'''get user's subjects '''
	subjects_user = worker_db.get_all_rows('users_scores',{'user_email':user_email})
	subjects_user = list(map(lambda x: x.subject,subjects_user))

	return subjects_user

def get_user_recom(user_email):
	'''get user's recommendation list '''
	#get all rows(recommend) from table users_recom_result
	subjects_recom = worker_db.get_all_rows('users_recom_result',{'user_email':user_email})
	#prepare a recommend list for show to user
	rows_recom = []
	for i in subjects_recom[:10]:
		t = i._asdict()
		t['univer'] = dict_id_name_uni[t['univer']]
		t['region'] = regions[t['region']]
		t['competition_subjects'] = format_competition_subjects(t['competition_subjects'])
		t['user_score'] = round(float(t['user_score']),4)
		rows_recom.append({key : t[key] for key in t.keys() if not key in ['id','user_email']})

	return rows_recom

def real_make_list(post_region):
	'''generate list of regions names and return them'''
	result = '<option value = ''>Choose univer</option>\n'  
	for uni_id in dict_reg_uni_id[post_region]:
		try:	
			result+='<option value = "{0}">{0}</option>\n'.format(dict_id_name_uni[uni_id])
		except:
			print(uni_id,'error')
			
			continue
	return result

def get_must_option_subj(subj_keys):
	'''find must have subjects and optional subjects in specialty and return them'''
	must_have_subj = subj_keys[:2]
	subj_keys = subj_keys[2:]

	if 'Творчий конкурс' in subj_keys:
		must_have_subj +=['Творчий конкурс']
		subj_keys.remove('Творчий конкурс')
	
	if 'Середній бал документа про освіту' in subj_keys:
		must_have_subj +=['Середній бал документа про освіту']
		subj_keys.remove('Середній бал документа про освіту')

	optional_subj = list(set(subj_keys)-set(must_have_subj))

	return must_have_subj,optional_subj

def validation_recom(users_subjects,competition_subjects):
	'''validate user's subjects and competition subjects of specialty'''
	res = {}
	#iterate in each subject
	for id_key in competition_subjects.keys():
		#find min_score
		if competition_subjects[id_key]['min_score']!='None':
			min_score = float(competition_subjects[id_key]['min_score'].split(' ')[1])
		else:
			min_score = 0.0
		#find koef
		koef = float(competition_subjects[id_key]['koef'].split('=')[1])
		#find subject name
		subject_name = competition_subjects[id_key]['subject_name'].replace(' (ЗНО)','')
		res[subject_name] = [koef, min_score]
	#make list of names of subjects
	subj_keys = list(res.keys())
	#list of names of user's subjects
	user_subj_keys = list(users_subjects.keys())
	#get must have and optional subjects
	must_subj, option_subj = get_must_option_subj(subj_keys)
	#check
	if set(must_subj)&set(user_subj_keys)==set(must_subj):
		
		if set(option_subj)&(set(user_subj_keys)-set(must_subj)):
			return True

		else:
			return False
	else:
		return False


def make_list_recom(user_subjects,all_recom_specialtys):
	''' generate list of user's subjects and validated specialties '''
	res = []
	for i in all_recom_specialtys:
		
		a = validation_recom(user_subjects, i.competition_subjects)
		res.append((a,i))
	return [y for x,y in res if x]

def recommendation(user_subjects,recom_specialtys):
	'''make recommendation list'''
	#create list of user's mean score in each specialty
	users_mean = [calculate_mean_user_score(user_subjects,i.competition_subjects) for i in recom_specialtys]

	#make result list, in which calculate delta user's mean and specialty mean score
	result = {u_score-float(s_score.average_score_budget) : (u_score,s_score) for u_score, s_score in zip(users_mean,recom_specialtys)}
	#sort this list
	keys = list(result.keys())
	keys.sort(reverse=True)

	return [result[key] for key in keys]

def calculate_mean_user_score(user_subjects,competition_subjects):
	'''calculate user's mean score '''
	res = {}
	mean = 0.0
	keys = ['subject_name','koef','min_score']

	for id_key in competition_subjects.keys():
		#find min score specialty koef
		if competition_subjects[id_key]['min_score']!='None':
			min_score = float(competition_subjects[id_key]['min_score'].split(' ')[1])	
		else:
			min_score = 0.0 
		#find koef
		koef = float(competition_subjects[id_key]['koef'].split('=')[1])
		#find subject_name
		subject_name = competition_subjects[id_key]['subject_name'].replace(' (ЗНО)','')
		res[subject_name]={'koef':koef,'min_score':min_score}
	#get names of user's subjects	
	user_subjects_keys = list(user_subjects.keys()) 
	#get names of competion subjects
	subj_keys = list(res.keys())
	#get must have subjects and optional
	must_subj,option_subj = get_must_option_subj(subj_keys)
	#calculate mean
	for subj_name in must_subj:
		if user_subjects[subj_name]<res[subj_name]['min_score']:
			mean = 0.0
			break
		else:
			mean += user_subjects[subj_name]*res[subj_name]['koef']
			
	if mean:
		for subj_name in set(option_subj)&(set(user_subjects_keys)-set(must_subj)):

			if user_subjects[subj_name]<res[subj_name]['min_score']:
				mean = 0.0
				break
			else:
				mean += user_subjects[subj_name]*res[subj_name]['koef']
			
	return mean


def format_row_tr(text):
	'''format text from tr'''
	text = text.split('\n')
	text = [ i for i in text if re.search('\w',i)]
	text = list(map(lambda x: x.strip(),text))
	return text

def format_data_basket(text,keys):
	'''format data basket'''
	text = format_row_tr(text)

	return {x:y for x,y in zip(keys,text)}