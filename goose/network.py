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
import urllib2
import requests
import goose.exceptions

class HtmlFetcher(object):

    def __init__(self, config):
        self.config = config
        # set header
        self.headers = {'User-agent': self.config.browser_user_agent}

    def get_url(self):
        # if we have a result
        # get the final_url
        if self.result is not None:
            return self.result.geturl()
        return None

    def get_html(self, url):
        # utf-8 encode unicode url

        if isinstance(url, unicode):
            url = url.encode('utf-8')

        #we need this because it used somethere else
        self.request = urllib2.Request(url, headers = self.headers)    

        # do request
        try:
            self.result = requests.get(url, headers = self.headers, timeout = self.config.http_timeout)
        except requests.exceptions.ConnectionError as error:
            raise goose.exceptions.ConnectionError(error)
        except requests.exceptions.HTTPError as error:
            raise goose.exceptions.UnknownError(error) 
        except requests.exceptions.Timeout as error:
            raise goose.exceptions.TimeoutError(error) 
        except requests.exceptions.TooManyRedirects as error:
            raise goose.exceptions.TooManyRedirectsError(error)
        except Exception as error:
            raise Ugoose.exceptions.UnknownError(error) 

        code = str(self.result.status_code)    

        if code.startswith('2'):
            return self.result.text
        elif code.startswith('3'):
            raise goose.exceptions.UnexpectedRedirectError(self.result.text)
        elif code == '401':
            raise goose.exceptions.NotAuthorizedError(self.result.text)
        elif code == '404':
            raise goose.exceptions.NotFoundError(self.result.text) 
        elif code.startswith('5'):
            raise goose.exceptions.UnknownError(self.result.text)

        return None   

        
