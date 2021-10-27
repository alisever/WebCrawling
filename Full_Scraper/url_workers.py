import multiprocessing as mp
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup

import sqlite

keyword = "feto"


def url_worker(url, q):
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidURL,
            requests.exceptions.InvalidSchema):
        # add broken urls to it's own set, then continue
        q.put((sqlite.insert_row_if_not_in, ('broken_urls', url)))
        return

    conn = sqlite.create_connection()
    processed_urls = [a[0] for a in
                      sqlite.select_all_rows(conn, 'processed_urls')]
    if response.url in processed_urls:
        q.put((sqlite.insert_row_if_not_in, ('processed_urls', url)))
        q.put((sqlite.delete_row, ('new_urls', url)))
        conn.close()
        return
    conn.close()

    # extract base url to resolve relative links
    parts = urlsplit(url)
    base = f"{parts.netloc}"
    strip_base = base.replace("www.", "")
    base_url = f"{parts.scheme}://{parts.netloc}"

    soup = BeautifulSoup(response.text, 'lxml')

    for anchor in list(set([link.attrs['href'] for link in soup.find_all('a')
                            if 'href' in link.attrs])):
        # extract link url from the anchor
        flag = True
        local_link = None

        if anchor.startswith('#'):
            flag = False
        elif anchor.startswith('/'):
            local_link = base_url + anchor
            q.put((sqlite.insert_row_if_not_in, ('local_urls', local_link)))
        elif strip_base in anchor:
            local_link = anchor
            q.put((sqlite.insert_row_if_not_in, ('local_urls', local_link)))
        else:
            flag = False
            q.put((sqlite.insert_row_if_not_in, ('foreign_urls', anchor)))

        if flag:
            conn = sqlite.create_connection()
            new_urls = [a[0] for a in sqlite.select_all_rows(conn, 'new_urls')]
            processed_urls = [a[0] for a in sqlite.select_all_rows(conn, 'processed_urls')]
            conn.close()
            if local_link not in new_urls and local_link not in processed_urls:
                q.put((sqlite.insert_row_if_not_in, ('new_urls', local_link)))

    if keyword in response.text.lower().encode('utf-8').decode():
        q.put((sqlite.insert_row_if_not_in, ('keyword_urls', url)))

    q.put((sqlite.insert_row_if_not_in, ('processed_urls', url)))
    q.put((sqlite.delete_row, ('new_urls', url)))


def url_listener(q):
    """listens for messages on the q."""
    conn = sqlite.create_connection()
    while True:
        f, args = q.get()
        if f == 'kill':
            conn.close()
            break
        f(conn, *args)


def main():
    # must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count() + 2)

    # put listener to work first
    watcher = pool.apply_async(url_listener, (q,))

    conn = sqlite.create_connection()
    while sqlite.select_all_rows(conn, 'new_urls'):
        # fire off workers
        jobs = [pool.apply_async(url_worker, (i[0], q)) for i in
                sqlite.select_all_rows(conn, 'new_urls')[0:100]]

        # collect results from the workers through the pool result queue
        for job in jobs:
            job.get()

        new_urls = len(sqlite.select_all_rows(conn, 'new_urls'))
        processed_urls = len(sqlite.select_all_rows(conn, 'processed_urls'))

        print(new_urls, processed_urls)

    conn.close()
    # now we are done, kill the listener
    q.put(('kill', 'kill'))
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
