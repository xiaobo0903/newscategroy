#!/usr/bin/python
# -*- coding: UTF-8 -*-
#web main

from flask import Flask, jsonify, request, abort
import json
from ret_info import *
from jiebaClass import *
from summaryClass import *

jieba = jiebaClass()
summarycls = summaryClass()
newsprocess = newsprocessClass()
app = Flask(__name__)

#利用结巴分词来进行分词处理
@app.route('/splitewords', methods=['POST'])
def splitewords():
    
    data = request.data
    j_data =  json.loads(data)
    return jieba.splite(j_data)

#根据TF_IDF算法提取关键词
@app.route('/kwIDF', methods=['POST'])
def keyword_IDF():
    
    data = request.data
    j_data =  json.loads(data)
    return jieba.keyword_IDF(j_data)

#根据TextRang算法提取关键词
@app.route('/kwTR', methods=['POST'])
def keyword_TR():
    
    data = request.data
    j_data =  json.loads(data)
    return jieba.keyword_TR(j_data)

#根据snowNLP计算情感指数
@app.route('/emontion', methods=['POST'])
def keyword_emontion():
    
    data = request.data
    j_data =  json.loads(data)
    return jieba.emontion(j_data)

#根据snowNLP计算情感指数
@app.route('/summary', methods=['POST'])
def summary():
    
    data = request.data
    j_data =  json.loads(data)
    return summarycls.get_abstract(j_data)


@app.errorhandler(404)
def not_found(error):
    return return_404()
  
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8080, debug=True)  
#    app.run()  
