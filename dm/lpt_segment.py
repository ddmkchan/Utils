#!/usr/bin/python
#coding=utf-8

import requests
import json

######################################################################################
#text    
#待分析的文本。  请以UTF-8格式编码，GET方式最大10K，POST方式最大20K

#pattern
#用以指定分析模式，可选值包括ws(分词)，pos(词性标注)，ner(命名实体识别)，dp(依存句法分析)，srl(语义角色标注),all(全部任务)  plain格式中不允许指定全部任务

#format
#用以指定结果格式类型，可选值包括xml(XML格式)，json(JSON格式)，conll(CONLL格式)，plain(简洁文本格式) 

#xml_input
#用以指定输入text是否是xml格式，可选值为false(默认值),true   仅限POST方式

#has_key
#用以指定json结果中是否含有键值，可选值包括true(含有键值，默认)，false(不含有键值)   配合format=json使用

#only_ner
#用以指定plain格式中是否只需要ner列表，可选值包括false(默认值)和true 配合pattern=ner&format=plain使用
######################################################################################

APP_KEY     = "Y1N00192xdgVUmwioQcJyGUFZXvf8TMNljUtyRLg"
LPT_CLOUD   = "http://api.ltp-cloud.com/analysis/"

def lpt_api(text, _format="plain", pattern="ws"):
    payload = {
            "api_key"   : APP_KEY,
            "text"      : text,
            "format"    : _format,
            "pattern"   : pattern
    }
    r = requests.get(LPT_CLOUD, params=payload)
    print r.url
    print r.text
    
if __name__ == "__main__":
    token = "g2ywbY8k"
    lpt_api(text="我是中国人")
