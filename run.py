import pandas as pd

from CRUD import insert_table, get_data_query, insert_vacancy_table, get_vacancy_data, insert_mongo_db, get_data_from_mongodb
from parser_api import get_vacancy, main_parser, skills_frequency
from sqlalchemy import create_engine, select
from models import connection, Base, engine
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
def main():
    df = get_data_query()
    df = get_vacancy(df)
    insert_vacancy_table(df)
def get_data_in_mongodb():
    df = get_vacancy_data()
    df_skills = skills_frequency(df)
    data_dict = df_skills.to_dict()
    vacancy = data_dict.get('vacancy_category')
    del data_dict['vacancy_category']
    final_dict = {}
    for key, value in data_dict.items():
        final_dict[key] = {}
        for key1, value1 in value.items():
            final_dict[key].update({vacancy.get(key1): value1})
    insert_mongo_db(final_dict, table_name)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    amount_vacancy, area, max_page = 100, 1, 2
    table_name = 'skills_frequency'
    #records = get_data_from_mongodb(table_name)
    #df = pd.DataFrame.from_dict(records)
    get_data_in_mongodb()


