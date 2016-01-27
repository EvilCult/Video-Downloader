#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import ttk 
import tkMessageBox
import os
import sys
import youkuClass
import tudouClass
import sohuClass
import letvClass

class GUI :

	def __init__ (self) :
		self.masterTitle = 'Video Downloader'
		self.slaveTitle = 'Setting'

	def __mainWindow (self) :
		self.master = Tkinter.Tk();

		self.master.title(self.masterTitle)
		self.master.resizable(width = 'false', height = 'false')

		self.__menu()
		self.__topBox()

	def __menu (self) :
		menubar = Tkinter.Menu(self.master)

		filemenu = Tkinter.Menu(menubar, tearoff = 0)
		filemenu.add_command(label = "设置", command = '')
		filemenu.add_command(label = "退出程序", command = self.master.quit)
		menubar.add_cascade(label = "Setting", menu = filemenu)

		self.master.config(menu = menubar)

	def __topBox (self) :
		self.mainTop = Tkinter.Frame(self.master, bd = 10)
		self.mainTop.grid(row = 0, column = 0, sticky = '')		

		self.urlInput = Tkinter.Entry(self.mainTop, width = 50)
		self.urlInput.grid(row = 0, column = 0)

		s = self.__selector(self.mainTop)
		s.grid(row = 0, column = 1)

		b = Tkinter.Button(self.mainTop, text = '搜索', command = self.__showResult)
		b.grid(row = 0, column = 2)

	def __selector (self, position) :
		self.selectorVal = Tkinter.StringVar()
		self.selectorVal.set("HD")

		videoType = ['HD', '超清', '高清']

		s = ttk.Combobox(position, width = 5, textvariable = self.selectorVal, state='readonly', values = videoType)

		return s	

	def __showResult (self) :
		mainFoot = Tkinter.Frame(self.master, bd = 10)
		mainFoot.grid(row = 1, column = 0, sticky = '')		

		self.resultWindow = Tkinter.Text(mainFoot, height = 5, width = 70, highlightthickness = 0)
		self.resultWindow.grid(row = 0, sticky = '')

		self.__getUrl()

		b = Tkinter.Button(mainFoot, text = '下载', command = '')
		b.grid(row = 1, column = 0, sticky = 'ew')

	def __getUrl (self):
		self.resultWindow.delete('1.0', 'end')

		url = self.urlInput.get()
		result = True
		if 'youku' in url :
			getClass = youkuClass.ChaseYouku()
		elif 'sohu' in url :
			getClass = sohuClass.ChaseSohu()
		elif 'letv' in url :
			getClass = letvClass.ChaseLetv()
		elif 'tudou' in url :
			getClass = tudouClass.ChaseTudou()
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
				i = 1
				for x in urlList['msg']:
					result += '第' + str(i) + '段:\n' + str(x) + '\n'
					i += 1
			else :
				result = urlList['msg']

		else :
			result = '链接地址不再分析范围内！'

		
		self.resultWindow.insert('end', result)

	def run (self) :
		self.__mainWindow()
		self.master.mainloop()