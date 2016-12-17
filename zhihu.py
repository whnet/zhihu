#!/usr/bin/env python
# coding: utf-8

from urlparse import urljoin
from contextlib import closing
from multiprocessing import cpu_count

import gevent
from gevent import monkey
monkey.patch_all()  # noqa
from gevent.pool import Pool
import requests

import const
import config
import exceptions
from db import Session
from model import Question
from spider import Spider
from parser import HtmlPageParser, extract_question_id


class ZhihuPage(HtmlPageParser):

    def html_page_identifier(self):
        identifier = -1
        page_url = self.page_url
        if 'topic' in page_url:
            identifier = 0
        elif 'question' in page_url and 'answer' not in page_url:
            identifier = 1
        elif 'anwser' in page_url:
            identifier = 2
        return identifier

    @property
    def questions(self):
        assert self.page_identifier == 0
        questions = []
        elements_a = self.page.xpath(u"//a[@class='question_link']")
        elements_b = self.page.xpath(u"//span[@class='count']")
        elements_a = elements_a[:len(elements_b)]
        for ele_a, ele_b in zip(elements_a, elements_b):
            question = dict()
            url = urljoin(
                self.page_url,
                ele_a.attrib['href'])
            question_id = extract_question_id(url)
            question['question_id'] = int(question_id)
            question['url'] = url
            question['title'] = ele_a.text.strip()
            count = ele_b.text
            if 'k' in count:
                count = int(count[:-1]) * 1000
            question['count'] = count
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
        ret = self.session.send(prepared, timeout=10)
        if ret is None or ret.status_code != 200:
            raise exceptions.LoginError()


def question_crawler():
    zhihu = ZhihuSpider(
        config.ZHIHU_USER_PHONE,
        config.ZHIHU_USER_PASSWORD)
    zhihu.login('')
    url_template = \
        (u'https://www.zhihu.com/topic/'
         u'19559937/top-answers?page=%d')
    page_urls = [url_template % x for x in range(1, 10)]
    pool = Pool(min(cpu_count(), 5))

    def fetch_questions(args):
        zhihu, page_url = args
        fails = 0
        try:
            html = zhihu.fetch(page_url)
        except:
            fails += 1
            if fails > 5:
                return
        page = ZhihuPage(page_url, html)
        with closing(Session()) as session:
            for q in page.questions:
                _q = Question()
                _q.zhihu_id = q['question_id']
                _q.url = q['url']
                _q.fllower_count = q['count']
                _q.title = q['title']
                session.add(_q)
                session.commit()
        gevent.sleep(1)
    args = [(zhihu, x) for x in page_urls]
    pool.map(fetch_questions, args)


if __name__ == '__main__':
    question_crawler()
