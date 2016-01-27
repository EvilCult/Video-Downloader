#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from Library import toolClass

class ChaseTudou :

	def __init__ (self) :
		self.videoLink     = ''
		self.fileUrlPrefix = 'http://vr.tudou.com/v2proxy/v2.m3u8?it='
		self.urlSuffix     = '&s=0&e=10000000000'
		self.videoTypeList = {'n': 'mp4', 'h': 'mp4', 's': 'mp4'}
		self.videoType     = self.videoTypeList['h']
		self.Tools         = toolClass.Tools()

	def chaseUrl (self) :
		result = {'stat': 0, 'msg': ''}
		videoID = self.__getVideoID(self.videoLink)

		if videoID :
			fileUrl = self.fileUrlPrefix + str(videoID)
			listFile = self.__getFileList(fileUrl)
			if len(listFile) > 0:
				result['msg'] = listFile
			else:
				result['stat'] = 1
		else :
			result['stat'] = 2

		return result

	def __getVideoID(self, link):
		pageHeader, pageBody = self.Tools.getPage(link)

		result = re.findall(r",iid: (.*)", pageBody)
		if len(result) > 0 :
			videoID = result[0]
		else :
			videoID = False

		return videoID

	def __getFileList (self, fileUrl) :
		pageHeader, pageBody = self.Tools.getPage(fileUrl)

		data = self.__formatList(pageBody)
		
		return data

	def  __formatList (self, data):
		result = []
		temp = []
		listContent = re.findall(r"(.*)&s=0&e=", data)
		for x in listContent:
			if x not in temp :
				temp.append(x)

		linkStr = ''
		for x in temp:
			result.append(x + self.urlSuffix)

		return result