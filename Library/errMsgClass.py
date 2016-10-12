#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ErrMsg :

	def __init__ (self) :
		pass

	def show (self, errNo) :
		msgs = self.__msgList()

		return msgs[str(errNo)]

	def __msgList (self) :
		msgs = {
			'1' : '链接地址不再分析范围内！',
			'2' : '可耻的分析失败了！',
			'3' : '没有获取到视频相关信息！',
			'4' : '没有找到所需清晰度的分段文件，请选择其他清晰度重试！',
			'5' : '',
			'6' : '',
			'7' : '',
			'8' : '',
			'9' : '',
			'10': '',
			'11': '',
			'12': ''
		}

		return msgs