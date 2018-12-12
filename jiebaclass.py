#!/usr/bin/python
# -*- coding: UTF-8 -*-

#把整理后的数据写入到mongodb数据库中，数据库名称为:cevcloud_logs, 数据库需要提前建立
#对于每天的记录puv_stat_day_YYYYMM来进行保存 ,每个月建立一个collection
import time, datetime
import json
import calendar
import jieba
import re
from jieba import analyse
from urllib import unquote
from snownlp import SnowNLP

#停词的路径
swpath="/home/python/stopword.txt"
analyse.set_stop_words(swpath)
class jiebaClass:
    
    def clearHTML(self, html):
        
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub('',html)
        ret = dd.replace('\n', '').replace('\t', '').replace('\r', '')
        return ret
    
    def json_text(self, j_data):
        
        title = j_data['title']
        content = j_data['content'] 
        all_text = title+content
        all_text = self.clearHTML(all_text)
        return all_text
        
#根据结巴分词来进行内容的处理，json中包含的结构中一定需要有title和content两个内容，否则就会返回空。
    def splite(self, j_data):        

        text = self.json_text(j_data)
        all_text_utf8 = text.encode("utf-8")
#        seg_list = jieba.cut(all_text_utf8, cut_all=True)
        seg_list = list(jieba.cut_for_search(all_text_utf8))
#        print("Default Mode: " + " ".join(seg_list)) 
# 输出抽取出的关键词
        kw = ""
        for keyword in seg_list:
            if kw == "" :
                kw = "\"" + keyword+"\""
            else:    
                kw = kw + ",\""+keyword+"\""
        
        #ret = "{\"title\":"+j_data['title']+",keyword:["+kw+"]}"
        ret = kw
        return ret        

#根据结巴分词来进行内容的处理，json中包含的结构中一定需要有title和content两个内容，否则就会返回空。
    def splite1(self, str_data):        

        all_text_utf8 = str_data.encode("utf-8")
#        seg_list = jieba.cut(all_text_utf8, cut_all=True)
        seg_list = list(jieba.cut_for_search(all_text_utf8))
#        print("Default Mode: " + " ".join(seg_list)) 
# 输出抽取出的关键词
        kw = ""
        for keyword in seg_list:
            if kw == "" :
                kw = keyword
            else:    
                kw = kw + ","+keyword
        
        #ret = "{\"title\":"+j_data['title']+",keyword:["+kw+"]}"
        ret = kw
        return ret        



    def keyword_IDF(self, text): 
        
        tfidf = analyse.extract_tags
# 基于TF-IDF算法进行关键词抽取
        keywords = tfidf(text)
#        print "keywords by tfidf:"
# 输出抽取出的关键词
        kw = ""
        for keyword in keywords:
            if kw == "" :
                kw = "\"" + keyword+"\""
            else:    
                kw = kw + ",\""+keyword+"\""
        
        #ret = "{\"title\":"+j_data['title']+",keyword:["+kw+"]}"
        ret = kw
        return ret
#根据textrank计算关键词
    def keyword_TR(self, j_data):
    
        textrank = analyse.textrank
        text = self.json_text(j_data)
        # 基于TextRank算法进行关键词抽取
        
#        print text
        keywords = textrank(text)
#        print "keywords by textrank:"
        # 输出抽取出的关键词
        kw = ""
        for keyword in keywords:
            if kw == "" :
                kw = "\"" + keyword+"\""
            else:    
                kw = kw + ",\""+keyword+"\""
        #ret = "{\"title\":"+j_data['title']+",keyword:["+kw+"]}"
        #print ret
                
        ret = kw
        return ret
#返回关键词和摘要
    def keyword_summary(self, j_data): 
        
        text = self.json_text(j_data)
        a1 = SnowNLP(text)
        a2 = a1.summary(2)
     #   keywords1 = self.keyword_TR(j_data)
        keywords2 = self.keyword_IDF(j_data)
        a2_str = ",".join(a2)
        ret = "{\"keyword\":["+keywords2+"], \"summary\":\""+a2_str+"\"}"
#        print ret
        return ret

    def emontion(self, j_data):
         
         text = self.json_text(j_data)
         a1 = SnowNLP(text)
         a2 = a1.sentiments
#         print a2
         return ""+str(a2)
     
    def summary(self, j_data):
         
         text = self.json_text(j_data)
         a1 = SnowNLP(text)
         a2 = a1.summary(2)
         return ",".join(a2)     
            
    def load_stopword(self):
        analyse.set_stop_words(swpath)        
            
            
            