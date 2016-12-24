#!/usr/bin/env python
# coding: utf-8

import re
from lxml import etree


def extract_topic_id(page_uri):
    regex = re.compile(
        r'https://.*/topic/(\d+)/?',
        re.I | re.U)
    groups = regex.findall(page_uri)
    return groups[0]


def extract_question_id(page_uri):
    regex = re.compile(
        r'https://.*/question/(\d+)/?',
        re.I | re.U)
    groups = regex.findall(page_uri)
    return groups[0]


def extract_answer_id(page_uri):
    regex = re.compile(
        r'/question/(\d+)/answer/(\d+)/?',
        re.I | re.U)
    groups = regex.findall(page_uri)
    return groups[0][1]


class HtmlPageParser(object):

    def __init__(self,  page_url, page):
        if not isinstance(page, unicode):
            page = page.decode('utf-8')
        self.page = etree.HTML(page.lower())
        self.page_url = page_url
