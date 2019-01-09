import re
import jieba
from bs4 import BeautifulSoup
from urllib.request import urljoin
from pandas import to_datetime

from download import get_response


class Parser:
    def __init__(self, editors, keywords, st, et):
        self.editors = editors
        self.keywords = keywords
        self.st = to_datetime(st)
        self.et = to_datetime(et)

        self.init_jieba()
        self.number_re = re.compile(r'\d+')

    def init_jieba(self):
        for word in self.keywords:
            jieba.add_word(word)

    '''解析列表'''
    def parse_content_list(self, response, url_manager):
        content_list_result = {}
        soup = BeautifulSoup(response.content, 'lxml')

        # 新闻列表
        div_li_list = soup.findAll('div', {'class': 'l_li'})

        is_continue = True
        for div_li in div_li_list:
            try:
                page_url = urljoin(response.url, div_li.a['href'])
                title = div_li.a.text.replace(' ', '')
                date_time = div_li.cite.text[1:-1]
                datetime = to_datetime(date_time)

                print('page_url: {} \n title: {} \n date_time: {} \n'.format(page_url, title, date_time))

                if datetime <= self.et and datetime >= self.st:
                    # 解析正文
                    result = self.parse_page(title, page_url)
                    if result is None:
                        continue

                    content, imgs_url, write_info = result

                    url_manager.add_viewed(page_url)

                    # 当前新闻编号
                    page_number = self.number_re.match(page_url.split('/')[-1]).group(0)
                    content_list_result[page_number] = {
                        'title': title,
                        'date_time': date_time,
                        'write_info': write_info,
                        'imgs_url': imgs_url,
                        'content': content
                    }
                else:
                    is_continue = False
                    url_manager.add_viewed(page_url)
                    continue
            except Exception as e:
                continue

        if is_continue:
            '''获取下一页url'''
            next_url = urljoin(response.url, soup.findAll('a', {'class': 'Next'})[0]['href'])
        else:
            next_url = None
        return content_list_result, next_url

    '''解析page'''
    def parse_page(self, title, page_url):
        response = get_response(page_url)
        soup = BeautifulSoup(response.content, 'lxml')

        title_tokens = set(jieba.cut(title))
        is_keyword_relative = True
        if self.keywords is not None and len(self.keywords) > 0:
            is_keyword_relative = self.is_relative(self.keywords, title_tokens)

        # 判断标题和正文是否包含关键字
        content_div = soup.find('div', {'id': 'lmz_content'})
        if content_div is None:
            return None
        content = content_div.text

        # 如果标题没有相关内容，则判断正文
        if not is_keyword_relative:
            content_tokens = set(jieba.cut(content.repalce('\n', '').repalce('\t', '')))
            if self.keywords is not None and len(self.keywords) > 0:
                is_keyword_relative = self.is_relative(self.keywords, content_tokens)

        # 如果还没有则跳过
        if not is_keyword_relative:
            return None

        # 图片
        imgs_url = []
        imgs = soup.find('div', {'id': 'lmz_content'}).findAll('img')
        if imgs is not None:
            for img in imgs:
                img_url = urljoin(response.url, img['src'])
                imgs_url.append(img_url)

        # 作者, editor (文字)
        editor_text = ''
        editors = []

        write_info = ''
        author_div_list = soup.findAll('div', {'class': 'd_write2'})
        for div in author_div_list:
            text = div.text.rstrip()
            write_info += text + '\n'
            if text.startswith('文字'):
                editor_text = text.split('：')[-1]
                editors = editor_text.split()

        #  print('editor_text: %s' % editor_text)
        if len(self.editors) > 0:
            is_relative = False
            for editor in editors:
                if editor in self.editors:
                    is_relative = True
                    break
            if not is_relative:
                return None

        print('---- write_info ----\n{}'.format(write_info))
        return content, imgs_url, write_info

    def is_relative(selef, keywords, tokens):
        for keyword in keywords:
            if keyword in tokens:
                return True
        return False
