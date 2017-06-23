#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import hashlib
import base64
import urllib
import re
import time
from Library import toolClass
from Library import errMsgClass

class ChaseYouku :

	def __init__ (self) :
		self.videoLink     = ''
		self.infoUrl       = 'https://ups.youku.com/ups/get.json?&ccode=0501&client_ip=0.0.0.0&client_ts=1529741351&utid=QM7jEAtFLzkCAdr3tQK%2BqDe4&vid='
		self.fileUrlPrefix = 'http://pl.youku.com/playlist/m3u8?ctype=12&ev=1&keyframe=0'
		self.videoTypeList = {'n': 'flvhd', 'h': 'mp4hd', 's': 'mp4hd2'}
		self.videoType     = 's'
		self.Tools         = toolClass.Tools()
		self.now           = int(time.time())
		self.err           = errMsgClass.ErrMsg()

	def chaseUrl (self) :
		result = {'stat': 1, 'msg': ''}

		videoID = self.__getVideoID(self.videoLink)
		if videoID :
			info = self.__getVideoInfo(videoID)
			if info != False :
				fileUrl = self.__getVideoFileUrl(info)
				if len(fileUrl) > 0 :
					if self.videoTypeList[self.videoType] in fileUrl :
						result['stat'] = 0
						result['msg'] = fileUrl[self.videoTypeList[self.videoType]]
					else :
						result['msg'] = self.err.show(4)
				else :
					result['msg'] = self.err.show(2)
			else :
				result['msg'] = self.err.show(3)
		else :
			result['msg'] = self.err.show(1)

		return result

	def __getVideoID(self, link):
		result = re.findall(r"id_(.*?==)", link)
		if len(result) > 0 :
			videoID = result[0]
		else :
			result = re.findall(r"id_(.*?)\.html", link)
			if len(result) > 0 :
				videoID = result[0] + "=="
			else :
				videoID = False

		return videoID

	def __getVideoInfo (self, videoID) :
		try:
			pageHeader, pageBody = self.Tools.getPage(self.infoUrl + videoID, ['Referer:http://c-h5.youku.com/'])
			if pageBody == '' :
				pageBody = False
		except:
			pageBody = False

		return pageBody
			
	def __getVideoFileUrl (self, videoInfo) :
		videoInfo = json.JSONDecoder().decode(videoInfo)

		if 'stream' in videoInfo['data'] :
			temp = {}
			for x in videoInfo['data']['stream'] :
				temp[x['stream_type']] = []
				for url in x['segs'] :
					if url['key'] != '-1' : 
						temp[x['stream_type']].append(url['cdn_url'])

		if len(temp) > 0 :
			fileUrl = temp
		else :
			fileUrl = False

		return fileUrl