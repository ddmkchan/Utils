#!/usr/bin/python
#-*- coding:utf-8 -*-
import pandas as pd
import pandas.io.sql as sql
import datetime
import time
import sys
from get_logger import *
import traceback
from define import *
mylogger = get_logger('h5_report')

def get_id_map():
	id_map = {}
	with open('dbconf_v2.txt') as f:
		for line in f.readlines():
			company_id, appid, server_id, port = line.rstrip().split('\t')
			conn = conn_map.get("%s_%s" % (server_id, port))
			id_map[appid] = (company_id, conn)
	return id_map

def get_game_type_summary():
    d = {'appid':[], 'typename':[]}
    for line in open('h5_apps').readlines():
        appid, typename = line.rstrip().split('\t')
        d['appid'].append(appid)
        d['typename'].append(typename)
    df = pd.DataFrame(d)
    gb = df.groupby('typename').size()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)

def get_h5_summary_by_appid(company_id, appid, typename, start_date, end_date, conn):

    """
    Appid_dc_everyday_h5：TotalPv1/TotalPv(首页跳出率） 
    childNodeCount/parentNodeCount （活跃k系数）
    """
    df = pd.DataFrame()
    _sql = "select StatiTime, sum(TotalPv) as TotalPv,sum(TotalUv) as TotalUv, sum(UniqIP) as UniqIP, \
    sum(TotalSession) as TotalSession, IF(sum(TotalPv)>0, round(sum(TotalPv1)/sum(TotalPv),4), 0) as run_off_rate, \
    IF(sum(ParentNodeCount)>0, round(sum(ChildNodeCount)/sum(ParentNodeCount), 4), 0) as active_k_rate \
    from dc_%s.%s_dc_everyday_h5 where PlayerType=2 and StatiTime>=%s and StatiTime<=%s \
    group by StatiTime" % (company_id, appid, start_date, end_date)
    df = sql.read_sql(_sql, conn)
    df['AppId'] = appid
    df['TypeName'] = typename
    dt = [datetime.date.fromtimestamp(int(i)) for i in df['StatiTime']]
    df['dt'] = dt
    del df['StatiTime']
    return df

def get_h5_duration_by_appid(company_id, appid, typename, start_date, end_date, conn):

    """
    对应活跃用户页面
    每次游戏时长分布, 每日累计游戏时长分布 (minute)
    """

    df = pd.DataFrame()
    _sql = "select a.StatiTime, b.new_user_num, a.activet_user_num, a.activet_user_num-b.new_user_num as old_user_num, a.TotalSession, a.cost_per_uv, a.cost_per_sess \
    from (select StatiTime, sum(TotalUv) as activet_user_num, sum(TotalSession) as TotalSession,sum(TotalOnlineTime)/sum(TotalUv)/60 as cost_per_uv, \
    sum(TotalOnlineTime)/sum(TotalSession)/60 as cost_per_sess from dc_%s.%s_dc_everyday_h5 where PlayerType=2 and StatiTime>=%s and StatiTime<=%s group by StatiTime) a \
    join (select StatiTime, sum(TotalUv) as new_user_num from dc_%s.%s_dc_everyday_h5 where PlayerType=1 and StatiTime>=%s and StatiTime<=%s group by StatiTime) b on a.StatiTime=b.StatiTime" % (company_id, appid, start_date, end_date, company_id, appid, start_date, end_date)
    df = sql.read_sql(_sql, conn)
    df['AppId'] = appid
    df['TypeName'] = typename
    dt = [datetime.date.fromtimestamp(int(i)) for i in df['StatiTime']]
    df['dt'] = dt
    del df['StatiTime']
    return df


def get_h5_payamount_by_appid(company_id, appid, typename, start_date, end_date, conn):
    
    """
    每日付费率, 
    Appid_dc_payment_by_day_h5中的PayNum;
    活跃是Appid_dc_everyday_h5中的TotalUv
    ARPPU
    """

    df = pd.DataFrame()
    _sql = "select a.*, b.TotalUv, a.PayNum/b.TotalUv as payment_rate, a.PayAmount/a.PayNum as arppu \
    from (select StatiTime, sum(PayAmount) as PayAmount, sum(PayTimes) as PayTimes, sum(PayNum) as PayNum from dc_%s.%s_dc_payment_by_day_h5 where StatiTime>=%s and StatiTime<=%s group by StatiTime) a \
    join (select StatiTime, sum(TotalUv) as TotalUv \
    from dc_%s.%s_dc_everyday_h5 where PlayerType=2 and StatiTime>=%s and StatiTime<=%s group by StatiTime) b on a.StatiTime=b.StatiTime" % (company_id, appid, start_date, end_date, company_id, appid, start_date, end_date)
    df = sql.read_sql(_sql, conn)
    df['AppId'] = appid
    df['TypeName'] = typename
    dt = [datetime.date.fromtimestamp(int(i)) for i in df['StatiTime']]
    df['dt'] = dt
    del df['StatiTime']
    return df


