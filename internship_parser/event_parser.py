import requests
from bs4 import BeautifulSoup

url = 'https://www.python.org/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

events = soup.find('div', class_='medium-widget event-widget last').select('li')

prefix = 'https://www.python.org'
print('Upcoming events:')

for event in events:
    print(event.text)
    print(f"{prefix + event.find('a').get('href')}")
