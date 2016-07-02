# coding: utf-8

import memcache

IP = '127.0.0.1'

mc = memcache.Client(['%s:15211' % IP])
