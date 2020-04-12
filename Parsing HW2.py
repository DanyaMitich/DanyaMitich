import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

work = input('Введите исследуемую вакансию： ')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
url = 'https://hh.ru'

vac_final = []
for i in range(100):
    main_link = f'{url}/search/vacancy?area=&st=searchVacancy&text={work}&page={i}'
    hh_data = requests.get(main_link, headers=headers).text
    soup = bs(hh_data,'lxml')

    vac_block = soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
    for vac in vac_block:
        vac_data = {}

        data_1 = vac.find('span', {'class': 'g-user-content'})
        vac_href = data_1.findChild()['href']
        vac_data['name'] = data_1.getText().replace('\xa0','')
        vac_data['test_name'] = ((vac_data['name'].lower()).count(work.lower())>0)
        vac_data['link'] = data_1.findChild()['href'] #vac_href

        data_2 = vac.find('div', {'class': 'vacancy-serp-item__sidebar'})
        vac_salary = data_2.getText()
        salary = vac_salary.replace('\xa0', '').split()
        if len(salary)>0:
            if salary[0] == "от":
                vac_data['min_sal'] = salary[1]
                vac_data['currency'] = salary[2]
            elif salary[0] == "до":
                vac_data['max_sal'] = salary[1]
                vac_data['currency'] = salary[2]
            else:
                vac_data['min_sal'] = salary[0].split('-')[0]
                vac_data['max_sal'] = salary[0].split('-')[0]
                vac_data['currency'] = salary[1]

        data_3 = vac.find('div', {'class': 'vacancy-serp-item__meta-info'})
        vac_emp_href = data_3.findChild()['href']
        vac_data['employer'] = data_3.getText().replace('\xa0','') #vac_employer
        vac_data['emp_href'] = url + data_3.findChild()['href'].replace('\xa0','')#vac_emp_href

        data_4 = vac.find('span', {'class': 'vacancy-serp-item__meta-info'}) #bloko-section-header-3
        vac_data['city'] = data_4.getText().replace('\xa0','') #vac_city
        vac_final.append(vac_data)

#pprint(vac_final)
print(len(vac_final))

hh_data = pd.DataFrame(vac_final)
hh_data.to_csv(f'hh_data_{work}' + ".csv", sep=';', index=False)



#https://api.superjob.ru/:version/method_name/:params