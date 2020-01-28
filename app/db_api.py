from app import models
from passlib.hash import sha256_crypt


class Worker_Db():
	'''class api to postgresql database'''
	def __init__(self,db):

		self.db = db
	
	def alter_into_table(self,table_name,attrs):
		self.db.session.add(models.dict_tables_name[table_name](**attrs))
		self.db.session.commit()
		return True
	
	def alter_into_table_list(self,table_name,list_of_attrs):
		for row in list_of_attrs:
			self.alter_into_table(table_name,row)
			
		return True
	def get_row(self,table_name,keys):
		row = self.db.session.query(models.dict_tables_name[table_name]).filter_by(**keys).first()
		return row

	def delete_row(self,table_name,keys):
		self.db.session.query(models.dict_tables_name[table_name]).filter_by(**keys).delete()
		self.db.session.commit()
		return True

	def delete_row_obj(self,table_name,row):
		row = row._asdict()
		self.db.session.query(models.dict_tables_name[table_name]).filter_by(**row).delete()
		self.db.session.commit()

		return True
	def get_last_row(self,table_name):
		last_row = self.db.session.query(models.dict_tables_name[table_name]).order_by(models.dict_tables_name[table_name].id.desc())[0]
		
		return last_row

	def get_all_rows(self,table_name,keys):
		
		all_rows = self.db.session.query(models.dict_tables_name[table_name].__table__).filter_by(**keys).all()
		
		return all_rows
	
	def get_list_dicts_rows(self,rows):
		res = []
		if rows:	
			for row in rows:
				
				res.append(row._asdict())
				#del res[-1]['_sa_instance_state']
			return list(map(lambda x: x._asdict(),rows)) 
		return []
	
