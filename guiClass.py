#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import ttk 
import tkFileDialog
import tkMessageBox
import os
import sys
from Module import youkuClass
from Module import tudouClass
from Module import sohuClass
from Module import letvClass

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
		self.__footBox()

	def __menu (self) :
		menubar = Tkinter.Menu(self.master)

		filemenu = Tkinter.Menu(menubar, tearoff = 0)
		filemenu.add_command(label = "设置", command = '')
		filemenu.add_command(label = "退出程序", command = self.master.quit)
		menubar.add_cascade(label = "Setting", menu = filemenu)

		self.master.config(menu = menubar)

	def __topBox (self) :
		mainTop = Tkinter.Frame(self.master, bd = 10)
		mainTop.grid(row = 0, column = 0, sticky = '')		

		self.urlInput = Tkinter.Entry(mainTop, width = 50)
		self.urlInput.grid(row = 0, column = 0)

		b = Tkinter.Button(mainTop, text = '搜索', command = '')
		b.grid(row = 0, column = 1)

	def __footBox (self) :
		mainFoot = Tkinter.Frame(self.master, bd = 10)
		mainFoot.grid(row = 1, column = 0, sticky = '')		

		self.resultWindow = Tkinter.Text(mainFoot, height = 5, width = 70, highlightthickness = 0)
		self.resultWindow.grid(row = 0, sticky = '')

		b = Tkinter.Button(mainFoot, text = '下载', command = '')
		b.grid(row = 1, column = 0, sticky = 'ew')

	def run (self) :
		self.__mainWindow()
		self.master.mainloop()