def get_h5_retain_summary_by_appid(company_id, appid, typename, start_date, end_date, conn):

    """
    Front_Appid_dc_retain_by_day_h5（新增留存）/Appid_dc_everyday_h5（新增）
    """

    df = pd.DataFrame()
    _sql = "select a.StatiTime, a.TotalUv, if(a.TotalUv>0, round(b.RetainedNum_1/a.TotalUv, 4), 0) as retain_rate_1, if(a.TotalUv>0, round(b.RetainedNum_7/a.TotalUv, 4), 0) as retain_rate_7, if(a.TotalUv>0, round(b.RetainedNum_3/a.TotalUv, 4), 0) as retain_rate_3 from  \
    (select StatiTime, sum(TotalUv) as TotalUv from dc_%s.%s_dc_everyday_h5 where StatiTime>=%s and StatiTime<=%s and PlayerType=1 group by StatiTime) a join \
    (select StatiTime, sum(RetainedNum_1) as RetainedNum_1, sum(RetainedNum_7) as RetainedNum_7, sum(RetainedNum_3) as RetainedNum_3 from dc_%s.Front_%s_dc_retain_by_day_h5 where StatiTime>=%s \
    and StatiTime<=%s and PlayerType=1 group by StatiTime) b on a.StatiTime=b.StatiTime" % (company_id, appid, start_date, end_date, company_id, appid, start_date, end_date)
    df = sql.read_sql(_sql, conn)
    df['TypeName'] = typename
    df['AppId'] = appid
    dt = [datetime.date.fromtimestamp(int(i)) for i in df['StatiTime']]
    df['dt'] = dt
    del df['StatiTime']
    return df

def get_new_user_num_by_appid(company_id, appid, start_date, end_date, conn):
    df = pd.DataFrame()
    _sql = "select StGatiTime, PlatformType, sum(num) as total_new_user_num\
                from dc_%s.Front_%s_dc_everyday \
                where StatiTime >= %s  and StatiTime <= %s and PlayerType=1 \
                and GameRegionID in (select Seqno from dc_%s.dc_custom_id where AppID = \'%s\' and type = 2 and vkey = '_ALL_GS') \
                group by StatiTime, PlatformType;"% (company_id, appid, start_date, end_date, company_id, appid)
    df = sql.read_sql(_sql, conn)
    df['appid'] = appid
    return df


def get_h5_data_from_db(start_date, end_date, func, output):
	df = pd.DataFrame()
	start_date = int(time.mktime(time.strptime('%s 00:00:00' % start_date, '%Y-%m-%d %H:%M:%S')))
	end_date = int(time.mktime(time.strptime('%s 00:00:00' % end_date, '%Y-%m-%d %H:%M:%S')))
	id_map = get_id_map()
	valid_apps = set([j.rstrip() for j in open('valid_h5_appid').readlines()])
	with open('h5_apps') as f:
		for line in f.readlines()[:]:
			try:
				appid, typename = line.rstrip().split('\t')
				#if appid in id_map:
				if appid in id_map and appid in valid_apps:
					company_id, conn = id_map.get(appid)
					mylogger.info("%s\t%s\t%s" % (appid, company_id, conn))
					for dt in range(start_date, end_date, 86400 * 30):
						dt2 = end_date if dt+86400*29 > end_date else dt+86400*29
						_df = func(company_id, appid, typename, dt, dt2, conn)
						df = pd.concat([df, _df])
						time.sleep(0.5)
			except Exception,e:
				mylogger.error(traceback.format_exc())
	df.to_csv(output)

    #company_id, conn = id_map.get(appid)

    #retain_df = get_retain_summary_by_appid(company_id, appid, start_date, end_date, conn)
    #print retain_dfG
    #print get_duration_by_appid(company_id, appid, start_date, end_date, conn)
    #print get_payamount_by_appid(company_id, appid, start_date, end_date, conn)
            
