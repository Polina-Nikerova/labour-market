import requests
from bs4 import BeautifulSoup
import lxml
import time
import pandas as pd

def get_links():
    # В список мы будет сохоранять ссылки на вакансии
    list_final = []
    # в цикле указываем количество страниц, по которым будет проходить парсер
    for num in range(1, 2):
        # создаем headers
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1094 Yowser/2.5 Safari/537.36'
        }
        URL = f'https://hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=&area=1905&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={num}&hhtmFrom=vacancy_search_list'
        print('Наша ссылка', URL)
        # Делаем запрос к сайту
        res = requests.get(URL, headers = headers)
        # если сайт дает доступ (200), то продолжаем работу, если нет, то выведет ошибку, которую мы предусмотрели в операторе else
        if res.status_code == 200:
            # создаем объект beautifulsoup
            soup = BeautifulSoup(res.text, 'lxml')
            # находим все элементы по XPATH = //a[@class='serp-item__title']
            # получаем список элементов типа beautifulsoup
            all_links = soup.find_all('a', {'class':'serp-item__title'})
            # чтобы извлечь из них непосредственно ссылки, проходим циклом по списку и при помощи метода get() забираем аттрибут href
            for link in all_links:
                link_1 = link.get('href')
                # добавляем ссылку в общий список
                list_final.append(link_1)
        else:
            print('Error web page')
    return list_final

def get_info(list_final):
    dict_info = {}
    for url_vac in list_final:
        print('Work with link - ', url_vac)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1094 Yowser/2.5 Safari/537.36'
        }
        response = requests.get(url_vac, headers=headers)
        time.sleep(2.5)
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            # //h1[@data-qa='vacancy-title']
            name = soup.find('h1', {'data-qa': 'vacancy-title'}).text
        except:
            print('Name error links - ', url_vac)
            name = None
        try:
            # //span[@data-qa='vacancy-salary-compensation-type-gross']
            salary = soup.find('div', {'data-qa': 'vacancy-salary'}).text.replace('\xa0', '')
        except:
            print('Salary error links - ', url_vac)
            salary = None

        try:
            # //div[@class='vacancy-description']
            describe = soup.find('div', {'class': 'vacancy-description'}).text.replace('\n', '')
        except:
            print('Describe error links - ', url_vac)
            describe = None

        try:
            # //div[@class='bloko-tag bloko-tag_inline']
            skills = soup.find_all('div', {'class': 'bloko-tag bloko-tag_inline'})
            skills_text = ""
            for skill in skills:
                skill = skill.text
                skills_text = skills_text + skill + ' / '
        except:
            print('skills_text error links - ', url_vac)
            skills_text = None

        dict_info[url_vac] = {'Название вакансии': name,
                              'Заработная плата': salary,
                              'Описание работы': describe,
                              'Навыки': skills_text}
    return dict_info

def save_data(dict_info):
    df = pd.DataFrame.from_dict(dict_info, orient='index')
    df.to_excel('./files/data.xlsx')

def main():
    links = get_links()
    dict_info = get_info(links)
    save_data(dict_info)

if __name__ == '__main__':
    main()