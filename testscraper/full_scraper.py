from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque

url = "https://www.sozcu.com.tr/"

# a queue of urls to be crawled next
new_urls = deque([url])

# a set of urls that we have already processed 
processed_urls = set()

# a set of domains inside the target website
local_urls = set()

# a set of domains outside the target website
foreign_urls = set()

# a set of broken urls
broken_urls = set()

# process urls one by one until we exhaust the queue
while len(new_urls):  # move url from the queue to processed url set
    url = new_urls.popleft()
    processed_urls.add(url)
    # print the current url

    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidURL,
            requests.exceptions.InvalidSchema):
        # add broken urls to it's own set, then continue    
        broken_urls.add(url)
        continue

    # extract base url to resolve relative links
    parts = urlsplit(url)
    base = "{0.netloc}".format(parts)
    strip_base = base.replace("www.", "")
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url

    soup = BeautifulSoup(response.text, "lxml")

    for link in soup.find_all('a'):
        # extract link url from the anchor
        anchor = link.attrs["href"] if "href" in link.attrs else ''

        if anchor.startswith('/'):
            local_link = base_url + anchor
            local_urls.add(local_link)
        elif strip_base in anchor:
            local_urls.add(anchor)
        elif not anchor.startswith('http'):
            local_link = path + anchor
            local_urls.add(local_link)
        else:
            foreign_urls.add(anchor)

        for i in local_urls:
            if i not in new_urls and i not in processed_urls:
                new_urls.append(i)

        if link not in new_urls and link not in processed_urls:
            new_urls.append(link)

    a = len(processed_urls)
    b = len(new_urls)
    print(f"Completed {a} out of {a + b}.")

print(local_urls)

import multiprocessing as mp
import time

fn = 'c:/temp/temp.txt'


def worker(arg, q):
    '''stupidly simulates long running process'''
    start = time.clock()
    s = 'this is a test'
    txt = s
    for i in range(200000):
        txt += s
    done = time.clock() - start
    with open(fn, 'rb') as f:
        size = len(f.read())
    res = 'Process' + str(arg), str(size), done
    q.put(res)
    return res


def listener(q):
    '''listens for messages on the q, writes to file. '''

    with open(fn, 'w') as f:
        while 1:
            m = q.get()
            if m == 'kill':
                f.write('killed')
                break
            f.write(str(m) + '\n')
            f.flush()


def main():
    # must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count() + 2)

    # put listener to work first
    watcher = pool.apply_async(listener, (q,))

    # fire off workers
    jobs = []
    for i in range(80):
        job = pool.apply_async(worker, (i, q))
        jobs.append(job)

    # collect results from the workers through the pool result queue
    for job in jobs:
        job.get()

    # now we are done, kill the listener
    q.put('kill')
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
