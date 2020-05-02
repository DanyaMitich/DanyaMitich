import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from pymongo import MongoClient
import time
import datetime

work = input('Введите вакансию для поиска сотрудника： ')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
url = 'https://hh.ru'

#1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД
client = MongoClient('localhost',27017)
db = client['newdb']
resume = db.resume

resume.delete_many({})

res_final = []
i = 1
while i>0: #запускаем перелистывание до тех пор, пока не достигнем мах количества страниц, которое получаем как текст предпоследней кнопки (левее кнопки Далее)
    main_link = f'{url}/search/resume?area=&clusters=true&exp_period=all_time&logic=normal&pos=full_text&from=employer_index_header&from=suggest_post&text={work}&page={i}'   #f'{url}/search/vacancy?area=&st=searchVacancy&text={work}&page={i}'
    hh_data = requests.get(main_link, headers=headers).text
    soup = bs(hh_data,'lxml')
    if i == 1: #при проходе первой страницы находим кнопку с номером последней страницы
        page_buttons = soup.find_all('a', {'class': 'bloko-button'})
        length = []
        for p in page_buttons:
            length.append(p.getText())
        max = int(length[-2])

    resume_block = soup.find_all('div', {'data-qa': 'resume-serp__resume'})
    for res in resume_block:
        resume_data = {}
        data_1 = res.find('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'})
        resume_data['link'] = url + data_1.findChild()['href']
        link_1 = resume_data['link']
        if resume.count_documents({'link': link_1}): #если такая ссылку уже есть в базе - дописываем в базу к этому резюме инфо о том, что оно было найдено по запросу от такой-то даты с такой-то вакансией
            print('exists')
            resume.update_one({'link': link_1}, {'$set': {f'{datetime.datetime.today().strftime("%Y%m%d")} поиск': f'{work}'}})
        else:
            #        res_href = data_1.findChild()['href']
            resume_data['name'] = data_1.getText().replace('\xa0','')
            resume_data['test_name'] = ((resume_data['name'].lower()).count(work.lower())>0)

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
            resume_data[f'{datetime.datetime.today().strftime("%Y%m%d")} поиск'] = work

            res_final.append(resume_data)
            resume.insert_one(resume_data)

    if i==max:
        i=0
    else:
        i=i+1

#    i=0
#    print(max)

print(len(res_final))
hh_data = pd.DataFrame(res_final)
hh_data.to_csv(f'hh_data_resume_{work}' + ".csv", sep=';', index=False, encoding='utf-8')

#for res in resume.find({}): #'test_name': {'$in': ['True']}
#    pprint(res)
#print(resume.count_documents({}))

#2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
level = int(input('Введите нижний порог зарплаты для отбора (число)：'))
for res in resume.find({'salary' : {'$gt': level}, 'currency' : 'руб.'}):
    pprint(res)

data_frame = pd.read_csv(f'hh_data_resume_{work}' + ".csv",sep=';')
#print(data_frame)
