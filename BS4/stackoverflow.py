import json
import requests
from bs4 import BeautifulSoup

url = 'https://stackoverflow.com/questions?tab=newest&page='

def filter(value):
  return value.text \
        .replace('questions','') \
        .replace(' ','') \
        .replace(',','') \
        .replace('\t','') \
        .replace('\n','') \
        .replace('\r','')
                  

def fetch(pageNumber):
  try:
    response = requests.get(url + str(pageNumber))
    maxPageNumber = crawl(response)
  except requests.exceptions.ConnectionError:
    print('exception')

  return maxPageNumber


def crawl(response):
  content = BeautifulSoup(response.text, 'lxml')
  links = content.findAll('a', {'class': 'question-hyperlink'})
  descriptions = content.findAll('div', {'class': 'excerpt'})
  parse(links, descriptions)

  questionNumber = filter(content.find('div', {'class': 'fs-body3 flex--item fl1 mr12 sm:mr0 sm:mb12'}))
  return round(int(questionNumber) / 50)


def parse(links, descriptions):
  for i in range(0, len(descriptions)):
    question = {
      'title': links[i].text,
      'url': links[i]['href'],
      'description': descriptions[i].text.replace('\r','').replace('\n','').lstrip().rstrip()
    }
    print(json.dumps(question, indent=2))


maxPageNumber = fetch(1)

for page in range(2, maxPageNumber):
  if page > 2:
    exit()
  _ = fetch(page)