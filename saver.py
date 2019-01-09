import os
import shutil
import requests

'''
content_list_result:
{'800':{
        'content': ...
    }
}
'''

class Saver:
    def __init__(self, dir_path):
        self.texts_dir_path = os.path.join(dir_path, 'texts')
        self.images_dir_path = os.path.join(dir_path, 'images')

        if not os.path.exists(self.texts_dir_path):
            os.mkdir(self.texts_dir_path)
        if not os.path.exists(self.images_dir_path):
            os.mkdir(self.images_dir_path)

    def save_2_file(self, content_list_result):
        for number, item in content_list_result.items():
            # 保存文本

            f = open(os.path.join(self.texts_dir_path, item['title'] + '.txt'), 'w', encoding='utf-8')
            f.write(item['title'] + '\n')
            f.write(item['date_time'] + '\n')
            f.write(item['write_info'] + '\n')
            f.write(item['content'])
            f.close()

            # 保存图片，对应一个文件夹
            imgs_dir = os.path.join(self.images_dir_path, item['title'])
            if not os.path.exists(imgs_dir):
                os.mkdir(imgs_dir)

            for i, img_url in enumerate(item['imgs_url']):
                print('download img : {}'.format(img_url))

                try:
                    r = requests.get(img_url, stream=True)
                    if r.status_code == 200:
                        name = str(i) + '.' + img_url.split('.')[-1]
                        with open(os.path.join(imgs_dir, name), 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                except Exception as e:
                    continue
