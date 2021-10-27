from urllib.parse import urlsplit
import requests

from bs4 import BeautifulSoup

url = 'https://www.yeniakit.com.tr/haber/baskan-erdogan-o-diyalogu-acikladi-aliyev-dedi-ki-o-ismi-ulkeme-sokmam-1588739.html'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

print(list(set([link.attrs['href'] for link in soup.find_all('a') if 'href' in link.attrs])))
exit()
try:
    response = requests.get(url)
except (requests.exceptions.MissingSchema,
        requests.exceptions.ConnectionError,
        requests.exceptions.InvalidURL,
        requests.exceptions.InvalidSchema):
    # add broken urls to it's own set, then continue
    print(0, url)

else:
    # extract base url to resolve relative links
    parts = urlsplit(url)
    print(parts)
    base = f"{parts.netloc}"
    strip_base = base.replace("www.", "")
    base_url = f"{parts.scheme}://{parts.netloc}"
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url

    soup = BeautifulSoup(response.text, "lxml")

    for link in soup.find_all('a'):
        # extract link url from the anchor
        anchor = link.attrs["href"] if "href" in link.attrs else ''

        if anchor.startswith('#'):
            pass
        elif anchor.startswith('/'):
            local_link = base_url + anchor
            print(1, local_link, link)
        elif strip_base in anchor:
            print(2, anchor, link)
        else:
            print(4, anchor, link)
