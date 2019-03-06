import threading
from saver import Saver
from parser2 import Parser
from url import UrlManager
from download import get_response


class Spider(threading.Thread):
    def __init__(self, queue, home_urls, editors,
                 keywords, st, et, save_dir):
        """
        home_urls: str 新闻来源
        editors: str 编辑来源（文字）
        keywords: list 关键词
        st: start time
        et: end time
        save_dir: str 保存目录
        """
        threading.Thread.__init__(self)
        self.queue = queue

        self.home_urls = home_urls
        self.editors = editors
        self.keywords = keywords
        self.st = st
        self.et = et
        self.save_dir = save_dir

        # url manager
        self.url_manager = UrlManager()
        # parser
        self.parser = Parser(editors, keywords, st, et)
        # saver
        self.saver = Saver(save_dir)

    def run(self):
        for home_url in self.home_urls:
            self.url_manager.add_url(home_url)

            # iteration
            while not self.url_manager.is_empty():
                cur_url = self.url_manager.get_url()
                print('cur_url: {}'.format(cur_url))

                if self.url_manager.is_viewed(cur_url):
                    continue

                # 获取当前页面新闻列表 (列表页）
                response = get_response(cur_url)

                # 解析内容并保存 content_list_result 返回的是列表页所有的 page 内容
                content_list_result, next_url = self.parser.parse_content_list(response, self.url_manager)

                #  print('content_list_result： {}'.format(content_list_result))
                print('next_url： {}'.format(next_url))

                if next_url is not None:
                    self.url_manager.add_url(next_url)

                # 保存
                self.saver.save_2_file(content_list_result)

                # 标记已访问
                self.url_manager.add_viewed(cur_url)

        print('crawl finished.')
        self.queue.put('爬取完成。')

    def stop(self):
        self.url_manager.urls = []
        self.url_manager.empty = True
        self.queue.put('停止爬取。')
