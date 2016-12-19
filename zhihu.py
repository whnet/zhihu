#!/usr/bin/env python
# coding: utf-8

import time
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
from tools import model_to_dict
from spider import Spider
from parser import HtmlPageParser, extract_question_id
from model import Question, SpiderValue, Answer, AnswerContent


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
            question['like_count'] = count
            print question
            questions.append(question)
        return questions

    @property
    def answers(self, max_count=20):
        answers = []
        assert answers
        elements_a = self.page.xpath(u"")
        elements_b = self.page.xpath(u"")
        elements_c = self.page.xpath(u"")
        for arg in zip(elements_a, elements_b, elements_c):
            ele_a, ele_b, ele_c = arg
            answer = dict()
            answer['answer_id'] = ''
            answers.append(answer)
        return answers


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
            fails = fails + 1
            if fails > 5:
                return
            gevent.sleep(0.5 * fails)
        page = ZhihuPage(page_url, html)
        with closing(Session()) as session:
            for q in page.questions:
                _q = Question()
                _q.zhihu_id = q['question_id']
                _q.url = q['url']
                _q.like_count = q['like_count']
                _q.title = q['title']
                session.add(_q)
                session.commit()
        gevent.sleep(0.5)
    args = [(zhihu, x) for x in page_urls]
    pool.map(fetch_questions, args)


def answer_crawler():

    def fetch_answers(args):
        zhihu, question = args
        page_url = question['url']
        fails = 0
        try:
            html = zhihu.fetch(page_url)
        except:
            fails = fails + 1
            if fails > 5:
                return
            gevent.sleep(0.5 * fails)
        answers = html.answers(10)
        for answer in answers:
            try:
                _a = Answer()
                _a.zhihu_id = answer['id']
                _a.nick_name = answer['nick_name']
                _a.like_count = answer['like_count']
                _a.question_id = question['question_id']
                session.add(_a)
                session.flush()
                _c = AnswerContent()
                _c.answer_id = _a.id
                _c.content = answer.content
                session.add(_c)
                session.commit()
            except:
                session.rollback()

    zhihu = ZhihuSpider()
    zhihu.login('')
    with closing(Session()) as session:
        pool = Pool(5)
        while True:
            lock_sql = \
                ("select *from spider_value "
                 "where name = 'spider.value.lock' "
                 "for update;")
            session.execute(lock_sql)
            value_key = 'spider.value.last_question_id'
            spider_value = session.query(SpiderValue) \
                .filter(
                    SpiderValue.name == value_key) \
                .first()
            if spider_value is None:
                spider_value = SpiderValue()
                spider_value.name = value_key
                spider_value.value = '0'
                session.add(spider_value)
                session.flush()
            last_question_id = int(spider_value.value)
            questions = []
            for question in session.query(Question) \
                    .filter(Question.id > last_question_id) \
                    .order_by(Question.id) \
                    .limit(100):
                questions.append(model_to_dict(question))
            if not questions:
                time.sleep(5)
            last_question_id = questions[-1]['id']
            spider_value.value = str(last_question_id)
            session.commit()
            args = [(zhihu, q) for q in questions]
            pool.map(fetch_answers, args)


if __name__ == '__main__':
    question_crawler()
