#!/usr/bin/python
# -*- coding: UTF-8 -*-


#注册新闻内容，通过json方式来进行注册
# json中主要由：source(源)/title(标题)/keyword(关键词,每个关键词按热度区分逐级递减)/domain(域名)/uri(访问地址)/time(生成时间)/category(分类)/MD5(domain+uri)/state(标志)/comment(说明)

from pymongo import MongoClient
import hashlib
import datetime
import json

_MDBIP = "192.168.1.84" 
_MDBPORT = 27017
_MDBINDEX = "mediabd"

class registenewsClass:
	
	def get_md5_value(self, src):

	    myMd5 = hashlib.md5()
	    myMd5.update(src)
	    myMd5_Digest = myMd5.hexdigest()
	    return myMd5_Digest
	    
	def connect(self):		
		client = MongoClient(_MDBIP, _MDBPORT)
		db_name = _MDBINDEX
		db = client[db_name]
		return db

	def saveData(self, j_data):        
		
		j_json = {}  
		ret = {}
		try:
			j_json["source"] = j_data["bussines"]
			j_json["title"] = j_data["title"]
			j_json["keyword"] = j_data["keyword"]
			j_json["domain"] = j_data["domain"]
			j_json["url"] = j_data["url"]
			j_json["category"] = j_data["category"]
			
			try:
				j_json["ctime"] = j_data["ctime"]
			except:
				now = datetime.datetime.now()
	    		j_json["ctime"] = now.strftime('%Y-%m-%d %H:%M:%S')
			try:
				j_json["scorce"] = j_data["scorce"]
			except:
				j_json["scorce"] = "0.5"
			try:
				j_json["summary"] = j_data["summary"]
			except:
				j_json["summary"] = ""

			j_json["_id"] = self.get_md5_value(j_json["domain"]+j_json["url"])
			j_json["state"] = "正常"
			j_json["comment"] = "正常"

			collactionname = "news_bank"

			if self.db == None:
				self.db = self.connect()
				print("connect to %s...")%(collactionname)
			collection_newsaction = self.db[collactionname]
			results1 = collection_newsaction.save(j_json)
    	
			ret["state"] = "OK"
			ret["info"] = "处理完成"
		except:
			ret["state"] = "Error"
    		ret["info"] = "数据内容不完整"			
		
		return json.dumps(ret)
    	
    	
    	