import requests
import json
#
#1
url = 'https://api.github.com'
user='Alex87Rt'

r = requests.get(f'{url}/users/{user}/repos')

with open('data.json', 'w') as f:
    json.dump(r.json(), f)

for i in r.json():
    print(i['name'])

#2
# url = 'https://samples.openweathermap.org/data/2.5/weather'
# tk = 'b6907d289e10d714a6e88b30761fae22'
#
# headers = {
#     'Content-Type': 'application/json','Authorization': tk
# }
#
# folder_info = 'Lesson1/resources'
# lesson1 = requests.get(f'{url}{"Lesson1"}')
# lesson1.json()
# lesson1 = requests.get(f'{url}{"Lesson1"}', headers = headers)
# lesson1.json()
# lesson1 = requests.get(f'{url}{folder_info}?path=app:/', headers = headers)
#
# for i in lesson1.json()['_embedded']['items']:
#     print(i['name'])
#
# with open('lesson1.json', 'w') as f:
#     json.dump(lesson1.json(), f)