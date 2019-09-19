#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ************************************************************************
# *
# * @file:zhihuishu.py
# * @author:kanhui
# * date:2019-09-18 16:05:17
# * @version 3.7.3
# *
# ************************************************************************
import time
from selenium import webdriver
import re
from progress.bar import Bar


class BrushClass():    # 刷课英文咋说？Brush?
    '''智慧树刷课'''

    def __init__(self):
        self.driver = webdriver.Chrome()

    def start(self):

        # 打开注册页面
        self.driver.get(
            "https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin"
        )
        self.login()

    def login(self):

        print("输入登录手机号：")
        self.username = input()
        print("输入登录密码：")
        self.password = input()

        # 定位到用户名输入框
        username_input = self.driver.find_element_by_id('lUsername')
        # 填入手机号码
        username_input.send_keys(self.username)

        # 定位到密码输入框
        password_input = self.driver.find_element_by_id("lPassword")
        # 填入密码
        password_input.send_keys(self.password)

        print("正在登录...")

        # 定位登录按钮
        submit_btn = self.driver.find_element_by_class_name("wall-sub-btn")
        # 点击按钮
        submit_btn.click()
        print("正在加载主页请等候...")
        self.select_video()

    def select_video(self):
        time.sleep(10)
        courses = self.driver.find_elements_by_xpath(
            "//div[@id='sharingClassed']//ul")

        # 打印课程信息
        print("当前账号内已有课程：")
        course_names = [i.text.replace("\n", ' ') for i in courses]
        for index, name in enumerate(course_names, start=1):
            print(str(index) + '-' + name)

        print("输入序号选择要查看的课程如：1")
        course_id = input()

        print("正在打开课程页面请耐心等候>>>>")
        # 打开选择课程页面
        courses[int(course_id) - 1].click()

        print("课程页面打开成功，正在获取详细视频信息...")
        # time.sleep(5)

        print("开始关闭智慧树警告页面！")
        # 先关闭智慧树警告页面
        try:
            self.driver.find_element_by_class_name("popbtn_yes").click()
            print("警告页面关闭成功!")
        except:
            print("警告页面关闭失败。。。如果出现异常请关闭后重试。")
        # 打印课程的所有小节视频

        self.videos = self.driver.find_elements_by_xpath(
            "//div[@id='chapterList']/ul/li")
        self.video_names = [i.text.replace("\n", ' ') for i in self.videos]
        for index, name in enumerate(self.video_names, start=1):
            print(str(index) + '-' + name)

        print("输入需要观看的视频的序号可以是多个例如(注意是英文逗号不是中文逗号！！！)：1,2,3\n或者单个：1")
        self.video_ids = list(input().split(','))

        self.brush_class()

    def brush_class(self):
        # 刷课主要逻辑代码
        for id in self.video_ids:

            # 先关闭智慧树警告页面
            try:
                self.driver.find_element_by_class_name("popbtn_yes").click()
            except:
                pass
            # 点击视频
            time.sleep(3)
            self.videos[int(id) - 1].click()
            print("开始播放视频：" + self.video_names[int(id) - 1])

            print("正在获取视频进度请等待大约10s.")
            time.sleep(5)
            res = re.findall(r"00:([0-9]{2}:[0-9]{2})",
                             self.video_names[int(id) - 1])[0]
            video_time = int(res.split(':')[0]) * 60 + int(
                res.split(':')[1]) + 10

            # 获取视频进度
            bar = Bar("进度", max=100, fill='>', suffix='%(percent)d%%')
            for i in range(int(video_time / 5)):
                time.sleep(5)
                # video_prog = i * 5 / video_time * 100
                # print("当前进度：{}".format(str(format(video_prog,'0.1f')) + '%'))
                bar.next()
                # 关闭弹窗
                try:
                    self.driver.switch_to.frame("tmDialog_iframe")
                    self.driver.find_element_by_class_name(
                        "answerOption").click()
                    self.driver.switch_to.default_content()
                    self.driver.find_element_by_class_name(
                        "popbtn_cancel").click()
                    print("视频出现弹窗，已成功关闭。")
                except:
                    pass
            bar.finish()
            print(self.video_names[int(id) - 1] + '播放完成！')


if __name__ == '__main__':
    brush = BrushClass()
    brush.start()
