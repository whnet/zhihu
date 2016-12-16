#!/usr/bin/env python
# coding: utf-8

import requests
from urlparse import urljoin

import const
import config
import exceptions
from spider import Spider
from parser import HtmlPageParser, extract_question_id


class ZhihuPage(HtmlPageParser):

    @property
    def questions(self):
        questions = []
        elements_a = self.page.xpath(u"//a[@class='question_link']")
        elements_b = self.page.xpath(u"//span[@class='count']")
        assert len(elements_a) == len(elements_b)
        for ele_a, ele_b in zip(elements_a, elements_b):
            question = dict()
            url = urljoin(
                self.page_url,
                ele_a.attrib['href'])
            question_id = extract_question_id(url)
            question['question_id'] = int(question_id)
            question['url'] = url
            question['title'] = ele_a.text
            question['count'] = int(ele_b.text)
            print question
            questions.append(question)
        return questions


class ZhihuSpider(Spider):

    def login(self, catpcha):
        data = {
            'phone_num': self.user,
            'password': self.password,
        }
        req = requests.Request(
            'POST',
            'https://www.zhihu.com/login/phone_num',
            data=data,
        )
        prepared = self.session.prepare_request(req)
        prepared.headers['Date'] = self.date
        prepared.headers['User-Agent'] = const.UA_CHROME
        ret = self.session.send(prepared)
        if ret is None or ret.status_code != 200:
            raise exceptions.LoginError()


if __name__ == '__main__':
    zhihu = ZhihuSpider(
        config.ZHIHU_USER_PHONE,
        config.ZHIHU_USER_PASSWORD)
    zhihu.login('')
    page_url = u'https://www.zhihu.com/topic/19559937/top-answers?page=3'
    html = zhihu.fetch(page_url)
    page = ZhihuPage(page_url, html)
    for d in page.questions:
        print d
