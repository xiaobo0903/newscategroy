#!/usr/bin/python
# -*- coding: UTF-8 -*-

#新闻分类学习器，通过原始素材的学习，来实现机器自动分类的处理。学习的素材要求：指定学习训练素材的目录，并且文件的名称为分类的名称，如：政治.txt 军事.txt等，目录下不能够有其它的非学习内容相关的信息文件
#生成的学习数据库在该指定目录下的train子目录下，可以把学习后的数据拷入到其它地方进行使用。

import jieba 
import os 
import sys 
import codecs 
from sklearn import feature_extraction 
from sklearn import svm 
import numpy as np
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn import tree 
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.externals import joblib
import re
from snownlp import sentiment #加载情感分析模块


class news_class_learn:
    
    file_path = ""
    save_path = ""
    category=[]
    train_data = []
    pre_vectorizer = None
    model = None
    pattern = re.compile(r'.txt')
    
    def __init__(self, path):
        
        self.set_path(path)
        return
#设置工作路径
    def set_path(self, path):
        
        self.file_path = path
        self.save_path = path+"/train/"
           
    
    def getfiledate(self):
        
        pathDir =  os.listdir(self.file_path)
        
        for allDir in pathDir:
            
            if(self.pattern.search(allDir) == None ):
                
                print "not ok!",allDir
                continue
        
            self.getdata(allDir)
     
    def getdata(self, filename):
         
         fname = filename.split(".")     
         txtfile = os.path.join('%s%s' % (self.file_path, filename))
         try:
             file_object = open(txtfile)
             filedata = file_object.read()
             self.train_data.append(filedata)
             self.category.append(fname[0])
         except Exception, e:
             print "error",e
         finally:
             file_object.close( )

    def emontion_train(self):

        sentiment.train('E:/Anaconda2/Lib/site-packages/snownlp/sentiment/neg.txt', 'E:/Anaconda2/Lib/site-packages/snownlp/sentiment/pos.txt') #对语料库进行训练，把路径改成相应的位置。我这次练习并没有构建语料库，用了默认的，所以把路径写到了sentiment模块下。
        sentiment.save('D:/pyscript/sentiment.marshal')#这一步是对上一步的训练结果进行保存，如果以后语料库没有改变，下次不用再进行训练，直接使用就可以了，所以一定要保存，保存位置可以自己决定，但是要把`snownlp/seg/__init__.py`里的`data_path`也改成你保存的位置，不然下次使用还是默认的。

    def train(self):
        
        vectorizer=CountVectorizer()
        train_ma = vectorizer.fit_transform(self.train_data)
        transformer=TfidfTransformer()
        tfidf=transformer.fit(train_ma).fit_transform(train_ma)
        ids = range(0, len(self.category))
        y = np.array(ids)
        
        print self.category
        model = SVC(kernel='linear', probability=True)
        model.fit(tfidf, y)
        joblib.dump(model, "%s/train_model.m"%(self.save_path))
        categroy_str = ",".join(self.category)
        fp = open("%s/category.m"%(self.save_path), "w")
        fp.write(categroy_str)
        fp.close()

    def class_train(self):
        
        self.getfiledate()
        self.train()

    def init_predict(self):

        try:
            file_object = open("%s/category.m"%(self.save_path))
            filedata = file_object.read()
            self.category = filedata.split(",")
        except Exception, e:
            print "error",e
            exit
        finally:
             file_object.close( )

        self.model = joblib.load("%s/train_model.m"%(self.save_path))
        
        self.getfiledate()
        self.pre_vectorizer=CountVectorizer()
        train_ma = self.pre_vectorizer.fit_transform(self.train_data)
     
    def predict(self, pre_str):
         vectorizer1=CountVectorizer(vocabulary=self.pre_vectorizer.vocabulary_)
         pre_array = []
         pre_array.append(pre_str)
         csr_mat = vectorizer1.fit_transform(pre_array)
         transformer = TfidfTransformer()
         tfidf = transformer.fit_transform(csr_mat) 
         predicted = self.model.predict(tfidf)
         predicted1 = self.model.predict_proba(tfidf)
#         print pre_str, self.category[predicted[0]]
         
         return self.category[predicted[0]]
     
             
#kk = news_class_learn("/home/data/")
#kk.init_predict()
#kk.predict("迎接 新学 学期 新学期 各地 做好 开学 准备")
#kk.predict("直播 预告 | 同步 看 世界 怒江 壮美 泸水 晚会")
#kk.predict("光明 光明网 专论 军民 协同 开创 军队 后勤 军民 融合 发展 格局 新格局")
            
            
            
            
            
            
            
            
            
            