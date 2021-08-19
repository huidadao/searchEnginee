import json
import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com'
data = []


def crawl(url, depth):
  try:
    response = requests.get(url)
  except:
    print(f'Failed to perform HTTP GET request on {url}')
    return

  content = BeautifulSoup(response.text, 'lxml')
  try:
    title = content.find('title').text
    description = [
      tag.text  \
        .replace('\t','') \
        .replace('\n','') \
        .replace('\r','') \
        .replace('\u201c', '')  \
        .replace('\u201d', '')  \
        .replace('\u2764', '')  \
        .replace('\u25be', '')  \
        .replace('\u2019', '')  \
        .replace('\u2015', '')  \
        .replace('\u2026', '')  \
        .replace('\u00ab', '')  \
        .replace('\u00bb', '')  \
        .replace('\u00a9', '')  \
        .replace('\u00d7', '')  \
        .replace('\ud648', '')  \
        .lstrip() \
        .rstrip() \
        for tag in content.findAll() if tag.name in ['div', 'p', 'h']
    ]
  except:
    return

  result = {
    'url': url,
    'title': title,
    'description': description
  }
  
  data.append(result)

  if depth == 0:
    return
  
  try:
    links = content.findAll('a')
    for link in links:
      try:
        if 'http' in link['href']:
          crawl(link['href'], depth-1)
      except KeyError:
        pass
  except:
    return

  return

crawl(url, 2)

with open('test.json', 'w', encoding='utf-8') as jsonFile:
  json.dump(data, jsonFile, indent=2)
