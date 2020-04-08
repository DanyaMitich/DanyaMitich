import requests
import json

main_link = 'https://api.github.com/users/'
username = input('Name: ')

repos = requests.get(f'{main_link}{username}/repos')
print(repos.text)

for repo in repos.json():
   if not repo['private']:
       print(repo['html_url'])