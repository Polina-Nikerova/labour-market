import streamlit as st
import numpy as np
import pandas as pd
from millify import prettify
from CRUD import get_vacancy_data
from parser_api import skills_frequency

def web_app():
    st.set_page_config(page_title='Analysis')
    df = get_vacancy_data()
    cols = df.columns.tolist()
    cols.remove('vacancy_category')
    for col in cols:
        df[col] = df[col].apply(lambda x: None if x == 'другое' else x)
    vacancy_id = df['vacancy_category'].unique().tolist()

    select_id = st.sidebar.selectbox('Vacancy category', vacancy_id)

    #if button_analysis:
    def table():
        st.title('Labour market analysis')
        df_to_show = df[df['vacancy_category'] == select_id]

        st.subheader(select_id.capitalize())

        salary_from_list = df_to_show['salary_from'].tolist()
        salary_from_av = np.nanmean(salary_from_list)

        salary_to_list = df_to_show['salary_to'].tolist()
        salary_to_av = np.nanmean(salary_to_list)
        if np.isnan(salary_to_av):
            salary_to_av = 0
        if np.isnan(salary_from_av):
            salary_from_av = 0

        col1, col2 = st.columns(2, gap='small')
        with col1:
            st.metric('Average minimum salary, RUB', prettify(round(salary_from_av)), delta=None, delta_color="normal", help=None, label_visibility="visible")
        with col2:
            st.metric('Average maximum salary, RUB', prettify(round(salary_to_av)), delta=None, delta_color="normal", help=None, label_visibility="visible")

        st.dataframe(df_to_show, width=2200, height=300)
        st.caption('Table 1. Data collected from hh.ru')
        st.title('')


        df_skills = skills_frequency(df)
        df_skills_to_show = df_skills[df_skills['vacancy_category'] == select_id]
        df_skills_to_show = df_skills_to_show.transpose()
        df_skills_to_show = df_skills_to_show.dropna().iloc[1:]
        df_skills_to_show.columns = ['frequency']
        df_skills_to_show = df_skills_to_show.sort_values(by=['frequency'], ascending=False)
        df_skills_to_show.reset_index(inplace=True)
        df_skills_to_show.rename(columns={'index':'skills'}, inplace=True)
        st.dataframe(df_skills_to_show, width=2200, height=300)
        df_skills_plot = df_skills_to_show.copy()
        df_skills_plot.set_index('skills', inplace=True)
        st.caption('Table 2. Skills most frequently mentioned for each category in Table 1')

    def plot():
        df_to_show = df[df['vacancy_category'] == select_id]

        st.subheader(select_id.capitalize())

        df_skills = skills_frequency(df)
        df_skills_to_show = df_skills[df_skills['vacancy_category'] == select_id]
        df_skills_to_show = df_skills_to_show.transpose()
        df_skills_to_show = df_skills_to_show.dropna().iloc[1:]
        df_skills_to_show.columns = ['frequency']
        df_skills_to_show = df_skills_to_show.sort_values(by=['frequency'], ascending=False)
        df_skills_to_show.reset_index(inplace=True)
        df_skills_to_show.rename(columns={'index': 'skills'}, inplace=True)
        df_skills_plot = df_skills_to_show.copy()
        df_skills_plot.set_index('skills', inplace=True)
        st.bar_chart(df_skills_plot)

    button_analysis = st.sidebar.button('Data analysis', on_click=table)
    button_plot = st.sidebar.button('Visual data', key='key', on_click=plot)
