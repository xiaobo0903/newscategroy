#!/usr/bin/python
# -*- coding: UTF-8 -*-

#web main
#新闻处理类主流程，负责新闻内容的分析：关键词提取，自动分类，自动摘要、情感判断等，并把相应的信息返回或者入库
from flask import Flask, jsonify, request, abort
import json
from registeNews import *
from newsprocessclass import *
from ret_info import *

regn = registenewsClass()
newsprocess = newsprocess()
app = Flask(__name__)

#利用结巴分词来进行分词处理
@app.route('/newsmain/analyze', methods=['POST'])
def analyze():
    
    data = request.data
    j_data =  json.loads(data)
    return newsprocess.process(j_data)

#根据TF_IDF算法提取关键词
@app.route('/newsmain/registe', methods=['POST'])
def registe():
    
    data = request.data
    j_data =  json.loads(data)
    r_data = newsprocess.process(j_data)
    return regn.saveData(r_data)

@app.errorhandler(404)
def not_found(error):
    return return_404()
  
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8080, debug=True)  
#    app.run()  
