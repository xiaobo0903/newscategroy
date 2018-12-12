#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time

def return_404():
    
    ret = '{"status":"404","info":"Page not found","date":"%s"}'%(time.strftime("%Y-%m-% %H:%M:%S",time.localtime(time.time())))
    return ret
