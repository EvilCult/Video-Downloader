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
		self.infoUrl       = 'http://play.youku.com/play/get.json?ct=12&vid='
		self.fileUrlPrefix = 'http://pl.youku.com/playlist/m3u8?ctype=12&ev=1&keyframe=0'
		self.videoTypeList = {'n': 'mp4hd', 'h': 'mp4hd2', 's': 'mp4hd3'}
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
				if fileUrl != False :
					listFile = self.__getFileList(fileUrl)
					if len(listFile) > 0:
						result['stat'] = 0
						result['msg'] = listFile
					else :
						result['msg'] = self.err.show(2)
				else :
					result['msg'] = self.err.show(4)
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
		if 'security' in videoInfo['data']:
			ep = videoInfo['data']['security']['encrypt_string']
		else :
			ep = False

		if ep :
			oip   = videoInfo['data']['security']['ip']
			vid   = videoInfo['data']['video']['encodeid']

			temp  = self.__rc4('becaf9be', base64.decodestring(ep))
			sid   = temp.split('_')[0]
			token = temp.split('_')[1]

			typeInfo = self.__getTypeCode(self.videoTypeList[self.videoType], videoInfo['data']['stream'])

			if typeInfo['videoTypeCode'] != '' :
				ep = urllib.quote(base64.encodestring(self.__rc4('bf7e5f01', str(sid) + '_' + str(typeInfo['videoTypeCode']) + '_' + str(token))), '')
				fileUrl = self.fileUrlPrefix + '&ep=' + str(ep) + '&oip=' + str(oip) + '&sid=' + str(sid) + '&token=' + str(token) + '&vid=' + str(vid) + '&type=' + typeInfo['videoType'] + '&ts=' + str(self.now)
			else :
				fileUrl = False
		else :
			fileUrl = False

		return fileUrl

	def __getFileList (self, fileUrl) :
		pageHeader, pageBody = self.Tools.getPage(fileUrl)

		data = self.__formatList(pageBody)
		return data

	def  __formatList (self, data) :
		result = []
		listContent = re.findall(r"(.*)\.ts\?", data)
		for x in listContent:
			if x not in result :
				result.append(x)
		return result

	def __getTypeCode (self, videoType, data) :
		typeCode = ''
		for info in data :
			if info['stream_type'] == videoType :
				typeCode = info['segs'][-1]['fileid']
				break

		if videoType == 'mp4hd':
			typeName = 'mp4'
		elif videoType == 'mp4hd2':
			typeName = 'hd2'
		elif videoType == 'mp4hd3':
			typeName = 'hd3'
		else :
			typeName = 'mp4'			

		result = {
			'videoType': typeName,
			'videoTypeCode': typeCode
		}
		return result

	def __rc4 (self, a, c) :
		f = h = 0
		b = list(range(256))
		result = ''
 
		while h < 256:
			f = (f + b[h] + ord(a[h % len(a)])) % 256
			b[h], b[f] = b[f], b[h]
			h += 1
		q = f = h = 0
 
		while q < len(c):
			h = (h + 1) % 256
			f = (f + b[h]) % 256
			b[h], b[f] = b[f], b[h]
			if isinstance(c[q], int):
				result += chr(c[q] ^ b[(b[h] + b[f]) % 256])
			else:
				result += chr(ord(c[q]) ^ b[(b[h] + b[f]) % 256])
			q += 1

		return result