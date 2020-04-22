import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from pymongo import MongoClient

work = 'сварщик' #input('Введите вакансию для поиска сотрудника： ')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
url = 'https://hh.ru'

#1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД
client = MongoClient('localhost',27017)
db = client['newdb']
resume = db.resume    #

res_final = [] #выводить в эксель для сотрудника службы персонала
for i in range(1):
    main_link = f'{url}/search/resume?area=&clusters=true&exp_period=all_time&logic=normal&pos=full_text&from=employer_index_header&from=suggest_post&text={work}&page={i}'   #f'{url}/search/vacancy?area=&st=searchVacancy&text={work}&page={i}'
    hh_data = requests.get(main_link, headers=headers).text
    soup = bs(hh_data,'lxml')

    resume_block = soup.find_all('div', {'data-qa': 'resume-serp__resume'})
    for res in resume_block:
        resume_data = {}
        data_1 = res.find('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'})
        res_href = data_1.findChild()['href']
        resume_data['name'] = data_1.getText().replace('\xa0','')
        resume_data['test_name'] = ((resume_data['name'].lower()).count(work.lower())>0)
        resume_data['link'] = url + data_1.findChild()['href'] #vac_href
        link_1 = resume_data['link']

        data_2 = res.find('div', {'class': 'resume-search-item__compensation'})
        salary = data_2.getText().replace('\xa0', ' ').split()
        if len(salary)>0:
            if salary[-2] == 'бел.':
                resume_data['salary'] = int(''.join(salary[:-2]))
                resume_data['currency'] = ''.join(salary[-2:])
            else:
                resume_data['salary'] = int(''.join(salary[:-1]))
                resume_data['currency'] = salary[-1]

        data_4 = res.find('div', {'class': 'resume-search-item__fullname'})
        resume_data['age'] = data_4.getText().replace('\xa0',' ')

        data_5 = res.find('span', {'class': 'resume-search-item__date'})
        resume_data['last_change'] = data_5.getText().replace('\xa0','')

        resume_data['id'] = soup.find('div', {'class': 'resume-search-item'})['data-resume-id']

        res_final.append(resume_data)

        # 3*)Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта
        if resume.count_documents({'link': link_1}):
            print('exists')
        else:
            resume.insert_one(resume_data)

print(len(res_final))
hh_data = pd.DataFrame(res_final)
hh_data.to_csv(f'hh_data_resume_{work}' + ".csv", sep=';', index=False, encoding='utf-8')

for res in resume.find({}):
    pprint(res)

print(resume.count_documents({}))

#2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
level = int(input('Введите нижний порог зарплаты для отбора (число)：'))
for res in resume.find({'salary' : {'$gt': level}, 'currency' : 'руб.'}):
    pprint(res)

