from random import choice

import requests
from lxml.html import fromstring

# Credit for proxies: https://www.alexbilz.com/post/rotating-free-elite-proxies-in-python/

class Proxies:

    def __init__(self):
        self.proxy = None
        self.proxies = []

    @staticmethod
    def get_proxies():
        url = 'https://sslproxies.org/'
        response = requests.get(url)
        parser = fromstring(response.text)
        p = []
        for i in parser.xpath('//tbody/tr'):
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                if i.xpath('.//td[5][contains(text(),"elite proxy")]'):
                    proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                    p.append(proxy)
        return p

    @staticmethod
    def to_proxy(proxy):
        return {"http": proxy, "https": proxy}

    def get(self):
        if len(self.proxies) < 2:
            self.proxies = self.get_proxies()
        self.proxy = choice(self.proxies)
        return self.to_proxy(self.proxy)

    def remove(self):
        # Remove invalid proxy from pool
        self.proxies.remove(self.proxy)
        self.proxy = self.get()

    def scrape(self, url, **kwargs):
        # Retry until request was sucessful
        while True:
            try:
                proxy = self.get()
                print("Proxy currently being used: {}".format(proxy))
                response = requests.get(url, proxies=proxy, timeout=5, **kwargs)
                break
            # if the request is successful, no exception is raised
            except requests.exceptions.ProxyError:
                print("Proxy error, choosing a new proxy")
                self.remove()
            except requests.exceptions.ConnectTimeout:
                print("Connect error, choosing a new proxy")
                self.remove()
        return response