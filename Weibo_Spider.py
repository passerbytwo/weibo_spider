# -*- coding: utf-8 -*-

import os
#import sys
import urllib2
import re
import zlib
import time
import random

def Page_Access(url,i):
		
	html_list = []
	care_url = 'http://m.weibo.cn/page/tpl?containerid=100505'+url[i][0]+'_-_FOLLOWERS'
	ua = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
	'Connection':'Keep-Alive',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Accept-Encoding':'gzip,deflate,sdch',
	'Accept':'*/*',
	'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
	'Cache-Control':'max-age=0',
	'referer':' "http://m.weibo.cn/u/"+url[i][0] '
	}
	cookie = {"Cookie":"这里写微博的cookie"}

	request = urllib2.Request(care_url, headers = ua)
	response = urllib2.urlopen(request)
	html = response.read()

	gzipped = response.headers.get('Content-Encoding')
	if gzipped:
		html = zlib.decompress(html, 16+zlib.MAX_WBITS)
	response.close()

	return html

def New_Page_Info(html, url_results, i):
	save_path = u'微博抓取'
	results = re.findall(r'\{"id":(.*?),"screen_name":"(.*?)","profile_image_url"', html, re.S)
	LEN = len(results)
	filename = url_results[i][1]+"_"+u"关注的人"
	if not os.path.exists(save_path):
		os.makedirs(save_path)
	path = save_path+"/"+filename+".txt"
	print u"正在写入文件..."
	try:
		fp = open(path, 'w+')
		fp.write("%s\t\t%s\n" % (url_results[i][0].encode("utf8"), url_results[i][1].encode("utf8")))
	except:
		print u'文件打开错误'
	for i in range(LEN):
		tmp1 = results[i][0]
		tmp2 = results[i][1].decode('unicode_escape')
		tmp_results = (tmp1,tmp2)
		fp.write("%s\t\t%s\n" % (tmp_results[0].encode("utf8"), tmp_results[1].encode("utf8")))
		if tmp_results not in url_results:
			url_results.append(tmp_results)
	fp.close()
	
	return url_results

def Spider():
	i = 0
	url = '1878546883'
	url_results = [(url, u'孙杨')]
	
	for url, item in url_results:
		print u"正在抓取%s的微博"%url_results[i][1]
		html_result = Page_Access(url_results,i)
		url_results = New_Page_Info(html_result, url_results, i)
		print u"列表中共有%d人"%len(url_results)
		time.sleep(random.randint(1,5))
		f = open('break.log','w+')
		f.write(str(url_results))
		f.close()
		i = i + 1

if __name__ == '__main__':
	print u"爬虫启动ing..."
	Spider()
