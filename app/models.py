from app import db, lm
from flask_login import UserMixin



class region_db(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer,primary_key=True)
	univer = db.Column(db.String())
	year = db.Column(db.String(100))
	faculty = db.Column(db.String())
	base = db.Column(db.String())
	specialty = db.Column(db.String())
	number_budget = db.Column(db.String(100))
	number_contract = db.Column(db.String(100))
	number_all_places = db.Column(db.String(100))
	number_applications = db.Column(db.String(100))
	competition_subjects = db.Column(db.JSON)
	average_score_budget = db.Column(db.String(100))
	average_score_contract = db.Column(db.String(100))


class Users(UserMixin,db.Model):

	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100),unique=True, nullable=False)
	password = db.Column(db.String(100),nullable=False)
	first_name = db.Column(db.String(100))
	second_name = db.Column(db.String(100))
	birthday = db.Column(db.Date)
	verified = db.Column(db.Boolean,nullable=False)
	

	def __repr__(self):
		return '<User %r>'%(self.email)

class Users_Basket(db.Model):
	__tablename__ = 'users_basket'
	id = db.Column(db.Integer, primary_key=True)
	user_email = db.Column(db.String(100), nullable=False)
	year = db.Column(db.String(100))
	univer = db.Column(db.String())
	region = db.Column(db.String(100))
	faculty = db.Column(db.String(100))
	specialty = db.Column(db.String(100))
	base = db.Column(db.String(100))
	number_budget = db.Column(db.String(100))
	number_contract = db.Column(db.String(100))
	number_all_places = db.Column(db.String(100))
	number_applications = db.Column(db.String(100))
	competition_subjects = db.Column(db.JSON)
	average_score_budget = db.Column(db.String(100))
	user_score = db.Column(db.String(100))

class Users_Query_Search(db.Model):
	__tablename__ = 'users_query_search'
	id = db.Column(db.Integer, primary_key=True)
	user_email = db.Column(db.String(100))
	year =  db.Column(db.String(100))
	region =  db.Column(db.String(100))
	univer =  db.Column(db.String())
	search_response =  db.Column(db.String())

class Regions(db.Model):
	__tablename__ = 'regions'
	region_id = db.Column(db.String(100),primary_key=True)
	region_name = db.Column(db.String(500), nullable=False)

class Users_Scores(db.Model):
	__tablename__ = 'users_scores'
	id = db.Column(db.Integer, primary_key=True)
	user_email = db.Column(db.String(100), nullable=False)
	subject = db.Column(db.JSON)

class Users_Recom_Result(db.Model):
	__tablename__ = 'users_recom_result'
	id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.String(100))
	user_email = db.Column(db.String(100), nullable=False)
	univer = db.Column(db.String())
	region = db.Column(db.String(100))
	faculty = db.Column(db.String())
	specialty = db.Column(db.String())
	base = db.Column(db.String(100))
	number_budget = db.Column(db.String(100))
	number_contract = db.Column(db.String(100))
	number_all_places = db.Column(db.String(100))
	number_applications = db.Column(db.String(100))
	average_score_budget = db.Column(db.String(100))
	competition_subjects = db.Column(db.JSON)
	user_score = db.Column(db.String(100))

dict_tables_name = {'users': Users,
					'users_query_search': Users_Query_Search,
					'users_basket': Users_Basket,
					'regions': Regions,
					'users_scores': Users_Scores,
					'users_recom_result': Users_Recom_Result}

def load_data_db(table_name):#takes a table name,return all data[] from table
	table = db.Table(table_name, db.metadata, autoload=True, autoload_with=db.engine)

	return db.session.query(table).all()

def make_regions_models(regions):
	
	
	def make_class(table_name):
		class reg_db(region_db):
			__tablename__ = table_name
		
		return reg_db

	
	return {'region_%s'%key: make_class('region_%s'%key)() for key in regions.keys()}
	
	

@lm.user_loader
def load_user(id):
    return Users.query.get(int(id))
