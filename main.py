#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2019 LeonTao
#
# Distributed under terms of the MIT license.

import os
import datetime
import queue
import tkinter as tk
from tkinter import filedialog

from util import center_window
from spider import Spider


class GradeGui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('XJTU 主页新闻抓取平台')
        # self.geometry("700x900")
        center_window(self, 800, 500)
        self.resizable(False, False)

        standard_font = (None, 14)

        self.main_frame = tk.Frame(self, width=600, height=400, bg="lightgrey")

        self.button_frame = tk.Frame(self, width=600, height=100)

        self.start_btn = tk.Button(self.button_frame, text="开始抓取", bg="lightgrey", fg="black",
                                      command=self.start_crawl, font=standard_font, state="disabled")
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_btn = tk.Button(self.button_frame, text="停止抓取", bg="lightgrey", fg="black",
                                      command=self.stop_crawl,
                                      font=standard_font)
        self.stop_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.button_frame.pack(side=tk.BOTTOM, pady=10)

        self.parameters_frame = tk.Frame(self, width=280, height=300)
        self.parameters_frame.pack(side=tk.LEFT, padx=5)

        # 文字 （编辑）
        editor_frame = tk.Frame(self.parameters_frame, width=200, height=50)
        editor_label = tk.Label(editor_frame, text='文字：', font=standard_font)
        editor_label.pack(side=tk.LEFT, padx=2)

        self.editor_var = tk.StringVar()
        self.editor_entry = tk.Entry(
            editor_frame, textvariable=self.editor_var, font=standard_font)
        self.editor_entry.pack(side=tk.RIGHT, padx=2)
        self.editor_default_v = '多个文字使用空格隔开'
        self.editor_var.set(self.editor_default_v)
        editor_frame.pack(side=tk.TOP, pady=10)

        # 关键词
        keyword_frame = tk.Frame(self.parameters_frame, width=200, height=50)
        keyword_label = tk.Label(keyword_frame, text='关键词：', font=standard_font)
        keyword_label.pack(side=tk.LEFT, padx=2)

        self.keyword_var = tk.StringVar()
        self.keyword_entry = tk.Entry(
            keyword_frame, textvariable=self.keyword_var, font=standard_font)
        self.keyword_entry.pack(side=tk.RIGHT, padx=2)
        self.keyword_default_v = '多个关键词使用空格隔开'
        self.keyword_var.set(self.keyword_default_v)

        keyword_frame.pack(side=tk.TOP, pady=10)

        # 起始时间
        st_frame = tk.Frame(self.parameters_frame, width=200, height=50)
        st_lable = tk.Label(st_frame, text='起始时间：', font=standard_font)
        st_lable.pack(side=tk.LEFT, padx=2)

        self.st_var = tk.StringVar()
        self.st_entry = tk.Entry(st_frame, textvariable=self.st_var, font=standard_font)
        self.st_entry.pack(side=tk.RIGHT, padx=2)
        self.st_default_v = '如：2019-1-1'
        self.st_var.set(self.st_default_v)
        st_frame.pack(side=tk.TOP, pady=10)

        # 截止时间
        et_frame = tk.Frame(self.parameters_frame, width=200, height=50)
        et_label = tk.Label(et_frame, text='截止时间：', font=standard_font)
        et_label.pack(side=tk.LEFT, padx=2)

        self.et_var = tk.StringVar()
        self.et_entry = tk.Entry(et_frame, textvariable=self.et_var, font=standard_font)
        self.et_entry.pack(side=tk.RIGHT, padx=2)
        self.et_default_v = '默认至今'
        self.et_var.set(self.et_default_v)
        et_frame.pack(side=tk.TOP, pady=10)

        # 保存路径
        save_frame = tk.Frame(self.parameters_frame, width=200, height=50)
        save_label = tk.Label(save_frame, text='保存目录：', font=standard_font)
        save_label.pack(side=tk.LEFT, padx=2)

        self.save_var = tk.StringVar()
        self.save_entry = tk.Entry(save_frame, textvariable=self.save_var, font=standard_font)
        self.save_entry.pack(side=tk.RIGHT, padx=2)

        self.choose_dir_btn = tk.Button(save_frame, text="选择目录", bg="lightgrey", fg="black",
                                      command=self.choose_dir, font=standard_font, state="active")
        self.choose_dir_btn.pack(side=tk.RIGHT, padx=2)

        save_frame.pack(side=tk.TOP, pady=10)

        self.output_frame = tk.Frame(self, width=280, height=300)
        self.output_frame.pack(side=tk.RIGHT, padx=5)

        self.output_text = tk.Text(self.output_frame, bg="#f2f2f2", fg="black", font=standard_font)
        #  self.output_text.configure(state='readonly')
        self.output_text.pack(side=tk.TOP, expand=1, pady=10)

        self.output_text.delete('1.0', tk.END)
        self.output_text['state'] = tk.DISABLED

        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

    # choose dir
    def choose_dir(self):
        self.output_text['state'] = tk.NORMAL
        save_dir = filedialog.askdirectory()

        if (os.path.exists(save_dir)):
            print('save_dir: %s' % save_dir)
            self.start_btn['state'] = tk.NORMAL
            #  self.output_text.insert(
                #  tk.INSERT, "保存目录: {} \n".format(save_dir))
        else:
            self.output_text.insert(tk.INSERT, "目录不存在，请重新选择 \n")
        self.save_var.set(save_dir)

    def start_crawl(self):
        home_url = 'http://news.xjtu.edu.cn/zyxw.htm'  # 主页新闻

        editor_text = self.editor_var.get()
        if editor_text == '' or editor_text == self.editor_default_v:
            editor_text = ''
        editors = editor_text.split()
        self.output_text.insert(tk.INSERT, "文字：%s\n"  % ' '.join(editors))

        keyword_text = self.keyword_var.get()
        if keyword_text == '' or keyword_text == self.keyword_default_v:
            keyword_text = ''
        keywords = keyword_text.split()
        self.output_text.insert(tk.INSERT, "关键词：%s\n"  % ' '.join(keywords))

        st = self.st_var.get()
        if st == '' or st == self.st_default_v:
            st = '2000-01-01 00:00:00'
        self.output_text.insert(tk.INSERT, "开始时间：%s\n"  % st)

        et = self.et_var.get()
        if et == '' or et == self.et_default_v:
            et = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.output_text.insert(tk.INSERT, "结束时间：%s\n"  % et)

        save_dir = self.save_var.get()
        if save_dir == '' or not os.path.exists(save_dir):
            self.output_text.insert(tk.INSERT, "目录不存在，请重新选择 \n")
            return

        self.output_text.insert(tk.INSERT, "保存目录：%s\n"  % save_dir)
        self.output_text.insert(tk.INSERT, "正在爬取...\n")

        self.queue = queue.Queue()
        self.spider = Spider(
            self.queue,
            home_url,
            editors,
            keywords,
            st,
            et,
            save_dir
        )
        self.spider.start()
        self.after(100, self.process_queue)
        self.start_btn['state'] = tk.DISABLED

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            # Show result of the task if needed
            self.output_text.insert(tk.INSERT, "%s\n" % msg)
            self.start_btn['state'] = tk.NORMAL
        except queue.Empty:
            self.after(100, self.process_queue)

    def stop_crawl(self):
        self.spider.stop()
        #  self.output_text.insert(tk.INSERT, "停止爬取。\n")
        self.start_btn['state'] = tk.NORMAL

    def safe_destroy(self):
        self.destroy()


if __name__ == "__main__":
    gui = GradeGui()
    gui.mainloop()
