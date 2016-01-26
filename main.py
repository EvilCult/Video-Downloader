#!/usr/bin/env python
# -*- coding: utf-8 -*-
import guiClass
from Module import youkuClass
from Module import tudouClass
from Module import sohuClass
from Module import letvClass


# e.g. youku
# obj = youkuClass.ChaseYouku();
# obj.videoLink = 'http://v.youku.com/v_show/id_XMTQ0NjU3MTU5Ng==.html?from=y1.2-2.4.2'
# url = obj.chaseUrl()
# print url

# e.g. tudou
# obj = tudouClass.ChaseTudou();
# obj.videoLink = 'http://www.tudou.com/listplay/BzWp_Z3jFdw/3lgQaEybkxs.html'
# url = obj.chaseUrl()
# print url

# e.g. sohu
# obj = sohuClass.ChaseSohu();
# obj.videoLink = 'http://tv.sohu.com/20160118/n434855906.shtml'
# url = obj.chaseUrl()
# print url

# e.g. letv
# obj = letvClass.ChaseLetv();
# obj.videoLink = 'http://sports.letv.com/video/24447570.html'
# url = obj.chaseUrl()
# print url

app = guiClass.GUI()
app.run()