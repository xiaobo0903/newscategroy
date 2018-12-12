#!/usr/bin/python
# -*- coding: UTF-8 -*-


#本类主要实现文章的关键字提取、情感判断、自动摘要、自动分类四项功能，对于自动打标签，可以调节关键字的多少来进行。
#其中关键字提取、情感分析、自动摘要由jieba类库来完成，自动分类由机器学习来完成。
#处理其间会用到两个类：jiebaclass.py news_class_learn.py, 其中news_class_learn中含有学习的模块，如果不准可以重新组织内容学习。
import jieba
import json
import re
from jiebaclass import *
from news_class_learn import *


workdir = "/home/data/"
jbclass = jiebaClass()
news = news_class_learn(workdir)

class newsprocess():
    
    def __init__(self):
        
        news.init_predict()
        return

    def clearHTML(self, html):
        
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub('',html)
        ret = dd.replace('\n', '').replace('\t', '').replace('\r', '')
        return ret
    
    def process(self, j_data):
        
        json_ret = {}
        title = self.clearHTML(j_data['title'])
        content = self.clearHTML(j_data['content'])
        all_text = title+content
        keywords = jieba.analyse.extract_tags(all_text, 20)
        keyword = ",".join(keywords) 
        
        nlp = SnowNLP(content)
        smyarray = nlp.summary(3)
        news_summary = ",".join(smyarray)
        
        nlp1 = SnowNLP(title)
        
        scorce = nlp1.sentiments
        
        emontion = "中"
        if(scorce > 0.7):
            emontion = "正"
        if(scorce < 0.3):
            emontion = "负"
            
        json_ret["summary"] = news_summary
#        json_ret["title"] = title
#        json_ret["content"] = content
        json_ret["emontion"] = emontion
        json_ret["keyword"] = keyword
        json_ret["scorce"] = ""+ str(round(scorce, 7))
        
        cutword = jbclass.splite1(title)
        category = news.predict(cutword)
        json_ret["category"] = category
        
        str_ret = json.dumps(json_ret)
        return str_ret


jjj = {}
jjj["title"] = "龙瑞高速遮放段货车自燃，幸无人员伤亡"
jjj["content"] = "3月15日上午7点半左右龙瑞高速瑞丽至芒市方向上行线K659公里处,一辆拉西瓜的大货车发生自燃目前火势已经扑灭,没有造成人员伤亡.高速民警正在指挥驳货,由于卸货速度较慢发生事故路段仍处于封闭状态.芒市高速公路交巡警大队副大队长朱绍华介绍,预计于下午3点半左右可以放行去往芒市昆明方向的车辆,沿遮放收费站下高速往G320线继续前行到风平芒市机场后方可继续上高速前往昆明,龙瑞高速遮放收费站下站匝道口处芒市高速公路交巡警大,队民警已在此实行临时交通管制请过往的驾驶员朋友们,减速慢行依次通过并服从现场执勤民警的指挥谢谢合作.本台记者杨笑丹."                                            
jjj["url"] = "/aaaaaa/bbbbb/cccc/23"
jjj["domain"] = "www.hhhh.com"
jjj["business"] = "qichayun"

json_str =json.dumps(jjj)

#print json_str
#j1 = '{"title":"龙瑞高速遮放段货车自燃，造成多个人员伤亡", "content":"自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。自然语言处理是一门融语言学、计算机科学、数学于一体的科学。因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，所以它与语言学的研究有着密切的联系，但又有重要的区别。自然语言处理并不是一般地研究自然语言，而在于研制能有效地实现自然语言通信的计算机系统，特别是其中的软件系统。因而它是计算机科学的一部分。"}'

j1 = '{"title":"龙瑞高速遮放段货车自燃，造成多个人员伤亡", "content":"3月15日上午7点半左右龙瑞高速瑞丽至芒市方向上行线K659公里处,\n\n\n\n\n\n一辆拉西瓜的大货车发生自燃目前火势已经扑灭,没有造成人员伤亡.高速民警正在指挥驳货,由于卸货速度较慢发生事故路段仍处于封闭状态.芒市高速公路交巡警大队副大队长朱绍华介绍,预计于下午3点半左右可以放行去往芒市昆明方向的车辆,沿遮放收费站下高速往G320线继续前行到风平芒市机场后方可继续上高速前往昆明,龙瑞高速遮放收费站下站匝道口处芒市高速公路交巡警大,队民警已在此实行临时交通管制请过往的驾驶员朋友们,减速慢行依次通过并服从现场执勤民警的指挥谢谢合作.本台记者杨笑丹."}'

newsproc = newsprocess()
jj = json.loads(newsproc.clearHTML(j1))
str_ret = newsproc.process(jj)
json_ss = json.loads(str_ret)
print "emontion="+json_ss["emontion"]
print "summary="+json_ss["summary"]
print "keyword="+json_ss["keyword"]
print "category="+json_ss["category"]
print "scorce="+json_ss["scorce"]
        