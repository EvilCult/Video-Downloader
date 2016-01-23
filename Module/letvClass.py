#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import random
import math
import time
import sys
sys.path.append("..")
from Library import toolClass

class ChaseLetv :

	def __init__ (self) :
		self.videoLink     = ''
		self.fileUrlPrefix = 'http://api.letv.com/mms/out/video/playJson?platid=1&splatid=101&domain=www.letv.com'
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
				listFile = self.__getFileList(fileUrl)
				# if len(listFile) > 0:
				# 	result['msg'] = listFile
				# else:
				# 	result['stat'] = 1
			# else :
			# 	result['stat'] = 1
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
		url = str(info['playurl']['domain'][0]) + str(info['playurl']['dispatch'][self.videoTypeList[self.videoType]][0]) + '&format=1&sign=letv&expect=3000&rateid=' + self.videoTypeList[self.videoType]

		return url

	def __getFileList (self, fileUrl) :
		pageHeader, pageBody = self.Tools.getPage(fileUrl)
		info = json.JSONDecoder().decode(pageBody)
		# if pageHeader[0] == 'HTTP/1.1 302 Moved' :
		# 	url = ''
		# 	for x in pageHeader :
		# 		if x[:10] == 'Location: ' :
		# 			url = x[10:]
		# 			break
		# 	pageHeader, pageBody = self.Tools.getPage(url)

		pageHeader, pageBody = self.Tools.getPage(info['location'])
		return pageBody

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

	def __letvRor (self, a, b):
		i = 0
		while(i < b) :
			a = self.Tools.rotate(a, 1, 'r+') + self.Tools.rotate((a & 1), 31, 'l');
			i += 1

		return a;