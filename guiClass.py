#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import ttk 
import tkMessageBox
import os
import sys
import threading
from Module import youkuClass
from Module import tudouClass
from Module import sohuClass
from Module import letvClass
from Module import bilibiliClass
from Module import acfunClass
from Module import iqiyiClass
from Library import fileProcesserClass

class GUI :

	def __init__ (self) :
		self.masterTitle = 'Video Downloader'
		self.slaveTitle = 'Info'
		self.fileList = []

	def __mainWindow (self) :
		self.master = Tkinter.Tk();

		self.master.title(self.masterTitle)
		self.master.resizable(width = 'false', height = 'false')

		self.__menu()
		self.__topBox()

	def __menu (self) :
		menubar = Tkinter.Menu(self.master)

		filemenu = Tkinter.Menu(menubar, tearoff = 0)
		filemenu.add_command(label = "Info", command = self.__showInfo)
		filemenu.add_command(label = "Quit", command = self.master.quit)
		menubar.add_cascade(label = "About", menu = filemenu)

		self.master.config(menu = menubar)

	def __topBox (self) :
		self.mainTop = Tkinter.Frame(self.master, bd = 10)
		self.mainTop.grid(row = 0, column = 0, sticky = '')		

		self.urlInput = Tkinter.Entry(self.mainTop, width = 50)
		self.urlInput.grid(row = 0, column = 0)

		s = self.__selector(self.mainTop)
		s.grid(row = 0, column = 1)

		self.__searchBtn()


	def __selector (self, position) :
		self.selectorVal = Tkinter.StringVar()
		self.selectorVal.set("HD")

		videoType = ['HD', '超清', '高清']

		s = ttk.Combobox(position, width = 5, textvariable = self.selectorVal, state='readonly', values = videoType)

		return s	

	def __showResult (self) :
		self.mainFoot = Tkinter.Frame(self.master, bd = 10)
		self.mainFoot.grid(row = 1, column = 0, sticky = '')		

		self.__searchBtn(False)
		self.resultWindow = Tkinter.Text(self.mainFoot, height = 5, width = 70, highlightthickness = 0)
		self.resultWindow.grid(row = 0, sticky = '')

		threading.Thread(target = self.__getUrl).start()

		self.dlZone = Tkinter.Button(self.mainFoot, text = '下载', command = self.__download)
		self.dlZone.grid(row = 1, column = 0, sticky = 'ew')

		self.mainFoot.update()

	def __getUrl (self):
		url = self.urlInput.get()
		result = True
		if 'youku' in url :
			getClass = youkuClass.ChaseYouku()
		elif 'sohu' in url :
			getClass = sohuClass.ChaseSohu()
		elif 'letv' in url :
			getClass = letvClass.ChaseLetv()
		elif 'tudou' in url and 'acfun' not in url :
			getClass = tudouClass.ChaseTudou()
		elif 'bilibili' in url :
			getClass = bilibiliClass.ChaseBilibili()
		elif 'acfun' in url :
			getClass = acfunClass.ChaseAcfun()
		elif 'iqiyi' in url :
			getClass = iqiyiClass.ChaseIqiyi()
		else :
			result = False

		if result :
			result = ''
			videoType = self.selectorVal.get()

			if videoType == u'HD' :
				videoType = 's'
			elif videoType == u'超清' :
				videoType = 'h'
			elif videoType == u'高清' :
				videoType = 'n'
			else :
				videoType = 's'

			getClass.videoLink = url
			getClass.videoType = videoType
			urlList = getClass.chaseUrl()

			if urlList['stat'] == 0 :
				self.fileList = urlList['msg']
				i = 1
				for x in urlList['msg']:
					result += '第' + str(i) + '段:\n' + str(x) + '\n'
					i += 1
			else :
				result = urlList['msg']

		else :
			result = '链接地址不再分析范围内！'

		self.resultWindow.insert('end', result)

		self.__searchBtn()

	def __download (self) :
		self.FPC = fileProcesserClass.FileProcesser()
		if len(self.fileList) > 0 :
			self.dlZone.grid_forget()
			self.dlStat = Tkinter.StringVar()
			self.dlZone = Tkinter.Label(self.mainFoot, textvariable = self.dlStat, width = 30, anchor = 'center')
			self.dlZone.grid(row = 1, column = 0, sticky = 'ew')

			self.FPC.download(self.fileList)
			self.__dlZoneUpdate()

	def __dlZoneUpdate (self) :
		self.dlStat.set(self.FPC.process)

		self.timer = self.master.after(1000, self.__dlZoneUpdate)

	def __searchBtn (self, stat = True) :
		if stat :
			self.sBtn = Tkinter.Button(self.mainTop, text = '搜索', width = 10, command = self.__showResult)
			self.sBtn.grid(row = 0, column = 2)
		else :
			self.sBtn = Tkinter.Button(self.mainTop, text = '分析中...', width = 10, command = '')
			self.sBtn.grid(row = 0, column = 2)


	def __showInfo(self):
		self.slave = Tkinter.Tk();

		self.slave.title(self.slaveTitle)
		self.slave.resizable(width = 'false', height = 'false')

		info = [
			'Support: www.youku.com\nwww.tudou.com\ntv.sohu.com\nwww.letv.com\nwww.bilibili.com\nwww.acfun.tv',
			'Website: https://github.com/EvilCult/Video-Downloader'
		]

		label = Tkinter.Label(self.slave, text="Video Downloader", font = ("Helvetica", "16", 'bold'), anchor = 'center')
		label.grid(row = 0)

		information = Tkinter.Text(self.slave, height = 10, width = 30, highlightthickness = 0)
		information.grid(row = 1, padx = 10, pady = 5)
		for n in info :
			information.insert('end', n.split(': ')[0] + '\n')
			information.insert('end', n.split(': ')[1] + '\r')

		label = Tkinter.Label(self.slave, text="Version: Beta 0.9.1", font = ("Helvetica", "10"), anchor = 'center')
		label.grid(row = 2)
		label = Tkinter.Label(self.slave, text="Author: Ray H.", font = ("Helvetica", "10"), anchor = 'center')
		label.grid(row = 3)

	def run (self) :
		self.__mainWindow()
		self.master.mainloop()