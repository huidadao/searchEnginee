import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com'

def downloadUrl(url):
  r = requests.get(url)
  if r.status_code != 200:
    raise Exception(f"Non-OK status code: {r.status_code}")
  return r.text

def parseText(html):
  bs = BeautifulSoup(html)
  return bs.select('.quote')[0].text
  

r = downloadUrl(url)
bodyText = parseText(r)

print(bodyText)