#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import random
import math
import time
from Library import toolClass
from Library import errMsgClass

class ChaseBilibili :

	def __init__ (self) :
		self.videoLink     = ''
		self.fileUrlPrefix = 'http://api.bilibili.com/playurl'

		self.videoTypeList = {'n': '0', 'h': '1', 's': '2'}
		self.videoType     = 's'
		self.Tools         = toolClass.Tools()
		self.err           = errMsgClass.ErrMsg()

	def chaseUrl (self) :
		result = {'stat': 1, 'msg': ''}
		videoIDList = self.__getVideoID(self.videoLink)

		if videoIDList['videoID'] :
			confgFileUrl = self.fileUrlPrefix + '?aid=' + str(videoIDList['videoID']) + '&page=' + str(videoIDList['page']) + '&vtype=hdmp4'
			videoUrl = self.__getVideoInfo(confgFileUrl)
			if videoUrl != False:
				fileUrl = self.__getFile(videoUrl)
				if fileUrl != '':
					result['stat'] = 0
					result['msg'] = fileUrl
				else:
					result['msg'] = self.err.show(2)
			else :
				result['msg'] = self.err.show(4)
		else :
			result['msg'] = self.err.show(1)

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

	def __getVideoInfo (self, confgFileUrl) :
		try:
			pageHeader, pageBody = self.Tools.getPage(confgFileUrl)
			info = json.JSONDecoder().decode(pageBody)

			urlList = [
				info['durl'][0]['url']
			]
			for x in xrange(0, len(info['durl'][0]['backup_url'])):
				urlList.append(info['durl'][0]['backup_url'][x])

			if int(self.videoTypeList[self.videoType]) <= len(urlList) - 1 :
				url = urlList[int(self.videoTypeList[self.videoType])]
			else :
				url = False
		except:
			url = False

		return url

	def __getFile (self, fileUrl) :
		try:
			pageHeader, pageBody = self.Tools.getPage(fileUrl)
			for param in pageHeader:
				if param[:8] == 'Location' :
					url = [param[10:]]
					break
		except:
			url = ''

		return url