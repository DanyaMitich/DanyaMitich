import requests
import json
import getpass

#1 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
main_link = 'https://api.github.com/users/'
username = input('Name: ')
password = 'Yagodka85'#getpass.getpass()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

repos = requests.get(f'{main_link}{username}/repos', auth=(username, password))
print(repos.text)

for repo in repos.json():
#   if not repo['private']:
   print(repo['html_url'])

with open("GIT.json", "w") as file:
   file.write(repos.text)

#2. Изучить список открытых API.
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

main_link = 'https://api.hh.ru'
username = 'danyamitich@outlook.com'
password = 'pass4test'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

hh_data = requests.get(f'{main_link}', auth=(username, password))
#with open("hh_data.json", "w") as file:
print(hh_data.text)
