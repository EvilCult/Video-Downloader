#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import hashlib
import base64
import urllib
import re
from Library import toolClass

class ChaseAcfun :

	def __init__ (self) :
		self.videoLink     = ''
		self.infoUrl       = 'http://api.aixifan.com/plays/'
		self.infoUrlSuffix = '/realSource'
		self.fileUrlPrefix = 'http://pl.youku.com/playlist/m3u8?ctype=12&ev=1&keyframe=1'
		self.videoTypeList = {'n': '', 'h': '', 's': ''}
		self.videoType     = 's'
		self.tempCookie    = ''
		self.Tools         = toolClass.Tools()

	def chaseUrl (self) :
		result = {'stat': 0, 'msg': ''}
		videoID = self.__getVideoID(self.videoLink)
		if videoID :
			info = self.__getVideoInfo(videoID)
			fileUrl = self.__getVideoFileUrl(info)
			fileList = self.__getFile(fileUrl)
			if len(fileList) > 0:
				result['msg'] = fileList
			else:
				result['stat'] = 1
		else :
			result['stat'] = 2

		return result

	def __getVideoID(self, link):
		pageHeader, pageBody = self.Tools.getPage(link)

		result = re.findall(r"data-vid=\"(\d*)\"", pageBody)
		if len(result) > 0 :
			videoID = result[0]
		else :
			videoID = False

		return videoID

	def __getVideoInfo (self, videoID) :
		pageHeader, pageBody = self.Tools.getPage(self.infoUrl + videoID + self.infoUrlSuffix, ['deviceType:2', 'User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'])

		return pageBody
			
	def __getVideoFileUrl (self, videoInfo) :
		videoInfo = json.JSONDecoder().decode(videoInfo)
		if 'data' in videoInfo:
			fileList = videoInfo['data']['files']
		else :
			fileList = False

		if fileList :
			fileUrl = False

			if self.videoType == 's' :
				fileCode = 4
			elif self.videoType == 'h' :
				fileCode = 3
			elif self.videoType == 'n' :
				fileCode = 2
			else :
				fileCode = 4

			for item in fileList:
				if item['code'] == fileCode :
					fileUrl = item['url']
					break
		else :
			fileUrl = False

		return fileUrl

	def __getFile (self, fileUrl) :
		data = []
		for url in fileUrl :
			pageHeader, pageBody = self.Tools.getPage(url)
			if 'HTTP/1.1 302' in pageHeader[0] :
				for x in pageHeader :
					if x[:10] == 'Location: ' :
						data.append(x[10:])
						break

		return data

	def  __formatList (self, data):
		result = []
		listContent = re.findall(r"(.*)\.ts\?", data)
		for x in listContent:
			if x not in result :
				result.append(x)
		return result

	def __yk_e (self, a, c) : 
		f = 0
		i = 0
		h = 0
		b = {}
		e = ''
		for h in xrange(0, 256) :
			b[h] = h;

		for h in xrange(0, 256) :
			f = ((f + b[h]) + self.__charCodeAt(a, h % len(a))) % 256;
			i = b[h]
			b[h] = b[f]
			b[f] = i

		f = h = 0
		for q in xrange(0, len(c)) :
			h = (h + 1) % 256
			f = (f + b[h]) % 256
			i = b[h]
			b[h] = b[f]
			b[f] = i
			e = e + self.__fromCharCode(self.__charCodeAt(c, q) ^ b[(b[h] + b[f]) % 256]);

		return e

	def __charCodeAt (self, data, index) :
		charCode = {}
		md5 = hashlib.md5() 
		md5.update(data) 
		key = md5.hexdigest()

		return ord(data[index])

	def __fromCharCode (self, codes) :
		return chr(codes)