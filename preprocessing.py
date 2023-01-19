import pandas as pd
import re
import numpy as np

def load_data():
    df = pd.read_excel('./files/data.xlsx')
    return df

def data_preprocessing(df):
    vacancy_list = ['менеджер', 'водитель', 'бухгалтер', 'администратор', 'управляющий', 'продавец', 'диспетчер',
                    'дизайнер', 'оператор', 'сборщик']
    def convert_vac(string, vacancy_list):
        for i in vacancy_list:
            if i in string.lower():
                return i
    df['Категория'] = df['Название вакансии'].apply(lambda x: convert_vac(x, vacancy_list))
    df = df.fillna('другое')
    df.rename(columns={'Unnamed: 0': 'Ссылка на вакансии'}, inplace=True)

    # search for minimum wage
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

def main():
    df = load_data()
    data_preprocessing(df)

if __name__ == '__main__':
    main()