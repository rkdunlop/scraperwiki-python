#!/usr/bin/env python2
# utils.py
# David Jones, ScraperWiki Limited
# Thomas Levine, ScraperWiki Limited

'''
Local version of ScraperWiki Utils, documentation here:
https://scraperwiki.com/docs/python/python_help_documentation/
'''

import os
import sys
import warnings
import tempfile
import urllib
import urllib2
import requests


def scrape(url, params=None, user_agent=None):
    '''
    Scrape a URL optionally with parameters.
    This is effectively a wrapper around urllib2.urlopen.
    '''

    headers = {}

    if user_agent:
        headers['User-Agent'] = user_agent

    data = params and urllib.urlencode(params) or None
    req = urllib2.Request(url, data=data, headers=headers)
    f = urllib2.urlopen(req)

    text = f.read()
    f.close()

    return text


def pdftoxml(pdfdata, options=""):
    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf',delete=False)
    pdffout.write(pdfdata)
    pdffout.close()

    xmlin = tempfile.NamedTemporaryFile(suffix='.xml', delete=False)
    tmpxml = xmlin.name  # "temph.xml"
    cmd = 'pdftohtml -xml -zoom 1.5 -enc UTF-8 -noframes %s "%s" "%s"' % (
        options, pdffout.name, os.path.splitext(tmpxml)[0])
    # can't turn off output, so throw away even stderr yeuch
    #cmd = cmd + " >/dev/null 2>&1"
    os.system(cmd)

    os.remove(pdffout.name)
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    os.remove(xmlin.name)
    return xmldata.decode('utf-8')


def _in_box():
    return os.environ.get('HOME', None) == '/home'


def status(type, message=None):
    assert type in ['ok', 'error']

    # if not running in a ScraperWiki platform box, silently do nothing
    if not _in_box():
        return "Not in box"

    url = os.environ.get("SW_STATUS_URL", "https://scraperwiki.com/api/status")
    if url == "OFF":
        # For development mode
        return

    # send status update to the box
    r = requests.post(url, data={'type': type, 'message': message})
    r.raise_for_status()
    return r.content
