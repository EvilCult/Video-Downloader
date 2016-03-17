#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import math
import re
from Library import toolClass

class ChaseIqiyi :

	def __init__ (self) :
		self.videoLink     = ''
		self.infoUrl       = 'http://cache.m.iqiyi.com/jp/tmts/'
		self.infoUrlSuffix = '/?uid=&cupid=qc_100001_100103&platForm=h5&src=f45bc84a7ea643209b29a72b0c1e385f&qd_pwsz=MF8w&__jsT=sgve&type=m3u8'
		self.fileUrlPrefix = ''
		self.videoTypeList = {'n': '96', 'h': '1', 's': '2'}
		self.videoType     = 's'
		self.tempCookie    = ''
		self.Tools         = toolClass.Tools()

	def chaseUrl (self) :
		result = {'stat': 0, 'msg': ''}
		videoStrID, videoNumID = self.__getVideoID(self.videoLink)
		if videoStrID and videoNumID :
			securitykey = self.__auth(videoNumID)
			info = self.__getVideoInfo(videoNumID, videoStrID, securitykey)
			fileUrl = self.__getVideoFileUrl(info)
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
		result = re.findall(r"data-player-videoid=\"(.*?)\"", pageBody)

		if len(result) > 0 :
			videoStrID = result[0]
			result = re.findall(r"data-player-tvid=\"(.*?)\"", pageBody)
			if len(result) > 0 :
				videoNumID = result[0]
			else :
				videoNumID = False
		else :
			videoStrID = False
			videoNumID = False

		return videoStrID, videoNumID

	def __auth (self, videoID) :
		p = [1732584193, -271733879, -1732584194, 271733878]
		C = [1732584193, -271733879, -1732584194, 271733878]
		rand = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21]
		S = self.__getKeyList(videoID)

		for s in xrange (0, 64) :
			idx = [s, 5 * s + 1, 3 * s + 5, 7 * s][int(s/16)]  % 16
			if idx < len(S) :
				sRand = S[idx]
			else :
				sRand = 0
			m = self.__joinArr(self.__joinArr(p[0], [p[1] & p[2] | ~p[1] & p[3], p[3] & p[1] | ~p[3] & p[2], p[1] ^ p[2] ^ p[3], p[2] ^ (p[1] | ~p[3])][self.Tools.rotate(s, 4, 'r')]), self.__joinArr(self.Tools.xor(int(abs(math.sin(s + 1)) * 4294967296), 0), sRand))
			_ = rand[4 * int(s/16) + s % 4]

			p = [p[3], self.__joinArr(p[1], self.Tools.rotate(m, _, 'l') | self.Tools.rotate(m, 32 - _, 'r+')), p[1], p[2]]

		temp = []
		for x in xrange(0, 4):
			temp.append(self.__joinArr(p[x], C[x]))
		C = temp

		sc = ''
		for s in xrange(0,32):
			sc += hex(self.Tools.rotate(C[self.Tools.rotate(s, 1 * 3, 'r')], (self.Tools.xor(1, s) & 7) * 4, 'r') & 15)[2:]

		return sc

	def __getVideoInfo (self, videoNumID, videoStrID, securitykey) :
		requestUrl = self.infoUrl + videoNumID + '/' + videoStrID + self.infoUrlSuffix +'&qypid=' + videoNumID + '_21&sc=' + securitykey + '&t=' + self.now
		pageHeader, pageBody = self.Tools.getPage(requestUrl)

		return pageBody.replace('var tvInfoJs=', '')
			
	def __getVideoFileUrl (self, videoInfo) :
		videoInfo = json.JSONDecoder().decode(videoInfo)
		if videoInfo['code'] == 'A00000' :
			fileUrlList = videoInfo['data']['vidl']
			fileUrl = fileUrlList[0]['m3u']
			for x in fileUrlList :
				if str(x['vd']) == str(self.videoTypeList[self.videoType]) :
					fileUrl = x['m3u']
					break
		else :
			fileUrl = False

		return fileUrl

	def __getFileList (self, fileUrl) :
		pageHeader, pageBody = self.Tools.getPage(fileUrl)

		data = self.__formatList(pageBody)
		return data

	def  __formatList (self, data):
		result = []
		temp = []
		listContent = re.findall(r"(http:\/\/.*)", data)
		listContent.append('xxx')
		last = listContent[0]
		for x in listContent:
			if x.split('start=')[0] != last.split('start=')[0] :
				reg = re.compile('start=\d*')
				url = reg.sub('start=0', last)
				reg = re.compile('&contentlength=\d*')
				url = reg.sub('', url)
				temp.append(url)
			last = x
		for x in temp:
			reg = re.compile('end=(\d*)')
			length = reg.findall(x)[0]
			if int(length) > 40000000 :
				reg = re.compile('end=\d*')
				url = reg.sub('end=40000000', x)
				result.append(url)
				reg = re.compile('start=\d*')
				url = reg.sub('start=40000000', x)
				result.append(url)
			else :
				result.append(x)
		return result

	def __getKeyList(self, videoID) :
		self.now = time.time()
		self.now = str(self.now).split(".")[0] + '666'
		S = {}

		for s in xrange(0, 13):
			if self.Tools.rotate(s, 2, 'r') in S :
				S[self.Tools.rotate(s, 2, 'r')] |= self.Tools.rotate(ord(self.now[s]), 8 * (s % 4), 'l')
			else :
				S[self.Tools.rotate(s, 2, 'r')] = self.Tools.rotate(ord(self.now[s]), 8 * (s % 4), 'l')
		i = 0
		for s in xrange(13, 29):
			idx = list('56039306435353631326034343531663'[self.Tools.rotate(i, 2, 'r') * 8: self.Tools.rotate(i, 2, 'r') * 8 + 8])
			idx.reverse()
			idx = ''.join(idx)

			if self.Tools.rotate(s, 2, 'r') in S:
				S[self.Tools.rotate(s, 2, 'r')] |= self.Tools.rotate(self.Tools.xor(self.Tools.rotate(int(idx, 16), 8 * (i % 4), 'r') & 255, i % 2), self.Tools.rotate((s & 3), 3, 'l'), 'l')
			else :
				S[self.Tools.rotate(s, 2, 'r')] = self.Tools.rotate(self.Tools.xor(self.Tools.rotate(int(idx, 16), 8 * (i % 4), 'r') & 255, i % 2), self.Tools.rotate((s & 3), 3, 'l'), 'l')

			i += 1
		i = 0
		for s in xrange(29, 45):
			idx = '3766316232303631373c623b60376538'[self.Tools.rotate(i, 2, 'r') * 8: self.Tools.rotate(i, 2, 'r') * 8 + 8]

			if self.Tools.rotate(s, 2, 'r') in S :
				S[self.Tools.rotate(s, 2, 'r')] |= self.Tools.rotate(self.Tools.xor(self.Tools.rotate(int(idx, 16), 8 * (i % 4), 'r') & 255 , i % 6), self.Tools.rotate((s & 3), 3, 'l'), 'l')
			else :
				S[self.Tools.rotate(s, 2, 'r')] = self.Tools.rotate(self.Tools.xor(self.Tools.rotate(int(idx, 16), 8 * (i % 4), 'r') & 255 , i % 6), self.Tools.rotate((s & 3), 3, 'l'), 'l')

			i += 1
		i = 0
		for s in xrange(45, 54):
			idx = videoID

			if self.Tools.rotate(s, 2, 'r') in S :
				S[self.Tools.rotate(s, 2, 'r')] |= self.Tools.rotate(ord(idx[i]), 8 * (s % 4), 'l')
			else :
				S[self.Tools.rotate(s, 2, 'r')] = self.Tools.rotate(ord(idx[i]), 8 * (s % 4), 'l')

			i += 1
		s = 54
		if self.Tools.rotate(s, 2, 'r') in S :
			S[self.Tools.rotate(s, 2, 'r')] |= self.Tools.rotate(1, self.Tools.rotate(s % 4, 3, 'l') + 7, 'l')
		else :
			S[self.Tools.rotate(s, 2, 'r')] = self.Tools.rotate(1, self.Tools.rotate(s % 4, 3, 'l') + 7, 'l')
		S[self.Tools.rotate(self.Tools.rotate(s + 8, 6, 'r'), 4, 'l') + 14] = self.Tools.rotate(s, 3, 'l')

		return S	

	def __joinArr (self, num1, num2) :
		result = self.Tools.rotate(self.Tools.rotate(num1, 1, 'r') + self.Tools.rotate(num2, 1, 'r'), 1, 'l') + (num1 & 1) + (num2 & 1)

		return result