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
		self.fileUrlPrefix = 'http://interface.bilibili.com/playurl?player=2&sign=5b790eb0d593597d1964425c4d9691df&otype=json'

		self.videoTypeList = {'n': '2', 'h': '1', 's': '0'}
		self.videoType     = 's'
		self.Tools         = toolClass.Tools()

	def chaseUrl (self) :
		result = {'stat': 0, 'msg': ''}
		videoID = self.__getVideoID(self.videoLink)

		if videoID :
			confgFileUrl = self.fileUrlPrefix + '&cid=' + str(videoID) + '&ts=' + str(int(time.time()))
			fileUrl = self.__getFile(confgFileUrl)
			if fileUrl != '' > 0:
				result['msg'] = fileUrl
			else:
				result['stat'] = 1
		else :
			result['stat'] = 2

		return result

	def __getVideoID (self, link) :
		pageHeader, pageBody = self.Tools.getPage(link)
		result = re.findall(r"cid=(\d*)", pageBody)
		if len(result) > 0 :
			videoID = result[0]
		else :
			videoID = False

		return videoID

	def __getFile (self, confgFileUrl) :
		pageHeader, pageBody = self.Tools.getPage(confgFileUrl)
		info = json.JSONDecoder().decode(pageBody)

		url = []
		if 'durl' in info :
			for item in info['durl']:
				if self.videoType == 's' :
					if 'backup_url' in item :
						url.append(item['backup_url'][0])
					else :
						url.append(item['url'])
				elif self.videoType == 'h' :
					if 'backup_url' in item :
						if len(item['backup_url']) > 1:
							url.append(item['backup_url'][1])
						else :
							url.append(item['backup_url'][0])
					else :
						url.append(item['url'])
				elif self.videoType == 'n' :
					url.append(item['url'])

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