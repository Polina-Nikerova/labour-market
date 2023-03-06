import pandas as pd
import re
import numpy as np
from collections import Counter

# Uploading data
def load_data(file_name):
    df = pd.read_excel(f'./files/{file_name}.xlsx')
    return df

def data_preprocessing(df):
    # Creating a list of "vacancy categories" to group different vacancy titles
    vacancy_list = ['менеджер', 'водитель', 'бухгалтер', 'администратор', 'управляющий', 'продавец', 'диспетчер',
                    'дизайнер', 'оператор', 'сборщик', 'охранник', 'developer', 'рабочий', 'руководитель', 'юрист',
                    'секретарь', 'официант', 'экономист', 'инженер', 'наборщик', 'продавец', 'редактор', 'аналитик']
    # Checking if the vacancy title contains any of the categories and creating a new column "Category"
    def convert_vac(string, vacancy_list):
        for i in vacancy_list:
            if i in string.lower():
                return i
    df['Категория'] = df['Название вакансии'].apply(lambda x: convert_vac(x, vacancy_list))
    df['Категория'] = df['Категория'].fillna('другое')
    df.rename(columns={'Unnamed: 0': 'Ссылка на вакансии'}, inplace=True)

    # Searching for minimum wage
    def find_wage_min(x):
        pattern_wage = re.compile(r'\d+')
        wages = re.findall(pattern_wage, x)
        if len(wages) < 2 and len(wages) != 0:
            wages = wages[0]
            return wages
        elif len(wages) >= 2:
            wages = wages[0]
            return wages
        else:
            return None

    df['wage_min'] = df['Заработная плата'].apply(lambda x: find_wage_min(x))

    # Searching for maximum wage
    def find_wage_max(x):
        pattern_wage = re.compile(r'\d+')
        wages = re.findall(pattern_wage, x)
        if len(wages) < 2 and len(wages) != 0:
            wages = wages[0]
            return wages
        elif len(wages) >= 2:
            wages = wages[-1]
            return wages
        else:
            return None

    df['wage_max'] = df['Заработная плата'].apply(lambda x: find_wage_max(x))

    # Calculating average salary for each vacancy
    def find_wage_av(x):
        pattern_wage = re.compile(r'\d+')
        wages = re.findall(pattern_wage, x)
        if len(wages) > 0:
            wages = [float(i) for i in wages]
            wage_av = np.mean(wages)
            return wage_av
        else:
            return None

    df['wage_av'] = df['Заработная плата'].apply(lambda x: find_wage_av(x))

    df.to_excel('./files/data_preprocessing.xlsx')

    def frequency_skills(df_skills):
        df_skills = df.groupby('Категория')['Навыки'].sum()
        df_skills = pd.DataFrame(df_skills)
        df_skills = df_skills.reset_index()
        df_skills['Навыки'] = df_skills['Навыки'].apply(lambda x: x.lower().strip().split('/'))
        df_skills['Навыки'] = df_skills['Навыки'].apply(lambda x: [i.strip() for i in x])
        df_skills['Навыки_частота'] = df_skills['Навыки'].apply(lambda x: Counter(x))
        column_skills = []
        df_skills['Навыки_частота'].apply(lambda x: column_skills.extend(list(x.keys())))
        column_skills = list(set(column_skills))
        column_skills = [i for i in column_skills if i != '']
        for column in column_skills:
            df_skills[column] = df_skills['Навыки_частота'].apply(lambda x: x[column] if column in x.keys() else None)
        df_skills.drop(['Навыки_частота', 'Навыки'], axis=1, inplace=True)
        df_skills.to_excel('./files/frequency_skills.xlsx', index=False)

    frequency_skills(df)

def main():
    df = load_data()
    data_preprocessing(df)

if __name__ == '__main__':
    main()