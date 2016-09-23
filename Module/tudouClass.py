#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from Library import toolClass

class ChaseTudou :

	def __init__ (self) :
		self.videoLink = ''
		self.Tools     = toolClass.Tools()

	def chaseUrl (self) :
		realUrl = self.__getRealUrl()

		return realUrl

	def __getRealUrl (self) :
		pageHeader, pageBody = self.Tools.getPage(self.videoLink)
		
		result = re.findall(r"pageConfig\s*?=\s*?{([\s\S]*?)}", pageBody)
		if len(result) > 0 :
			configStr = result[0]

			result = re.findall(r"vcode:\s*?'(.*?)'", configStr)

			if len(result) > 0 :
				url = 'http://v.youku.com/v_show/id_' + result[0] + '.html'
			else :
				url = ''

		else :
			url = ''

		return url


