#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

__version__ = '0.9'
__all__ = ["PinYin"]

import os.path
import itertools
import copy

class PinYin(object):
    def __init__(self, dict_file='newword.data'):
        self.word_dict = {}
        self.dict_file = dict_file


    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with file(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]


    def hanzi2pinyin(self, string=""):
        result = []

        if not isinstance(string, unicode):
            string = string.decode("utf-8")
        
        for char in string:
            key = '%X' % ord(char)
            #pys = self.word_dict.get(key, "")
            #if pys:
            #    pinyins = pys.split()
            pinyins = self.word_dict.get(key, char).split()
            result.append([p.lower() for p in pinyins])

        return result

    def hanzi2pinyin_split(self, string="", split=""):
        result = self.hanzi2pinyin(string=string)
        if split == "":
            return result
        else:
            return split.join(result)

def Cartesian_product(_list):
    rs = []
    source = copy.copy(_list)
    _index = 2
    while len(_list) >= 2:
        tmp = ["%s %s" % (x[0], x[1]) for x in itertools.product(_list[0], _list[1])]
        if len(_list) > 2:
            _list = [tmp]
            _list.extend(source[_index:])
            _index += 1
        else:
            rs = tmp
            break
    return rs

if __name__ == "__main__":
    test = PinYin()
    test.load_word()
    string = "重启(重庆店)"
    print "in: %s" % string
    print test.hanzi2pinyin(string=string)
    #print Cartesian_product(test.hanzi2pinyin(string=string))
