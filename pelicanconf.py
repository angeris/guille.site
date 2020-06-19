#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Guillermo Angeris'
SITENAME = u'Longest Path Search'
SITEURL = 'https://guille.site'

PATH = 'content'

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = u'en'

THEME = 'theme'

TAGLINE = 'Because finding the shortest path is overrated (and not NP-Hard).'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

# DEFAULT_PAGINATION = 10

FEED_RSS = 'feeds/feed.rss'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['/Users/guille/Documents/programming/pelican-plugins']
PLUGINS = ['render_math']

STATIC_PATHS = ['images', 'notes']
