#!/usr/bin/env python
# coding: utf-8

import os
import contextlib
from urlparse import urljoin
from multiprocessing import Process, cpu_count

import gevent
import requests
from gevent.pool import Pool
from sqlalchemy import func
from gevent import monkey
monkey.patch_all()  # noqa

import const
import config
import exceptions
from db import Session
from spider import Spider
from parser import HtmlPageParser, extract_question_id
from model import SpiderValue, Question


class ZhihuPage(HtmlPageParser):

    @property
    def questions(self):
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
    def answers(self):
        elements_a = self.page.xpath(
            u"//div[@class='zm-editable-content clearfix']")
        elements_b = self.page.xpath(
            u"//div[@class='zm-item-answer-author-info']")
        elements_c = self.page.xpath(
            u"//span[@class='js-voteCount']")
        print elements_a, elements_b, elements_c


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
        with contextlib.closing(Session()) as session:
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


_zhihu = ZhihuSpider(
    config.ZHIHU_USER_PHONE,
    config.ZHIHU_USER_PASSWORD)
_zhihu.login('')


def start_multi_instance():
    worker_num = min(cpu_count(), config.MIN_WOKER_NUM)
    for i in range(worker_num):
        p = Process(target=crawler, args=(i,))
        p.start()


def query_questions(min_id, max_id):
    with contextlib.closing(Session()) as session:
        questions = []
        for _question in session.query(Question) \
                .filter(
                    Question.id > min_id,
                    Question.id <= max_id).all():
            questions.append(_question)
        return questions


def fetch_then_parse(question):
    question_url = question.url
    html = _zhihu.fetch(question_url)
    page = ZhihuPage(question_url, html)
    print page.answers


def crawler(idx):
    print "pid: %d, ppid: %d" % (os.getpid(), os.getppid())
    read_lock_sql = \
        ("select *from spider_value where name"
         " = 'spider.value.lock' for update;")
    read_per_cycle = config.READ_STEP_PER_CYCLE
    with contextlib.closing(Session()) as session:
        tries = 0
        pool = Pool(5)
        while True:
            gevent.sleep(0.5)
            session.execute(read_lock_sql)
            spider_config_key = 'spider.value.last_question_id'
            spider_config = session.query(SpiderValue).filter(
                SpiderValue.name == spider_config_key).first()
            if spider_config is None:
                spider_config = SpiderValue()
                spider_config.name = spider_config_key
                spider_config.value = '0'
                session.add(spider_config)
            last_question_id = int(spider_config.value)
            next_question_id = session.query(Question.id) \
                .filter(Question.id > last_question_id).order_by(Question.id) \
                .offset(read_per_cycle-1).limit(1).scalar()
            if next_question_id is None:
                next_question_id = session.query(func.max(Question.id)) \
                    .order_by(Question.id).scalar()
            if next_question_id == last_question_id:
                session.commit()
                tries = max(tries + 1, 20)
                gevent.sleep(tries * 0.5)
                continue
            tries = 0
            spider_config.value = str(next_question_id)
            session.commit()
            greenlets = []
            questions = query_questions(
               last_question_id, next_question_id)
            for _question in questions:
                greenlets.append(
                    pool.spawn(fetch_then_parse, _question))
            pool.join()
            last_question_id = next_question_id


if __name__ == '__main__':
    start_multi_instance()
    
