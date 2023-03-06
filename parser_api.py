import numpy as np
import requests
from bs4 import BeautifulSoup
import lxml
import time
import pandas as pd
from collections import Counter
import random
import re
import json
from CRUD import insert_base_table
import numpy as np

def get_links_api(amount_vacancy, page, area):
    # Работа с апи
    # Справочник для параметров GET-запроса
    params = {
        # 'text': 'NAME:Аналитик', # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': area,  # Поиск осуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'per_page': amount_vacancy  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API

    import json
    data = json.loads(req.text)

    data = data['items']

    list_final = []

    for i in data:
        list_final.append(i['url'])

    return list_final

def get_data_api(list_final):

    session = requests.Session()

    count = 0

    for link in list_final:

        count = count + 1
        if count == 9:
            time.sleep(60)
            count = 0

        try:
            req = session.get(link)
        except Exception as ex:
            print('Error')
            time.sleep(random.uniform(30, 60))
            continue

        time.sleep(random.uniform(1.5, 3.5))
        if req.status_code == 200:
            print('Count - ', count)
            print('Work - ', link)
            data = json.loads(req.text)
            name = data['name']

            description = data['description']
            description_soup = BeautifulSoup(description, 'lxml')
            description_soup = description_soup.text

            salary = data['salary']
            if salary:  # не пусто
                salary_from = salary.get('from')
                salary_to = salary.get('to')
            else:
                salary_from = None
                salary_to = None

            skills = data['key_skills']
            skills = [j for i in skills for j in i.values()]
            skills = ','.join(skills)

            insert_base_table(name, salary_from, salary_to, description_soup, skills)
            print('Add row')
        else:
            print('Error')
def get_vacancy(df):

    vacancy_list = ['менеджер', 'водитель', 'бухгалтер', 'администратор', 'управляющий', 'продавец', 'диспетчер',
                    'дизайнер', 'оператор', 'сборщик', 'охранник', 'developer', 'разработчик', 'рабочий', 'руководитель',
                    'юрист', 'секретарь', 'официант', 'экономист', 'инженер', 'наборщик', 'продавец', 'редактор', 'аналитик',
                   'тестировщик']

    def convert_vac(string, vacancy_list):
        for i in vacancy_list:
            pattern_vacancy = fr'\b{i}\b'
            check_exists = re.findall(pattern_vacancy, string.lower())
            if len(check_exists) > 0:
                return i

    df['vacancy_category'] = df['vacancy_name'].apply(lambda x: convert_vac(x, vacancy_list))
    category = df['vacancy_category'].value_counts()

    df = df.fillna('другое')

    return df
def skills_frequency(df):

    df_skills = df.groupby('vacancy_category')['skills'].sum()
    df_skills = pd.DataFrame(df_skills)
    df_skills = df_skills.reset_index()

    df_skills['skills'] = df_skills['skills'].apply(lambda x: x.split(',') if x is not None or x != np.nan else x)
    df_skills['skills_frequency'] = df_skills['skills'].apply(lambda x: Counter(x))

    column_skills = []
    df_skills['skills_frequency'].apply(lambda x: column_skills.extend(list(x.keys())))
    column_skills = list(set(column_skills))
    column_skills = [i for i in column_skills if i != '']

    for column in column_skills:
        df_skills[column] = df_skills['skills_frequency'].apply(lambda x: x[column] if column in x.keys() else None)

    df_skills.drop(['skills_frequency', 'skills'], axis=1, inplace=True)

    return df_skills

def main_parser(amount_vacancy, area, max_page):
    bag_of_links = []
    for page in range(1, max_page):
        print('Working with page', page)
        list_links = get_links_api(amount_vacancy, page, area)
        bag_of_links.extend(list_links)
    get_data_api(bag_of_links)