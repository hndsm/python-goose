# -*- coding: utf-8 -*-
"""\
This is a python port of "Goose" orignialy licensed to Gravity.com
under one or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.

Python port was written by Xavier Grangier for Recrutae

Gravity.com licenses this file
to you under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import json
import re

from base import BaseMockTests, MockResponse

from goose import Goose
from goose.utils import FileHelper
from goose.configuration import Configuration
from goose.text import StopWordsChinese
from goose.text import StopWordsArabic
from goose.text import StopWordsKorean


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class MockResponseExtractors(MockResponse):
    def content(self, req):
        current_test = self.cls._get_current_testname()
        path = os.path.join(CURRENT_PATH, "data", "extractors", "%s.html" % current_test)
        path = os.path.abspath(path)
        content = FileHelper.loadResourceFile(path)
        return content


class TestExtractionBase(BaseMockTests):
    """\
    Extraction test case
    """
    callback = MockResponseExtractors

    def getRawHtml(self):
        return self.load_test_file('.html')

    def loadData(self):
        content = self.load_test_file('.json')
        self.data = json.loads(content)

    def load_content_html(self):
        self.expected_content_html = self.load_test_file('.content.html')

    def load_test_file(self, suffix):
        suite, module, cls, func = self.id().split('.')
        path = os.path.join(CURRENT_PATH, "data", module, "%s%s" % (func, suffix))
        path = os.path.abspath(path)
        try:
            return FileHelper.loadResourceFile(path)
        except IOError:
            pass

    def assert_cleaned_text(self, field, expected_value, result_value):
        """\

        """
        # # TODO : handle verbose level in tests
        # print "\n=======================::. ARTICLE REPORT %s .::======================\n" % self.id()
        # print 'expected_value (%s) \n' % len(expected_value)
        # print expected_value
        # print "-------"
        # print 'result_value (%s) \n' % len(result_value)
        # print result_value

        # cleaned_text is Null
        msg = u"Resulting article text was NULL!"
        self.assertNotEqual(result_value, None, msg=msg)

        # cleaned_text length
        msg = u"Article text was not as long as expected beginning!"
        self.assertTrue(len(expected_value) <= len(result_value), msg=msg)

        # clean_text value
        result_value = result_value[0:len(expected_value)]
        msg = u"The beginning of the article text was not as expected!"
        self.assertEqual(expected_value, result_value, msg=msg)

    def assert_tags(self, field, expected_value, result_value):
        """\

        """
        # as we have a set in expected_value and a list in result_value
        # make result_value a set
        expected_value = set(expected_value)

        # check if both have the same number of items
        msg = (u"expected tags set and result tags set"
                u"don't have the same number of items")
        self.assertEqual(len(result_value), len(expected_value), msg=msg)

        # check if each tag in result_value is in expected_value
        for tag in result_value:
            self.assertTrue(tag in expected_value)

    def runArticleAssertions(self, article, fields):
        """\

        """
        for field in fields:
            expected_value = self.data['expected'][field]
            result_value = getattr(article, field, None)

            # custom assertion for a given field
            assertion = 'assert_%s' % field
            if hasattr(self, assertion):
                getattr(self, assertion)(field, expected_value, result_value)
                continue

            # default assertion
            msg = u"Error %s" % field
            self.assertEqual(expected_value, result_value, msg=msg)

    def assert_content_html(self, article):
        expected_content_html = re.sub('\s', '', self.expected_content_html)
        actual_content_html = re.sub('\s', '', article.content_html).decode("utf8")
        msg = u"HTML content is incorrect\n\n"
        msg += "Expected: %s\n\n" % self.expected_content_html
        msg += "Actual: %s" % article.content_html.decode("utf8")
        self.assertEqual(expected_content_html, actual_content_html, msg=msg)

    def extract(self, instance):
        article = instance.extract(url=self.data['url'])
        return article

    def getConfig(self):
        config = Configuration()
        config.enable_image_fetching = False
        return config

    def getArticle(self):
        """\

        """
        # load test case data
        self.loadData()
        self.load_content_html()

        # basic configuration
        # no image fetching
        config = self.getConfig()
        self.parser = config.get_parser()

        # target language
        # needed for non english language most of the time
        target_language = self.data.get('target_language')
        if target_language:
            config.target_language = target_language
            config.use_meta_language = False

        # run goose
        g = Goose(config=config)
        return self.extract(g)


class TestExtractions(TestExtractionBase):

    def test_allnewlyrics1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_cnn1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek2(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek3(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_cbslocal(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_elmondo1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_elpais(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_liberation(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_lefigaro(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_techcrunch1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['title', 'cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_foxNews(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_aolNews(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_huffingtonPost2(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_testHuffingtonPost(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'meta_description', 'title', ]
        self.runArticleAssertions(article=article, fields=fields)

    def test_espn(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_engadget(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_msn1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    # #########################################
    # # FAIL CHECK
    # # UNICODE
    # def test_guardian1(self):
    #     article = self.getArticle()
    #     fields = ['cleaned_text']
    #     self.runArticleAssertions(article=article, fields=fields)
    def test_time(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'title']
        self.runArticleAssertions(article=article, fields=fields)

    def test_time2(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_cnet(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_yahoo(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_politico(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessinsider1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessinsider2(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessinsider3(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_cnbc1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_marketplace(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue24(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue25(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue28(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue32(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue4(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_gizmodo1(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'meta_description', 'meta_keywords']
        self.runArticleAssertions(article=article, fields=fields)

    def test_mashable_issue_74(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_usatoday_issue_74(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_okaymarketing(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)

    def test_bbc(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_theguardian(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_blockquotes(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_open_graph_content(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_clean_bad_tags(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_embedded_media_items(self):
        article = self.getArticle()
        self.assert_content_html(article)


class TestKnownHosts(TestExtractionBase):
    def test_known_host_selectors(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_known_host_selectors_with_regexs_references(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_huffingtonpost(self):
        article = self.getArticle()
        self.assert_content_html(article)


class TestRelativePaths(TestExtractionBase):

    def test_relative_paths(self):
        article = self.getArticle()
        self.assert_content_html(article)

    def test_tags_with_no_path(self):
        article = self.getArticle()
        self.assert_content_html(article)

class TestReplacingAttributes(TestExtractionBase):

    def test_replacing_attributes(self):
        article = self.getArticle()
        self.assert_content_html(article)


class TestPublishDate(TestExtractionBase):

    def test_publish_date(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=['publish_date'])

    def test_publish_date_rnews(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=['publish_date'])

    def test_publish_date_article(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=['publish_date'])

class TestMetaDescription(TestExtractionBase):

    def test_meta_description(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=['meta_description'])


class TestExtractWithUrl(TestExtractionBase):

    def test_get_canonical_url(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'canonical_link']
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractChinese(TestExtractionBase):

    def getConfig(self):
        config = super(TestExtractChinese, self).getConfig()
        config.stopwords_class = StopWordsChinese
        return config

    def test_bbc_chinese(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractArabic(TestExtractionBase):

    def getConfig(self):
        config = super(TestExtractArabic, self).getConfig()
        config.stopwords_class = StopWordsArabic
        return config

    def test_cnn_arabic(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text']
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractKorean(TestExtractionBase):

    def getConfig(self):
        config = super(TestExtractKorean, self).getConfig()
        config.stopwords_class = StopWordsKorean
        return config

    def test_donga_korean(self):
        return 'pending'
        article = self.getArticle()
        fields = ['cleaned_text', 'meta_description', 'meta_keywords']
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractionsRaw(TestExtractions):

    def extract(self, instance):
        article = instance.extract(raw_html=self.getRawHtml())
        return article

    def test_bbc(self):
        return 'pending'


class TestArticleTags(TestExtractionBase):

    def test_tags_kexp(self):
        article = self.getArticle()
        fields = ['tags']
        self.runArticleAssertions(article=article, fields=fields)

    def test_tags_deadline(self):
        article = self.getArticle()
        fields = ['tags']
        self.runArticleAssertions(article=article, fields=fields)

    def test_tags_wnyc(self):
        article = self.getArticle()
        fields = ['tags']
        self.runArticleAssertions(article=article, fields=fields)

    def test_tags_cnet(self):
        article = self.getArticle()
        fields = ['tags']
        self.runArticleAssertions(article=article, fields=fields)

    def test_tags_abcau(self):
        """
        Test ABC Australia page with "topics" tags
        """
        article = self.getArticle()
        fields = ['tags']
        self.runArticleAssertions(article=article, fields=fields)
