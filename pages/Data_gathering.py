import streamlit as st
from CRUD import insert_table, get_data_query, insert_vacancy_table, get_vacancy_data, insert_mongo_db, get_data_from_mongodb
from parser_api import get_vacancy, main_parser, skills_frequency, get_links_api
from sqlalchemy import create_engine, select
from models import connection, Base, engine
import warnings

table_name = 'skills_frequency'
def st_data_gathering():

    st.set_page_config(page_title='Data gathering')

    dict_regions = {
        'Москва': 1,
        'Санкт-Петербург': 2,
        'Севастополь': 3
    }

    select_region_id = st.selectbox('Region', list(dict_regions.keys()))
    select_vacancy_id = st.selectbox('Number of vacancies per page', [i for i in range(10, 101, 10)])
    select_pages_id = st.selectbox('Maximum number of pages', [i for i in range(1, 11)])

    run_button = st.button('Run parser')

    if run_button:
        st.write('Starting parsing...')
        amount_vacancy, area, max_page = select_vacancy_id, dict_regions[select_region_id], select_pages_id
        main_parser(amount_vacancy, area, max_page)
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

st_data_gathering()

