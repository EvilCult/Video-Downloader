#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import os
import time
import threading

class FileProcesser :

	def __init__ (self) :
		self.fileUrl = ''
		self.savePath = self.__makeSavePath()
		self.saveName = ''
		self.fileID = 0
		self.process = ''

	def download (self, url) :
		self.process = '准备中...'
		self.fileUrl = url
		self.saveName = time.strftime("%Y%m%d%H%M%S")
		p = threading.Thread(target = self.__downloadFile)
		p.start()

	def __downloadFile (self) :
		self.fileID = 1
		for url in self.fileUrl:
			target = urllib.urlopen(url)
			header = str(target.info()).split('\n')
			for x in header :
				if x[0:12] == 'Content-Type' :
					cType = x[14:]
					break
			if cType == 'video/x-flv' :
				fileType = '.flv'
			elif cType == 'video/mp4':
				fileType = '.mp4'
			else :
				fileType = '.mp4'				
			urllib.urlretrieve(url, self.savePath + '/' + self.saveName + '_' + str(self.fileID) + fileType, reporthook = self.__report)
			self.fileID += 1
		self.process = '下载完成'

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






