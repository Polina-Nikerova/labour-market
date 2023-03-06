import requests
from bs4 import BeautifulSoup
import lxml
import time
import pandas as pd
from collections import Counter

def get_links():
    # Creating an empty list for the links
    list_final = []
    # We specify the number of pages the parser will open to collect the vacancy data
    for num in range(1, 2):
        # Creating headers
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1094 Yowser/2.5 Safari/537.36'
        }
        URL = f'https://hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=&area=1905&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={num}&hhtmFrom=vacancy_search_list'
        print('Наша ссылка', URL)
        # Request to the web site
        time.sleep(5)
        res = requests.get(URL, headers=headers)
        # In case of 200, keep running. If not, print error.
        if res.status_code == 200:
            # Creating a beautifulsoup object
            soup = BeautifulSoup(res.text, 'lxml')
            # Searching for all the elements that meet XPATH = //a[@class='serp-item__title']
            # The BeautifulSoup elements are saved as a list
            all_links = soup.find_all('a', {'class':'serp-item__title'})
            # Using 'get' to take the links
            for link in all_links:
                link_1 = link.get('href')
                # Forming a list of links
                list_final.append(link_1)
        else:
            print('Error web page')
    return list_final

def get_info(list_final):
    # Creating an empty dictionary
    dict_info = {}
    # In the next loop each is opened and specific information from the vacancy page is taken
    for url_vac in list_final:
        print('Work with link - ', url_vac)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1094 Yowser/2.5 Safari/537.36'
        }
        response = requests.get(url_vac, headers=headers)
        time.sleep(6)
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            # An html code for the vacancy name //h1[@data-qa='vacancy-title']
            name = soup.find('h1', {'data-qa': 'vacancy-title'}).text
        except:
            print('Name error links - ', url_vac)
            name = None
        time.sleep(6.1)
        try:
            # An html code for salary //span[@data-qa='vacancy-salary-compensation-type-gross']
            salary = soup.find('div', {'data-qa': 'vacancy-salary'}).text.replace('\xa0', '')
        except:
            print('Salary error links - ', url_vac)
            salary = None
        time.sleep(6.2)
        try:
            # An html code for the vacancy description //div[@class='vacancy-description']
            describe = soup.find('div', {'class': 'vacancy-description'}).text.replace('\n', '')
        except:
            print('Describe error links - ', url_vac)
            describe = None
        time.sleep(6)
        try:
            #  An html code for the list of skills //div[@class='bloko-tag bloko-tag_inline']
            skills = soup.find_all('div', {'class': 'bloko-tag bloko-tag_inline'})
            skills_text = ""
            for skill in skills:
                skill = skill.text
                skills_text = skills_text + skill + ' / '
        except:
            print('skills_text error links - ', url_vac)
            skills_text = None

        # Adding Vacancy name, Salary, Description and the List of skills to the dictionary with links as key values
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