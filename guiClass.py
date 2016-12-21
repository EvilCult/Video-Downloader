#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import ttk 
import tkMessageBox
import tkFileDialog
import os
import sys
import threading
import time
import webbrowser
from Module import youkuClass
from Module import tudouClass
from Module import sohuClass
from Module import letvClass
from Module import bilibiliClass
from Module import acfunClass
from Module import iqiyiClass
from Library import fileProcesserClass
from Library import updateClass
from Library import cfgClass

class GUI :

	def __init__ (self) :
		self.masterTitle = 'Video Downloader'
		self.fileList = []
		self.version = ''
		self.appVer = ''
		self.appUrl = ''
		self.gitUrl = ''
		self.feedUrl = ''

		self.CfgClass = cfgClass.Config()
		self.cfg = self.CfgClass.get()

	def __mainWindow (self) :
		self.master = Tkinter.Tk();

		self.master.title(self.masterTitle)
		self.master.resizable(width = 'false', height = 'false')

		self.__menu()
		self.__topBox()
		self.__autoUpdate()

	def __menu (self) :
		menubar = Tkinter.Menu(self.master)

		fileMenu = Tkinter.Menu(menubar, tearoff = 0)
		fileMenu.add_command(label = "Config", command = self.__configPanel)
		fileMenu.add_command(label = "Close", command = self.master.quit)
		menubar.add_cascade(label = "File", menu = fileMenu)

		aboutMenu = Tkinter.Menu(menubar, tearoff = 0)
		aboutMenu.add_command(label = "Info", command = self.__showInfo)
		aboutMenu.add_command(label = "Check Update", command = self.__chkUpdate)
		menubar.add_cascade(label = "About", menu = aboutMenu)

		helpMenu = Tkinter.Menu(menubar, tearoff = 0)
		helpMenu.add_command(label = "GitHub", command = lambda target = self.gitUrl : webbrowser.open_new(target))
		helpMenu.add_command(label = "Release Notes", command = lambda target = self.appUrl : webbrowser.open_new(target))
		helpMenu.add_command(label = "Send Feedback", command = lambda target = self.feedUrl : webbrowser.open_new(target))
		menubar.add_cascade(label = "Help", menu = helpMenu)

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

	def __getUrl (self) :
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
			getClass.videoLink = url
			url = getClass.chaseUrl()
			getClass = youkuClass.ChaseYouku()
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

			self.FPC.download(self.fileList, self.cfg['path'])
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

	def __showInfo (self) :
		self.slave = Tkinter.Tk();

		self.slave.title('Info')
		self.slave.resizable(width = 'false', height = 'false')

		info = [
			'Support: www.youku.com\nwww.tudou.com\ntv.sohu.com\nwww.letv.com\nwww.bilibili.com\nwww.acfun.tv\nwww.iqiyi.com',
			'Website: http://evilcult.github.io/Video-Downloader/',
			'Special Thanks: bunnyswe(https://github.com/bunnyswe)\nliuyug(https://github.com/liuyug)'
		]

		label = Tkinter.Label(self.slave, text="Video Downloader", font = ("Helvetica", "16", 'bold'), anchor = 'center')
		label.grid(row = 0, pady = 10)

		information = Tkinter.Text(self.slave, height = 10, width = 50, highlightthickness = 0, font = ("Helvetica", "14"))
		information.grid(row = 1, padx = 10, pady = 5)
		for n in info :
			information.insert('end', n.split(': ')[0] + '\n')
			information.insert('end', n.split(': ')[1] + '\r')

		label = Tkinter.Label(self.slave, text="Version: " + self.version, font = ("Helvetica", "12"), anchor = 'center')
		label.grid(row = 2)
		label = Tkinter.Label(self.slave, text="Author: Ray H.", font = ("Helvetica", "12"), anchor = 'center')
		label.grid(row = 3)

	def __configPanel (self) :
		self.slave = Tkinter.Toplevel();

		self.slave.title("Config")
		self.slave.resizable(width = 'false', height = 'false')

		l1 = Tkinter.Label(self.slave, text = '下载目录：')
		l1.grid(row = 0)

		self.filePath = Tkinter.StringVar()
		self.filePath.set(self.cfg['path'])
		e1 = Tkinter.Entry(self.slave, textvariable = self.filePath)
		e1.grid(row = 0, column = 1, columnspan = 3)

		b1 = Tkinter.Button(self.slave, text = '选择', command = self.__chooseCfgFolder)
		b1.grid(row = 0, column = 4, sticky = 'e')

		l2 = Tkinter.Label(self.slave, text = '检查更新：')
		l2.grid(row = 1)

		self.chkUpdateTime = Tkinter.IntVar()
		self.chkUpdateTime.set(int(self.cfg['udrate']))
		r1 = Tkinter.Radiobutton(self.slave, text="每天", variable=self.chkUpdateTime, value=1)
		r1.grid(row = 1, column = 1, sticky = 'e')
		r2 = Tkinter.Radiobutton(self.slave, text="每周", variable=self.chkUpdateTime, value=2)
		r2.grid(row = 1, column = 2, sticky = 'e')
		r3 = Tkinter.Radiobutton(self.slave, text="每月", variable=self.chkUpdateTime, value=3)
		r3.grid(row = 1, column = 3, sticky = 'e')

		b2 = Tkinter.Button(self.slave, text = '更新', command = self.__setConfig)
		b2.grid(row = 2, column = 1, sticky = 'e')

		b3 = Tkinter.Button(self.slave, text = '取消', command = self.slave.destroy)
		b3.grid(row = 2, column = 2, sticky = 'e')

	def __chooseCfgFolder (self) :
		path = tkFileDialog.askdirectory(initialdir="/",title='请选择文件夹')
		self.filePath.set(path.strip())

	def __setConfig (self):
		newCfg = {
			"path": self.filePath.get(),
			"udrate": self.chkUpdateTime.get()
		}

		result = self.CfgClass.update(newCfg)

		if result['stat'] == 1 :
			self.cfg['path'] = newCfg['path']
			self.cfg['udrate'] = newCfg['udrate']
			self.slave.destroy()
			tkMessageBox.showinfo('成功', '更新成功')
		else :
			self.__error(result['stat'])

	def __error(self,errNum):
		if errNum == 2:
			tkMessageBox.showinfo('失败', '更新失败！\n选择的下载目录不存在！')
		elif errNum == 3:
			tkMessageBox.showinfo('失败', '更新失败！\n更新频率选择错误！')
		else :
			tkMessageBox.showinfo('失败', '更新失败！\n未知错误！')

	def __chkUpdate (self) :
		Updater = updateClass.Update()

		info = Updater.check(self.appVer)

		self.slave = Tkinter.Tk();

		self.slave.title('Update')
		self.slave.resizable(width = 'false', height = 'false')

		if info['update'] == True :
			label = Tkinter.Label(self.slave, text = info['version'], font = ("Helvetica", "16", 'bold'), anchor = 'center')
			label.grid(row = 0, pady = 10)

			information = Tkinter.Text(self.slave, height = 10, width = 60, highlightthickness = 0, font = ("Helvetica", "14"))
			information.grid(row = 1, padx = 10, pady = 5)
			information.insert('end', info['msg']);

			btn = Tkinter.Button(self.slave, text = 'Download', width = 10, command = lambda target = info['dUrl'] : webbrowser.open_new(target))
			btn.grid(row = 2, pady = 10)
		else :
			label = Tkinter.Label(self.slave, text = self.version, font = ("Helvetica", "16", 'bold'), anchor = 'center')
			label.grid(row = 0, pady = 10)

			label = Tkinter.Label(self.slave, height = 3, width = 60, text = info['msg'], font = ("Helvetica", "14"), anchor = 'center')
			label.grid(row = 1, pady = 10)

		now = int(time.time())
		self.CfgClass.lastUd(now)

	def __autoUpdate (self) :
		now = int(time.time())
		if self.cfg['udrate'] == 1:
			updateTime = int(self.cfg['udtime']) + 86400
		elif self.cfg['udrate'] == 2:
			updateTime = int(self.cfg['udtime']) + 86400 * 7
		elif self.cfg['udrate'] == 3:
			updateTime = int(self.cfg['udtime']) + 86400 * 30
		else :
			updateTime = int(self.cfg['udtime']) + 86400 * 7

		if updateTime < now :
			Updater = updateClass.Update()

			info = Updater.check(self.appVer)

			self.CfgClass.lastUd(now)

			if info['update'] == True :
				self.slave = Tkinter.Tk();

				self.slave.title('Update')
				self.slave.resizable(width = 'false', height = 'false')

				label = Tkinter.Label(self.slave, text = info['version'], font = ("Helvetica", "16", 'bold'), anchor = 'center')
				label.grid(row = 0, pady = 10)

				information = Tkinter.Text(self.slave, height = 10, width = 60, highlightthickness = 0, font = ("Helvetica", "14"))
				information.grid(row = 1, padx = 10, pady = 5)
				information.insert('end', info['msg']);

				btn = Tkinter.Button(self.slave, text = 'Download', width = 10, command = lambda target = info['dUrl'] : webbrowser.open_new(target))
				btn.grid(row = 2, pady = 10)

	def run (self) :
		self.__mainWindow()
		self.master.mainloop()