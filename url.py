#  from pybloom import BloomFilter


# 管理url列表
class UrlManager(object):
    def __init__(self):
        self.urls = []
        #  self.url_bloom_filter = BloomFilter(capacity=800000, error_rate=0.0001)
        self.url_bloom_filter = set()
        self.empty = False

    def add_url(self, url):
        self.urls.append(url)

    def add_urls(self, urls):
        for url in urls:
            self.add_url(url)

    def is_empty(self):
        if self.empty:
            return True

        return len(self.urls) == 0

    def get_url(self):
        return self.urls.pop(0)

    def get_len(self):
        return len(self.urls)

    def is_viewed(self, url):
        return url in self.url_bloom_filter

    def add_viewed(self, url):
        self.url_bloom_filter.add(url)
