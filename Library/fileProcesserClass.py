#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import os
import time
import threading

class FileProcesser :

	def __init__ (self) :
		self.fileUrl = ''
		self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
		self.saveName = ''
		self.fileID = 0
		self.process = ''
		self.chunk = 4096

	def download (self, url, savePath = '') :
		if savePath != '' :
			self.savePath = savePath
		else :
			self.savePath = self.__makeSavePath()

		self.process = '准备中...'
		self.fileUrl = url
		self.saveName = time.strftime("%Y%m%d%H%M%S")
		p = threading.Thread(target = self.__downloadFile)
		p.start()

	def __downloadFile (self) :
		self.fileID = 1
		for url in self.fileUrl:
			try:
				request = urllib2.Request(url)
				request.add_header('User-Agent', self.ua)
				request.add_header('Range', 'bytes=0-')
				response = urllib2.urlopen(request)

				pageInfo = response.info()
				fileLength = pageInfo.getheader('Content-Length').strip()
				cType = pageInfo.getheader('Content-Type').strip()

				if 'flv' in cType :
					self.fileType = '.flv'
				elif 'mp4' in cType:
					self.fileType = '.mp4'
				else :
					self.fileType = '.mp4'

				chunkIdx = 1
				while True:
					data = response.read(self.chunk)

					if data :
						with open(self.savePath + '/' + self.saveName + '_' + str(self.fileID) + self.fileType,'a+') as f:
							f.write(data)

						percent = int(chunkIdx * self.chunk * 100 / int(fileLength))
						self.process = "正在下载视频" + str(self.fileID) + " - " + "%d%%" % percent
						chunkIdx += 1
					else :
						self.process = '下载完成'
						break
			except Exception, e:
				self.process = "下载失败"
				exit()

			self.fileID += 1

	def __report(self, count, blockSize, totalSize):
		percent = int(count * blockSize * 100 / totalSize)
		self.process = "正在下载视频" + str(self.fileID) + " - " + "%d%%" % percent

	def __makeSavePath (self) :
		sysPath = self.__findSysPath()
		folder = 'VideoDownloader'
		savePath = os.path.join(sysPath, folder)
		if not os.path.isdir(savePath):
			os.makedirs(savePath)

		return savePath

	def __findSysPath (self) :
		return os.path.join(os.path.expanduser("~"), 'Desktop')
