# -*- coding: utf-8 -*- 
import urllib

def view_bar(num=1, sum=100, bar_word="."):   
    #打印进度条
    rate = float(num) / float(sum)   
    rate_num = int(rate * 100)   
    print '\r%d%% :' %(rate_num),   
    for i in range(0, num):   
        os.write(1, bar_word)   
    sys.stdout.flush()   

def cbk(a, b, c):
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' % per
    #logger.info('%.2f%%' % per)


if __name__ == "__main__":
    urllib.urlretrieve("http://img.kantuban.com/pin/d90d2a11556d4c9ed1b49f5341b2da21", "/home/chenyp/dm/zhaohaowan/tt.jpg", cbk)