def retain_summary():
    retain_df = pd.read_csv("h5_retain_q1")
    #filter = retain_df['retain_rate_1'].quantile(0.4)
    #print filter
    retain_df = retain_df[(retain_df.TotalUv>100) & (retain_df.retain_rate_1>0) & (retain_df.retain_rate_3>0) & (retain_df.retain_rate_7>0)]
    gb = retain_df.groupby('TypeName')['retain_rate_1'].mean()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = retain_df.groupby('TypeName')['retain_rate_1'].quantile(0.75)
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = retain_df.groupby('TypeName')['retain_rate_3'].mean()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print
    gb = retain_df.groupby('TypeName')['retain_rate_3'].quantile(0.75)
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = retain_df.groupby('TypeName')['retain_rate_7'].mean()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print
    gb = retain_df.groupby('TypeName')['retain_rate_7'].quantile(0.75)
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = retain_df.groupby('TypeName').AppId.nunique()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print "%s\t%s" % (retain_df['retain_rate_1'].mean(), retain_df['retain_rate_1'].quantile(0.75))
    print "%s\t%s" % (retain_df['retain_rate_3'].mean(), retain_df['retain_rate_3'].quantile(0.75))
    print "%s\t%s" % (retain_df['retain_rate_7'].mean(), retain_df['retain_rate_7'].quantile(0.75))

def active_summary():
    df = pd.read_csv("h5_summary_q1")
    #df = df[(df.TotalPv>100) & (df.active_k_rate<=200)]
    df = df[(df.TotalPv>200) & (df.active_k_rate<=200) & (df.run_off_rate<=0.75)]
    gb = df.groupby('TypeName')['run_off_rate'].mean()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName')['run_off_rate'].quantile(0.5)
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName')['run_off_rate'].quantile(0.7)
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName')['active_k_rate'].mean()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName')['active_k_rate'].quantile(0.5)
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName')['active_k_rate'].quantile(0.7)
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName').AppId.nunique()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    #print pd.DataFrame.mean(df['run_off_rate'])
    print df['run_off_rate'].mean(), df['run_off_rate'].median(), df['run_off_rate'].quantile(0.3)
    print df['active_k_rate'].mean(), df['active_k_rate'].median(), df['active_k_rate'].quantile(0.3)

def duration_summary():
	df = pd.read_csv("h5_duration_q1")
	df = df[(df.activet_user_num>=100) & (df.cost_per_uv<=120)]
	print len(df)
	gb = df.groupby('TypeName')['cost_per_uv'].mean()
	for k, v in gb.iteritems():
		print "%s\t%s" % (k, v)
	print 
	gb = df.groupby('TypeName')['cost_per_uv'].median()
	for k, v in gb.iteritems():
		print "%s\t%s" % (k, v)
	print 
	gb = df.groupby('TypeName')['cost_per_sess'].mean()
	for k, v in gb.iteritems():
		print "%s\t%s" % (k, v)
	print 
	gb = df.groupby('TypeName')['cost_per_sess'].median()
	for k, v in gb.iteritems():
		print "%s\t%s" % (k, v)
	print 
	gb = df.groupby('TypeName').AppId.nunique()
	for k, v in gb.iteritems():
		print "%s\t%s" % (k, v)
	print "%s\t%s" % (df['cost_per_uv'].mean(), df['cost_per_uv'].quantile(0.5))
	print "%s\t%s" % (df['cost_per_sess'].mean(), df['cost_per_sess'].quantile(0.5))


def payment_summary():
    df = pd.read_csv("h5_payamount_q1")
    df = df[(df.PayAmount>0) & (df.PayNum>0) & (df.arppu<=500) & (df.payment_rate>=0)]
    gb = df.groupby('TypeName')['payment_rate'].mean()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName')['payment_rate'].quantile(0.5)
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName')['arppu'].mean()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName')['arppu'].quantile(.5)
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    gb = df.groupby('TypeName').AppId.nunique()
    for k, v in gb.iteritems():
        print "%s\t%s" % (k, v)
    print 
    print df['payment_rate'].mean(), df['payment_rate'].median()
    print df['arppu'].mean(), df['arppu'].median()


def main():
	start = '2016-01-01'
	end = '2016-03-29'
	#get_h5_data_from_db(start, end, get_h5_duration_by_appid, 'h5_duration_q1')
	get_h5_data_from_db(start, end, get_h5_summary_by_appid, 'h5_summary_q1')
	get_h5_data_from_db(start, end, get_h5_payamount_by_appid, 'h5_payamount_q1')
	get_h5_data_from_db(start, end, get_h5_retain_summary_by_appid, 'h5_retain_q1')
	mylogger.info("done!!!")


if __name__=="__main__":
    #duration_summary()
    #retain_summary()
    #active_summary()
    payment_summary()
	#main()
