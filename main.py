#!/usr/bin/env python
# -*- coding: utf-8 -*-
import site
site.addsitedir('./Module')
site.addsitedir('./Library')
import guiClass

app = guiClass.GUI()
app.run()