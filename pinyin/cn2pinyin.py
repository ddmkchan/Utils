#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import xlwt
from pinyin import PinYin, Cartesian_product

test = PinYin()
test.load_word()

wbk = xlwt.Workbook()

def main():
    #files = ['shop_2.csv', 'sight_2.csv']
    files = ['shop_2.csv', 'sight_2.csv', 'district_2_n.csv']
    for f in files:
        func(f)
    wbk.save("/home/chenyp/sharefolder/cn2pinyin.xls")

def func2(filename):
    #餐馆的输入文档
    poitype = filename.split(".")[0].decode('utf-8')
    column2 = u"%sid" % poitype
    count = 0
    lines = open(filename).readlines()[1:100]
    MAX = 35000
    if len(lines) % MAX == 0:
        total = len(lines) / MAX
    else:
        total = int(len(lines) / 35000.0 + 1)
    sheets = [wbk.add_sheet("%s_%s" % (poitype, i)) for i in xrange(total)]
    for s in sheets:
        add_excel_title(s, column2)
    sheet = sheets[0]
    row = 1
    for l in lines:
        segs = l.rstrip().split("\t")
        try:
            #餐馆的输入文档
            _id = segs[0]
            name = segs[1].decode('utf-8')
            name = add_space(name)
            pys = get_pinyins(name)
            more_than_one = False if len(pys) == 1 else True
            for py in get_pinyins(name):
                #print "ADD\t%s\t%s\t%s\t%s" % (_id, name, py, more_than_one)
                write2excel(sheet, row, u"ADD", int(_id), name, py, u"", more_than_one)
                row += 1
            count += 1

            if count % MAX == 0:
                _index = count / MAX 
                sheet = sheets[_index]
                row = 1
                print count, _index ,sheet.name
        except Exception,e:
            print str(e), sheet.name, count, row
    wbk.save("/home/chenyp/sharefolder/rest_cn2pinyin.xls")

def func(filename):
    poitype = filename.split(".")[0].decode('utf-8')
    column2 = u"%sid" % poitype
    sheet = wbk.add_sheet(poitype)
    row = 1
    sheet.write(0, 0, column2)
    sheet.write(0, 1, u"名称")
    sheet.write(0, 2, u"旧的拼音")
    #sheet.write(0, 0, u"新增或更新")
    #sheet.write(0, 1, column2)
    #sheet.write(0, 2, u"名称")
    #sheet.write(0, 3, u"新的拼音")
    #sheet.write(0, 4, u"旧的拼音")
    #sheet.write(0, 5, u"是否存在多音字")
    #sheet.write(0, 6, u"parentdistrict")
    #sheet.write(0, 7, u"isinchina")
    for l in open(filename).readlines()[1:]:
        segs = l.rstrip().split("\t")
        try:
            _id = segs[1]
            name = segs[2].decode('utf-8')
            ename = segs[3]
            pinyin = segs[4]
            parentdistrict = segs[5]
            #isinchina = segs[7]
            name = add_space(name)
            if re.search(u'[\u4e00-\u9fa5]+', name) is None:
                py = pinyin.decode('utf-8')
                pys = get_pinyins(name)
                print "%s\t%s\t%s" % (_id, name, py)
                if (len(name)>=2 and len(py.split()) <2) or len(name) != len(py.split(' ')):
                    sheet.write(row, 0, _id)
                    sheet.write(row, 1, name)
                    sheet.write(row, 2, py)
                    row += 1
                #if len(name)>=2 and len(py.split()) <2:
                #    more_than_one = False if len(pys) == 1 else True
                #    for new_py in pys[:1]:
                #        print "UPDATE\t%s\t%s\t%s\t%s" % (_id, name, new_py, more_than_one)
                #        write2excel(sheet, row, u"UPDATE", int(_id), name, new_py, py, more_than_one, parentdistrict, int(isinchina))
                #        row += 1
                #else:
                #    if len(name) != len(py.split(' ')):
                #        more_than_one = False if len(pys) == 1 else True
                #        for new_py in pys[:1]:
                #            print "UPDATE\t%s\t%s\t%s\t%s" % (_id, name, new_py, more_than_one)
                #            write2excel(sheet, row, u"UPDATE", int(_id), name, new_py, py, more_than_one, parentdistrict, int(isinchina))
                #            row += 1
            #else:
            #    pys = get_pinyins(name)
            #    more_than_one = False if len(pys) == 1 else True
            #    for py in pys[:1]:
            #        print "ADD\t%s\t%s\t%s\t%s" % (_id, name, py, more_than_one)
            #        write2excel(sheet, row, u"ADD", int(_id), name, py, u"", more_than_one, parentdistrict, int(isinchina))
            #        row += 1
        except Exception,e:
            print str(e)
            #pass
    #wbk.save("/home/chenyp/sharefolder/shop_cn2pinyin.xls")

