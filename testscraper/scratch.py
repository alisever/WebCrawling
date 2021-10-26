import requests
import re
from bs4 import BeautifulSoup

keyword = "fet\u00f6"

url = 'https://www.yeniakit.com.tr/haber/fetoculere-karsi-erdogani-boyle-desteklediler-1586546.html'
url1 = 'https://stackoverflow.com/questions/9007653/how-to-find-tag-with-particular-text-with-beautiful-soup'

response = requests.get(url)

print(keyword in response.text.lower().encode('ISO-8859-1').decode())
