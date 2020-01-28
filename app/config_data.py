#all useful data 
from app.models import load_data_db


#list with head names of table HTML
names_head_table_result =['year','univer','region','faculty', 'specialty', 'base', 
			'number_budget', 'number_contract', 
			'number_all_places', 'number_applications', 
			'competition_subjects', 'average_score_budget']
keys_basket = ['faculty', 'specialty', 'base', 
			'number_budget', 'number_contract', 
			'number_all_places', 'number_applications', 
			'competition_subjects', 'average_score_budget']
subjects_name =['Українська мова та література',
				'Математика',
				'Фізика',
				'Хімія',
				'Іноземна мова',
				'Історія України',
				'Географія',
				'Біологія',
				'Середній бал документа про освіту',
				'Бал за успішне закінчення підготовчих курсів закладу освіти']

specs_server = load_data_db('specials')#list of named tuples specialties, id and name
regions_server = load_data_db('regions')#list of named tuples regions, id and name
regions = {region.region_id:region.region_name for region in regions_server}
# dict of university id(key) and university name
dict_id_name_uni = {elem.univer_id: elem.univer_name for elem in load_data_db('univers')}

# dict of region id(key) and university id
dict_reg_uni_id = { i :[] for i in [r.region_id for r in regions_server]}
for elem in load_data_db('reg_uni'):
	dict_reg_uni_id[elem.region_id] += [elem.univer_id] 