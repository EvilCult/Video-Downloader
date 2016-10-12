#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
import os
import sqlite3
import platform
import time

class Config :

	def __init__(self):
		self.USER = getpass.getuser()
		self.appTitle = 'Video-Downloader'
		self.__getConfigPath()

		self.table = 'config'
		if self.__connect() == False:
			self.connStat = False
		else :
			self.connStat = True
			self.__chkTable()

	def __del__ (self) :
		if self.connStat == True :
			self.__disConn()

	def get (self) :
		result = {'stat' : 1, 'msg' : ''}

		if self.connStat != False : 
			sql = "SELECT * FROM " + self.table + " ORDER BY id DESC LIMIT 1"
			self.cur.execute(sql)
			values = self.cur.fetchone()

			if values :
				result['stat'] = 0
				result['path'] = values[1]
				result['udrate'] = values[2]
				result['udtime'] = values[3]
		
		return result

	def update (self, data) :
		result = {'stat' : 1, 'msg' : ''}
		if os.path.isdir(data['path']) :
			if int(data['udrate']) in [1,2,3] :
				if self.connStat != False : 
					sql = "UPDATE " + self.table + " SET path = '" + str(data['path']) + "', udrate = " + str(data['udrate'])
					self.cur.execute(sql)
					self.conn.commit()
					result['msg'] = '更新成功！'
			else :
				result['stat'] = 3
				result['msg'] = '目录不存在！'
		else :
			result['stat'] = 2
			result['msg'] = '目录不存在！'

		return result

	def lastUd (self, timeStr) :
		if self.connStat != False : 
			sql = "UPDATE " + self.table + " SET udtime = " + str(timeStr)
			self.cur.execute(sql)
			self.conn.commit()

	def __connect (self) :
		try:
			if not os.path.exists(self.configPath) :
				os.makedirs(self.configPath)
			self.configPath += 'Config'

			self.conn = sqlite3.connect(self.configPath)
			self.cur = self.conn.cursor()
			return True
		except:
			return False

	def __chkTable (self) :
		if self.connStat == False : return False

		sql = "SELECT tbl_name FROM sqlite_master WHERE type='table'"
		tableStat = False

		self.cur.execute(sql)
		values = self.cur.fetchall()

		for x in values:
			if self.table in x :
				tableStat = True

		if tableStat == False :
			self.__create()

	def __create (self) :
		if self.connStat == False : return False

		sql = 'create table ' + self.table + ' (id integer PRIMARY KEY autoincrement, path varchar(500), udrate int(1), udtime varchar(100))'
		self.cur.execute(sql);

		path = os.path.join(os.path.expanduser("~"), 'Desktop')
		udrate = '2'
		udtime = str(int(time.time()))

		sql = "insert into " + self.table + " (path, udrate, udtime) values ('" + path + "', " + udrate + ", '" + udtime + "')"

		self.cur.execute(sql)
		self.conn.commit()

	def __disConn (self) :
		if self.connStat == False : return False

		self.cur.close()
		self.conn.close()

	def __getConfigPath (self) :
		osType = platform.system()

		if osType == 'Linux' :
			self.configPath = '/usr/local/bin/' + self.appTitle + '/'
		elif osType == 'Darwin' :
			self.configPath = '/Users/' + self.USER + '/Library/Application Support/' + self.appTitle + '/'
		elif osType == 'Windows' :
			sysDrive = os.getenv("SystemDrive")
			self.configPath = sysDrive + '\\Users\\' + self.USER + '\\Documents\\' + self.appTitle + '\\'