def write2excel(sheet, row, c1, c2, c3, c4, c5, c6, c7, c8):
    sheet.write(row, 0, c1)
    sheet.write(row, 1, c2)
    sheet.write(row, 2, c3)
    sheet.write(row, 3, c4)
    sheet.write(row, 4, c5)
    sheet.write(row, 5, c6)
    sheet.write(row, 6, c7)
    sheet.write(row, 7, c8)

def add_excel_title(sheet, column2):
    sheet.write(0, 0, u"新增或更新")
    sheet.write(0, 1, column2)
    sheet.write(0, 2, u"名称")
    sheet.write(0, 3, u"新的拼音")
    sheet.write(0, 4, u"旧的拼音")
    sheet.write(0, 5, u"是否存在多音字")

def get_pinyins(name):
    rs = []
    p = re.compile(u'[\u4e00-\u9fa5]+')
    ch_names = p.findall(name)
    cnames = "".join([ch_name for ch_name in ch_names])
    pys = Cartesian_product(test.hanzi2pinyin(string=cnames))
    for p in pys:
        tmp = name
        for ch_name in ch_names:
            m = re.search(ch_name, cnames)
            _start = m.start()
            _end = m.end()
            replace = " ".join([k for k in p.split()[_start:_end]])
            tmp = re.sub(ch_name, replace, tmp, 1)
        rs.append(tmp)
    return rs

def is_hz_py(s1, s2):
    num_p = re.compile(u'\d+')
    if num_p.match(s1) is not None and num_p.match(s2) is not None:
        return True
    chr_p = re.compile(u"(\,|\.|`|-|_|\=|\?|\'|\||\"|\(|\)|{|}|\[|\]|<|>|\*|#|\&|\^|\$|@|\!|\~|\:|\;|\+|\\\\|）|（|【|】|［|］|\/|《|》|—|－|，|。|、|：|；|！|·|？|“|”|●|\s)+")
    if chr_p.match(s1) is not None or chr_p.match(s2) is not None:
        return True
    issame = False
    p = re.compile(u'[\u4e00-\u9fa5]+')
    p_eng = re.compile(u'[a-zA-Z]+')
    if p.match(s1) is not None and p.match(s2) is not None:
        issame = True
    if p_eng.match(s1) is not None and p_eng.match(s2) is not None:
        issame = True
    return issame

def add_space(string):
    strs = []
    j = 0
    while (j<len(string)):
        if j+1 == len(string):
            strs.append(string[j])
        else:
            if not is_hz_py(string[j], string[j+1]):
                strs.append(string[j]+u" ")
            else:
                strs.append(string[j])
        j += 1
    string  = "".join(strs)
    return string

def t2():
    test = PinYin()
    test.load_word()
    #string = u"Kottlers古玩城"
    #string = u"Head 2 Toe发型店"
    #string = u"蓝"
    #print string
    #print test.hanzi2pinyin(string=string)
    #print Cartesian_product(test.hanzi2pinyin(string=string))

    name = u"普季(商城)"
    name = u"Kottlers古玩城"
    name = u"hello 艾压(重庆店)山"
    name = u"库兰达（库兰达热带雨林）"
    #name = u"盛文甘hello店(店)"
    #name = u"义乌三期市场（原篁园市场）"
    print name
    p = re.compile(u'[\u4e00-\u9fa5]+')
    p_eng = re.compile(u'[a-zA-Z]+')
    j = 0
    strs = []
    while (j<len(name)):
        
    #for j in xrange(len(name)):
    #    if j 
        
        if j+1 == len(name):
            strs.append(name[j])
        else:
            print (name[j], name[j+1]), is_hz_py(name[j], name[j+1])
            if not is_hz_py(name[j], name[j+1]):
                print name[j], j
                strs.append(name[j]+u" ")
            else:
                strs.append(name[j])
        j += 1
    name  = "".join(strs)
    ch_names =  p.findall(name)
    tmp = name
    ll = []
    mydict = {}
    cnames = "".join([ch_name for ch_name in ch_names])
    #pys = test.hanzi2pinyin(string=cnames)
    pys = Cartesian_product(test.hanzi2pinyin(string=cnames))
    print cnames, pys, ch_names
    for p in pys:
        tmp2 = name
        for ch_name in ch_names:
            m = re.search(ch_name, cnames)
            _start = m.start()
            _end = m.end()
            replace = " ".join([k for k in p.split()[_start:_end]])
            print _start, _end, replace, tmp2
            tmp2 = re.sub(ch_name, replace, tmp2, 1)
        print tmp2

if __name__ == "__main__":
    #func("sight_2.csv")
    #func("shop_2.csv")
    #func("district.csv")
    #t2()
    #func2("rest.txt")
    main()
    #print is_hz_py(u'5', u'6')
    #func()
    #for l in open("district_2_n.csv").readlines()[1:]:
    #    segs = l.rstrip().split("\t")
    #    if len(segs) == 7:
    #        _id = segs[1]
    #        name = segs[2]
    #        ename = segs[3]
    #        pinyin = segs[4]
    #        parentdistrict = segs[5]
    #        isinchina = segs[6]
    #        if pinyin == "":
    #            print l.rstrip()
