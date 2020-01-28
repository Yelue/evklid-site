import re

from app import app
from app import db,lm

from flask import request,render_template,redirect,\
				  url_for,json,session
from flask_login import login_user, logout_user, current_user,\
						login_required

from app import tasks

from app.config_data import *

from app.forms import *




@lm.unauthorized_handler
def unauthorized():
	'''if user not autorized render oops.html'''
	return render_template('oops.html')

@app.route('/index',methods=['GET'])
@app.route('/',methods=['GET'])
@login_required
def index():
	'''get results if it exists and render index.html'''
	if 'search_results' in session:
		results = session.get('search_results')
	else:
		results = []
	
	return render_template('index.html',specs = specs_server,
						 regions = regions_server,
						 results= results,
						 names_head_table_result=names_head_table_result
						 )


@app.route('/register', methods=['GET','POST'])
def register():
	'''register user'''
	#make form
	form = RegisterForm(request.form)
	#check if data correct to register
	if request.method == 'POST' and form.validate():
		
		tasks.register_user(form)
		
		return redirect(url_for('login'))

	return render_template('register.html',form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	'''signin user in system'''
	#check if user login redirect to index.html
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	#make a login form
	form = LoginForm()
	#check if correct data to login
	if form.validate_on_submit():

		user = tasks.signin_user(form)
	
		if user:
			login_user(user, remember=form.remember_me.data)
	
			return redirect(url_for('index'))
		else:
	
			return render_template(
									'login.html',
									title='Sign In', 
									form=form,
									message='invalid email or password'
									)
	
	return render_template(
							'login.html', 
							title='Sign In', 
							form=form,message=False
							)


@app.route('/logout')
def logout():
	'''logout user'''
	logout_user()

	return redirect(url_for('login'))


@app.route('/user_page')
@login_required
def user_page():
	#get all user's choices from users_basket
	user_basket = tasks.get_user_basket(current_user.email)
	#make fieldnames for basket table
	keys_basket = list(user_basket[0].keys()) if user_basket else []
	#get all user's subjects
	subjects_user = tasks.get_user_subjects(current_user.email)
	#get list of recommendation specialtys
	user_recom = tasks.get_user_recom(current_user.email)
	#make fieldnames for recommendations table
	keys_recom = list(user_recom[0].keys()) if user_recom else []

	return render_template('user_page.html',rows_basket=user_basket,
											keys_basket= keys_basket,
											subjects_user = subjects_user,
											subjects_name=subjects_name,
											rows_recom = user_recom,
											keys_recom = keys_recom,
											specs = specs_server,
						 					regions = regions_server)


@app.route('/recommend', methods=['GET','POST'])
def recommend():

	
	#make recommendation list and save into table 
	tasks.make_recommendation(request.form,current_user.email)
	
	return redirect(url_for('user_page'))


@app.route('/start_search',methods=['POST'])
def start_search():
	'''search specialty '''
	#get form
	form = request.form
	#call search function and get results
	results = tasks.search_specialty(form)
	
	#add to session results
	if 'search_results' in session:
		session.pop('search_results',None)	

		session['search_results'] = results
	else:
		session['search_results'] = results

	#add query to table user's_query_search
	tasks.add_query_search(
							current_user.email,
							form['region'],
							form['year'],
							form['univer']
							)
	
	#redirect to index.html 
	return redirect(url_for('index'))


@app.route('/add_to_basket',methods=['POST','GET'])
def add_to_basket():
	'''add to basket choosen specialty by user'''
	tasks.add_subj_to_basket(
								current_user.email,
								request.form['keys_r'],
								request.form['text']
								)
	
	return 'Done'


@app.route('/delete_score', methods=['POST','GET'])
def delete_score():
	''' delete user's subject '''
	#get subject name and subject score
	subject_name = request.form['subject_name'].strip()
	subject_score = request.form['subject_score'].strip()
	#delete this subject from table users_scores
	tasks.delete_subject(current_user.email,subject_name,subject_score)
	
	return '200'


@app.route('/delete_choice', methods=['POST','GET'])
def delete_choice():
	'''function delete choosen specialty from users's basket '''
	tasks.del_choice(request.form,current_user.email)
	

	return '200'


@app.route('/add_to_users_score',methods=['POST','GET'])
def add_to_users_score():
	'''function add user's subject, subject name and subject score, to table users_scores '''
	#get subject name and subject score
	subject_name = request.form['subject_name']
	subject_score = request.form['subject_score']
	tasks.add_user_subj(current_user.email,subject_name,subject_score)

	return '200'
@app.route('/make_list',methods=['POST'])
def make_list():
	'''make and return list of region's universities '''
	#get from form user's region
	post_region = request.form['post_region']
	#get list of universities in this region
	answer = tasks.real_make_list(post_region)
	
	return answer



