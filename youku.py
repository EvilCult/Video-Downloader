#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pycurl
import StringIO
import json
import hashlib
import struct
import base64
import urllib
import re

class chaseYouku :

	def __init__ (self) :
		self.youkuLink     = ''
		self.cookieUrl     = 'http://p.l.youku.com/ypvlog'
		self.infoUrl       = 'http://play.youku.com/play/get.json?ct=12&vid='
		self.fileUrlPrefix = 'http://pl.youku.com/playlist/m3u8?ctype=12&ev=1&keyframe=1'
		self.videoType     = 'mp4' # mp4:高清; flv:标清; hd2:超清; hd3:1080p
		self.tempCookie    = ''

	def chaseUrl (self) :
		videoID = self.__getVideoID(self.youkuLink)
		if videoID :
			self.__auth()
			info, r_key = self.__getVideoInfo(videoID)
			fileUrl = self.__getVideoFileUrl(info, r_key)
			listFile = self.__getFileList(fileUrl)
			if len(listFile) > 0:
				result = listFile
			else:
				result = '网络繁忙，稍后重试'
		else :
			result = 'URL不正确'

		return result

	def __getVideoID(self, link):
		result = re.findall(r"id_(.*)==\.html", link)
		if len(result) > 0 :
			videoID = result[0]
		else :
			videoID = False

		return videoID

	def __auth (self) :
		resultFormate = StringIO.StringIO()
		curl = pycurl.Curl()
		curl.setopt(pycurl.URL, self.cookieUrl)
		curl.setopt(pycurl.ENCODING, 'gzip,deflate')
		curl.setopt(pycurl.HEADER, 1)
		curl.setopt(pycurl.TIMEOUT, 10)
		curl.setopt(pycurl.WRITEFUNCTION, resultFormate.write)
		curl.perform()
		headerSize = curl.getinfo(pycurl.HEADER_SIZE)
		curl.close()
		cookieHeader = resultFormate.getvalue()[0:headerSize].split('\r\n')

		ysuid = ''
		for i in cookieHeader:
			if i[12:19] == '__ysuid' :
				ysuid = i[20:]
				break

		if ysuid :
			ysuid = ysuid[0 : ysuid.find(';')];
			self.tempCookie = 'Cookie: __ysuid=' + ysuid + ';';	

	def __getVideoInfo (self, videoID) :
		resultFormate = StringIO.StringIO()
		url = self.infoUrl + videoID
		curl = pycurl.Curl()
		curl.setopt(pycurl.URL, url)
		curl.setopt(pycurl.ENCODING, 'gzip,deflate')
		curl.setopt(pycurl.HEADER, 1)
		curl.setopt(pycurl.TIMEOUT, 10)
		curl.setopt(pycurl.HTTPHEADER, ['Referer: http://v.youku.com/v_show/' + videoID + '.html?x', self.tempCookie])
		curl.setopt(pycurl.WRITEFUNCTION, resultFormate.write)
		curl.perform()
		headerSize = curl.getinfo(pycurl.HEADER_SIZE)
		curl.close()
		tempHeader = resultFormate.getvalue()[0 : headerSize].split('\r\n')
		info = resultFormate.getvalue()[headerSize : ]

		header = {}
		for i in tempHeader:
			temp = i.split(': ')
			if len(temp) > 1 :
				header[temp[0]] = temp[1]
			else :
				header[temp[0]] = ''


		self.tempCookie = header['Set-Cookie'].split('; ')
		r_key = self.tempCookie[0][3 : ]

		return info, r_key
			
	def __getVideoFileUrl (self, videoInfo, r_key) :
		videoInfo = json.JSONDecoder().decode(videoInfo)
		ep = videoInfo['data']['security']['encrypt_string']

		if ep :
			oip   = videoInfo['data']['security']['ip']
			vid   = videoInfo['data']['id']
			temp  = self.__yk_e('becaf9be', base64.decodestring(ep))
			sid   = temp.split('_')[0]
			token = temp.split('_')[1]
			ep    = urllib.quote(base64.encodestring(self.__yk_e('bf7e5f01', str(sid) + '_' + str(vid) + '_' + str(token))))

			fileUrl = self.fileUrlPrefix + '&ep=' + str(ep) + '&oip=' + str(oip) + '&sid=' + str(sid) + '&token=' + str(token) + '&vid=' + str(vid) + '&type=' + self.videoType
			self.tempCookie[0] = 'r=""' + urllib.quote(r_key) + '""'
		else :
			fileUrl = False

		return fileUrl

	def __getFileList (self, fileUrl) :
		resultFormate = StringIO.StringIO()
		url = fileUrl
		curl = pycurl.Curl()
		curl.setopt(pycurl.URL, url)
		curl.setopt(pycurl.ENCODING, 'gzip,deflate')
		curl.setopt(pycurl.TIMEOUT, 10)
		curl.setopt(pycurl.HTTPHEADER, ['Referer:', self.tempCookie[0]])
		curl.setopt(pycurl.WRITEFUNCTION, resultFormate.write)
		curl.perform()
		curl.close()

		data = resultFormate.getvalue()
		data = self.__formatList(data)
		return data

	def  __formatList (self, data):
		result = []
		listContent = re.findall(r"(.*)\.ts\?", data)
		for x in listContent:
			if x not in result :
				result.append(x)
		print result

	def __yk_e (self, a, c) : 
		f = i = h =0
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




obj = chaseYouku()
obj.youkuLink = raw_input("URL: ")
url = obj.chaseUrl()






