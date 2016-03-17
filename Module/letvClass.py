#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import random
import math
import time
from Library import toolClass

class ChaseLetv :

	def __init__ (self) :
		self.videoLink     = ''
		self.fileUrlPrefix = 'http://api.letv.com/mms/out/video/playJson?platid=1&splatid=104&tss=no&domain=www.letv.com'
		self.urlSuffix     = '&start=0&end=10000000000&'
		self.videoTypeList = {'n': '1000', 'h': '1300', 's': '720p'}
		self.videoType     = 's'
		self.Tools         = toolClass.Tools()

	def chaseUrl (self) :
		result = {'stat': 0, 'msg': ''}
		videoID = self.__getVideoID(self.videoLink)

		if videoID :
			tkey = self.__auth(time.time())
			confgFileUrl = self.fileUrlPrefix + '&id=' + str(videoID) + '&tkey=' + str(tkey)
			fileUrl = self.__getVideoFileUrl(confgFileUrl)
			if fileUrl != False :
				fileUrl = self.__getFile(fileUrl)
				if fileUrl != '' > 0:
					result['msg'] = [fileUrl]
				else:
					result['stat'] = 1
			else :
				result['stat'] = 1
		else :
			result['stat'] = 2

		return result

	def __getVideoID (self, link) :
		result = re.findall(r"/(\d+?)\.html", link)
		if len(result) > 0 :
			videoID = result[0]
		else :
			videoID = False

		return videoID

	def __auth (self, now) :
		key = 773625421
		now = int (now)
		result = self.__letvRor(now, key % 13)
		result = self.Tools.xor(result, key)
		result = self.__letvRor(result ,key % 17)

		return result

	def __getVideoFileUrl (self, confgFileUrl) :
		pageHeader, pageBody = self.Tools.getPage(confgFileUrl)

		info = json.JSONDecoder().decode(pageBody)
		# url = str(info['playurl']['domain'][0]) + str(info['playurl']['dispatch'][self.videoTypeList[self.videoType]][0]) + '&format=1&sign=letv&expect=3000&rateid=' + self.videoTypeList[self.videoType]
		url = str(info['playurl']['domain'][0]) + str(info['playurl']['dispatch'][self.videoTypeList[self.videoType]][0])
		url = url.replace('tss=ios', 'tss=no')
		url = url.replace('splatid=101', 'splatid=104')

		return url

	def __getFile (self, fileUrl) :
		pageHeader, pageBody = self.Tools.getPage(fileUrl)

		url = ''
		if pageHeader[0] == 'HTTP/1.1 302 Moved' :
			for x in pageHeader :
				if x[:10] == 'Location: ' :
					url = x[10:]
					break

		return url

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

	def __letvRor (self, a, b):
		i = 0
		while(i < b) :
			a = self.Tools.rotate(a, 1, 'r+') + self.Tools.rotate((a & 1), 31, 'l');
			i += 1

		return a