#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import random
import math
import time
import sys
sys.path.append("..")
from Lib import toolClass

class ChaseLetv :

	def __init__ (self) :
		self.videoLink     = ''
		self.fileUrlPrefix = 'http://api.letv.com/mms/out/video/playJsonH5?platid=3&splatid=304&tss=ios&detect=0&dvtype=1000&accessyx=1&domain=m.letv.com&'
		self.fileUrlSuffix = 'id=24419088tkey=-1957124021&devid=6bf5ee6495e436d480b1020e04f918b2'
		self.urlSuffix     = '&start=0&end=10000000000&'
		self.videoTypeList = {'n': '1000', 'h': '1300', 's': 'mp4'}
		self.videoType     = 'n'
		self.Tools         = toolClass.Tools()

	def chaseUrl (self) :
		result = {'stat': 0, 'msg': ''}
		videoID = self.__getVideoID(self.videoLink)

		if videoID :
			devid = self.__fakeCookie()
			self.tempCookie = 'Cookie: tj_lc=' + devid
			tkey = self.__auth(int(time.time()))
			confgFileUrl = self.fileUrlPrefix + 'id=' + str(videoID) + '&tkey=' + str(tkey) + '&devid=' + str(devid)
			fileUrl = self.__getVideoFileUrl(confgFileUrl)
			if fileUrl != False :
				listFile = self.__getFileList(fileUrl)
				# if len(listFile) > 0:
				# 	result['msg'] = listFile
				# else:
				# 	result['stat'] = 1
			else :
				result['stat'] = 1
		else :
			result['stat'] = 2

		return result

	def __getVideoID (self, link) :
		result = re.findall(r"vplay/(\d+?)\.html", link)
		if len(result) > 0 :
			videoID = result[0]
		else :
			videoID = False

		return videoID

	def __auth (self, now) :
		e = now
		t = 185025305
		r = t % 17
		n = e
		n = self.__letvRotate(n, r)
		o = self.__xor(n, t)

		return o

	def __getVideoFileUrl (self, confgFileUrl) :
		pageHeader, pageBody = self.Tools.getPage(confgFileUrl, [self.tempCookie])
		info = json.JSONDecoder().decode(pageBody)

		url = str(info['playurl']['domain'][0]) + str(info['playurl']['dispatch'][self.videoTypeList[self.videoType]][0])

		return url

	def __getFileList (self, fileUrl) :
		pageHeader, pageBody = self.Tools.getPage(fileUrl, ['Referer: ' + self.videoLink, 'User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4', self.tempCookie])
		if pageHeader[0] == 'HTTP/1.1 302 Moved' :
			url = ''
			for x in pageHeader :
				if x[:10] == 'Location: ' :
					url = x[10:]
					break
			pageHeader, pageBody = self.Tools.getPage(url, ['Referer: ' + self.videoLink, 'User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4', self.tempCookie])

		print pageHeader
		print pageBody

		# data = self.__formatList(data)

		# return data

	def  __formatList (self, data) :
		result = []
		temp = []
		listContent = re.findall(r"http://(.*)\s+?", data)

		for x in listContent:
			link = re.sub(r"&start=.*?&end=.*?&", self.urlSuffix, x)
			if link not in temp :
				temp.append(link)

		linkStr = ''
		for x in temp:
			result.append('http://' + x)

		return result

	def __fakeCookie (self) :
		t = ''
		for x in xrange(0,32):
			t += str(hex(int(math.floor(16 * random.random())))[2:])
			
		return t

	def __letvRotate (self, e, t) :
		for n in xrange(0,t):
			r = 1 & e
			e = self.__rotate(e, 1, 'r')
			r = self.__rotate(r, 31, 'l')
			e += r
		
		return e

	def __xor (self, x, y, base = 32) :
		stat = True
		if x >= 0 :
			x = str(bin(int(str(x), 10)))[2:]
			for i in xrange(0, base - len(x)):
				x = '0' + x
		else :
			x = str(bin(int(str(x + 1), 10)))[3:]
			for i in xrange(0, base - len(x)):
				x = '0' + x
			t = ''
			for i in xrange(0,len(x)):
				if x[i] == '1' :
					t = t + '0'
				else :
					t = t + '1'
			x = t
		if y >= 0 :
			y = str(bin(int(str(y), 10)))[2:]
			for i in xrange(0, base - len(y)):
				y = '0' + y
		else :
			y = str(bin(int(str(y + 1), 10)))[3:]
			for i in xrange(0, base - len(y)):
				y = '0' + y
			t = ''
			for i in xrange(0,len(y)):
				if y[i] == '1' :
					t = t + '0'
				else :
					t = t + '1'
			y = t
		t = ''
		for i in xrange(0, base):
			if x[i] == y[i] :
				t = t + '0'
			else :
				t = t + '1'
		x = t
		if x[0] == '1' :
			stat = False
			t = ''
			for i in xrange(0,len(x)):
				if x[i] == '1' :
					t = t + '0'
				else :
					t = t + '1'
			x = t
		r = int(str(x), 2)
		if stat == False :
			r = 0 - r - 1

		return r

	def __rotate (self, x, y, w, base = 32) :
		stat = True
		if x >= 0 :
			x = str(bin(int(str(x), 10)))[2:]
			for i in xrange(0, base - len(x)):
				x = '0' + x
		else :
			x = str(bin(int(str(x + 1), 10)))[3:]
			for i in xrange(0, base - len(x)):
				x = '0' + x
			t = ''
			for i in xrange(0,len(x)):
				if x[i] == '1' :
					t = t + '0'
				else :
					t = t + '1'
			x = t
		if y >= base :
			y = y % base
		for i in xrange (0, y) :
			x = x[0] + x + '0'
		if w == 'r' :
			x = x[0 : base]
		else :	
			x = x[(len(x) - base) : ]
		if x[0] == '1' :
			stat = False
			t = ''
			for i in xrange(0,len(x)):
				if x[i] == '1' :
					t = t + '0'
				else :
					t = t + '1'
			x = t
		r = int(str(x), 2)
		if stat == False :
			r = 0 - r - 1

		return r


# link = raw_input('URL:')
# obj = chaseSohu()
# # obj.videoLink = 'http://m.tv.sohu.com/us/0/81658605.shtml?channeled=1211010002'
# # obj.videoLink = 'http://tv.sohu.com/20151008/n422678853.shtml'
# obj.videoLink = link
# obj.videoType = 's'
# url = obj.chaseUrl()






