#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import random
import math
import time
from Library import toolClass

class ChaseBilibili :

	def __init__ (self) :
		self.videoLink     = ''
		self.fileUrlPrefix = 'http://www.bilibili.com/m/html5'

		self.videoTypeList = {'n': '2', 'h': '1', 's': '0'}
		self.videoType     = 's'
		self.Tools         = toolClass.Tools()

	def chaseUrl (self) :
		result = {'stat': 0, 'msg': ''}
		videoInfo = self.__getVideoID(self.videoLink)

		if videoInfo['videoID'] :
			confgFileUrl = self.fileUrlPrefix + '?aid=' + str(videoInfo['videoID']) + '&page=' + str(videoInfo['page'])
			fileUrl = self.__getFile(confgFileUrl)
			if fileUrl != '':
				result['msg'] = fileUrl
			else:
				result['stat'] = 1
		else :
			result['stat'] = 2

		return result

	def __getVideoID (self, link) :
		result = re.findall(r"/av(\d*)", link)
		if len(result) > 0 :
			videoID = result[0]
		else :
			videoID = False

		result = re.findall(r"/index_(\d*)\.html", link)
		if len(result) > 0 :
			page = result[0]
		else :
			page = 1

		result = {
			'videoID': videoID,
			'page': page
		}

		return result

	def __getFile (self, confgFileUrl) :
		pageHeader, pageBody = self.Tools.getPage(confgFileUrl)
		info = json.JSONDecoder().decode(pageBody)

		url = [info['src']]

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