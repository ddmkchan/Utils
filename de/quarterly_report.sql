--set hive.cli.print.header=true;
--=============================================================
--setp1 统计appid活跃天数，评价dau
--=============================================================
--drop table if exists tmp.temp_cyp_app_summary;
--CREATE TABLE `tmp.temp_cyp_app_summary`(
--  `appid` string, 
--  `dau` double, 
--  `total_user` bigint, 
--  `validdays` bigint)
--partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;


--insert overwrite table tmp.temp_cyp_app_summary partition(qt='${qt}') 
--select t.appid, avg(user_num) as dau, sum(user_num) as total_user, count(`date`) as validdays from 
--(select `date`, appid, count(distinct accountid) as user_num from warehouse.online_day where `date`>='${day}' and `date`<='${day2}' group by `date`,appid) t group by t.appid;


--=============================================================
--step2 每个玩家的游戏次数，游戏时长统计
--=============================================================
--drop table if exists tmp.temp_cyp_uid_summary;
--CREATE TABLE `tmp.temp_cyp_uid_summary`(
--  `platform` string, 
--  `uid` string, 
--  `logintimes` int, 
--  `duration` double, 
--  `total_logintimes` bigint, 
--  `total_duration` double)
--partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--
--
--insert overwrite table tmp.temp_cyp_uid_summary partition(qt='${qt}') 
--select a.platform, concat(a.appid, "_", a.uid) as uid, cast(round((avg(logintimes)), 0) as int) as logintimes, 
--round(avg(duration)/60, 2) as duration, sum(logintimes) as total_logintimes, round(sum(duration)/60,2) as total_duration
--from (select appid from tmp.temp_cyp_app_summary where qt='${qt}' and dau>=200 and validdays>=30) b  
--join (select `date`, platform, uid, appid, logintimes, duration from warehouse.online_day where `date`>='${day}' and `date`<='${day2}') a on a.appid=b.appid group by a.platform, concat(a.appid, "_", a.uid);



--=============================================================
--各游戏类型
--=============================================================
--drop table if exists tmp.temp_cyp_gametype;
--create table tmp.temp_cyp_gametype as 
--select b.typename, a.appid, a.uid, cast(round((avg(logintimes)), 0) as int) as logintimes, 
--round(avg(duration)/60, 2) as duration, sum(logintimes) as total_logintimes, sum(duration) as total_duraton, count(distinct `date`) as validdays from 
--(select appid, typename from warehouse.app_from_db) b join 
--(select `date`, uid, appid, logintimes, duration from warehouse.online_day where  `date`>='${day}' and `date`<='${day2}') a on a.appid=b.appid 
--join (select appid from tmp.temp_cyp_app_summary where dau>=200 and validdays>=30) c on a.appid=c.appid group by b.typename, a.appid, a.uid;



--=============================================================
------各游戏类型下用户占比
--=============================================================
--select t3.typename,t3.duration_flag, t3.user_num, round(t3.user_num/b.total_user, 4) as ratio from  
--(select t2.typename, t2.duration_flag, count(t2.uid) as user_num from 
--(select typename, uid, (case when t.duration>=0 and t.duration<=10 then 'duration_lv1'
--                    when t.duration>10 and t.duration<=30 then 'duration_lv2' 
--                    when t.duration>30 and t.duration<=60 then 'duration_lv3' 
--                    when t.duration>60 and t.duration<=120 then 'duration_lv4' 
--                    when t.duration>120 and t.duration<=240 then 'duration_lv5' 
--                    else 'duration_lv6' end) as duration_flag 
--from tmp.temp_cyp_gametype t) t2 group by t2.typename, t2.duration_flag) t3 join (select typename, count(uid) as total_user from tmp.temp_cyp_gametype group by typename) b 
--on t3.typename=b.typename order by t3.typename, t3.duration_flag; 



--=============================================================
--一日玩家比例
--=============================================================
--drop table if exists tmp.temp_cyp_oneday_user_quarterly;
--create table tmp.temp_cyp_oneday_user_quarterly as 
--select a.platform, e.typename, a.appid, a.accountid, a.validdays, a.duration from  
--(select platform, appid, accountid, count(distinct `date`) as validdays, sum(duration) as duration from warehouse.online_day where `date`>='${day}' and `date`<='${day2}' and platform in (1,2) 
--group by platform, appid, accountid) a join (select appid from tmp.temp_cyp_app_summary where qt='${qt}' and dau>=200 and validdays>=30) c on a.appid=c.appid 
--join tmp.temp_dc_game_type d on c.appid=d.appid
--join tmp.temp_typename_to_dc_game_type e 
--on d.game_type=e.game_type; 


----=============================================================
----一日玩家比例 step2
----=============================================================
--CREATE TABLE `tmp.temp_cyp_oneday_user_rate`(
--  `platform` int, 
--  `typename` string, 
--  `oneday_user` bigint, 
--  `total_user` bigint, 
--  `ratio` double)
--partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;


--insert overwrite table tmp.temp_cyp_oneday_user_rate partition(qt='${qt}')
--select t1.platform, t2.typename, t1.oneday_user, t2.total_user, round(t1.oneday_user/t2.total_user, 2) as ratio from  
--(select platform, typename, count(accountid) as oneday_user  from tmp.temp_cyp_oneday_user_quarterly where validdays=1 group by platform, typename) t1 join 
--(select platform, typename, count(accountid) as total_user from tmp.temp_cyp_oneday_user_quarterly group by platform, typename) t2 on t1.platform=t2.platform 
--and t1.typename=t2.typename order by platform, typename;


----=============================================================
--首日付费用户
----=============================================================
--drop table if exists tmp.temp_cyp_new_user_has_payment;
--create table tmp.temp_cyp_new_user_has_payment as 
--select a.*, b.dau, round(a.first_day_payment_user_num/b.dau, 4) as rate from 
--(select from_unixtime(cast(firstpaytime as int), 'yyyy-MM-dd') as `date`, platform, appid, count(accountid) as first_day_payment_user_num 
--from warehouse.account_rolling where firstpaytime=firstlogintime 
--group by from_unixtime(cast(firstpaytime as int), 'yyyy-MM-dd'), platform, appid) a join tmp.temp_cyp_dau_mau b on a.appid=b.appid and a.`date`=b.dt and a.platform=b.platform;

----=============================================================
--首日付费用户
----=============================================================
--select t.platform, t.typename, round(sum(t.rate)/count(appid), 4) as rate, count(appid) as app_num from 
--(select a.platform, b.typename, a.appid, sum(a.rate)/count(`date`) as rate from (select * from tmp.temp_cyp_new_user_has_payment) a join 
--(select appid from tmp.temp_cyp_app_summary where dau>=200 and validdays>=30) c on a.appid=c.appid join 
--(select appid, typename from warehouse.app_from_db) b on a.appid=b.appid group by a.platform, b.typename, a.appid) t group by t.platform, t.typename;



--=============================================================
--DAU
--=============================================================
--drop table if exists tmp.temp_cyp_dau;
--CREATE TABLE `tmp.temp_cyp_dau`(
--  `date` string, 
--  `platform` int, 
--  `typename` string, 
--  `appid` string, 
--  `user_num` bigint)
--partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--
--
--create table tmp.temp_cyp_dau as 
--insert overwrite table tmp.temp_cyp_dau partition(qt='${qt}')
--select t.`date` as dt, t.platform, b.typename, t.appid, t.user_num from 
--(select appid, typename from warehouse.app_from_db) b join 
--(select `date`, platform, appid, count(distinct accountid) as user_num from warehouse.online_day where `date`>='${day}' and `date`<='${day2}' and platform in (1,2) 
--group by `date`, platform, appid) t on t.appid=b.appid join (select appid from tmp.temp_cyp_app_summary where qt='${qt}' and dau>=200 and validdays>=30) t2 on t.appid=t2.appid;


--drop table if exists tmp.temp_cyp_wau;
--CREATE TABLE `tmp.temp_cyp_wau`(
--  `dayofweek` string, 
--  `platform` int, 
--  `typename` string, 
--  `appid` string, 
--  `user_num` bigint)
--partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--
--
--insert overwrite table tmp.temp_cyp_wau partition(qt='${qt}')
--select t.dayofweek, t.platform, b.typename, t.appid, t.user_num from 
--(select appid, typename from warehouse.app_from_db) b join 
--(select dayofweek, platform, appid, count(distinct accountid) as user_num from warehouse.online_day where `date`>='${day}' and `date`<='${day2}' and platform in (1,2) 
--group by dayofweek, platform, appid) t on t.appid=b.appid join (select appid from tmp.temp_cyp_app_summary where qt='${qt}' and dau>=200 and validdays>=30) t2 on t.appid=t2.appid;




--=============================================================
--MAU
--see quarterly_report.py
--drop table if exists tmp.temp_cyp_dau_2;
--=============================================================



--=============================================================
--DAU / MAU
--=============================================================
--drop table if exists tmp.temp_cyp_dau_mau;
--create table tmp.temp_cyp_dau_mau as 
--select a.`date`, a.platform, c.typename, a.appid, a.user_num as dau, b.user_num as mau, round(a.user_num/b.user_num, 2) as rate 
--from (select * from tmp.temp_cyp_dau where `date`>='${day}' and `date`<'${day2}') a 
--join (select * from tmp.temp_cyp_dau_2 where dt>='${day}' and dt<'${day2}') b on a.`date`=b.dt and a.appid=b.appid and a.platform=b.platform join 
--(select appid, typename from warehouse.app_from_db) c on b.appid=c.appid;


--=============================================================
--DAU / MAU  tmp.temp_cyp_dau_mau_from_db
--=============================================================
--select a.platform, b.typename, round(avg(dau/mau), 2) as rate, count(distinct a.appid) as app_num from  (select * from tmp.temp_cyp_dau_mau_from_db where dau>=200) a join (select appid, typename from warehouse.app_from_db) b on a.appid=b.appid group by a.platform, b.typename;


--=============================================================
--Revenue
--=============================================================
--drop table if exists tmp.temp_cyp_revenue;
--CREATE TABLE `tmp.temp_cyp_revenue`(
--  `dt` string, 
--  `platform` int, 
--  `typename` string, 
--  `appid` string, 
--  `payamount` double, 
--  `payment_user` bigint, 
--  `dau` bigint, 
--  `arpu` double, 
--  `arppu` double, 
--  `payment_rate` double)
--partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;

--insert overwrite table tmp.temp_cyp_revenue partition(qt='${qt}') 
--select a.`date` as dt, a.platform, b.typename, a.appid, round(a.payamount, 4) as payamount, a.payment_user, c.user_num as dau, round(a.payamount/c.user_num, 4) as arpu, a.arppu, round(a.payment_user/c.user_num, 4) as payment_rate from 
--(select appid, typename from warehouse.app_from_db) b join 
--(select `date`, platform, appid, sum(payamount) as payamount, round(sum(payamount)/count(distinct accountid), 4) as arppu, count(distinct accountid) as payment_user from warehouse.payment_day where `date`>='${day}' and `date`<='${day2}' and payamount<=10000000 group by `date`, platform, appid) a on a.appid=b.appid 
--join (select appid from tmp.temp_cyp_app_summary where qt='${qt}' and dau>=50 and validdays>=30) d on a.appid=d.appid 
--join (select * from tmp.temp_cyp_dau where qt='${qt}') c on a.appid=c.appid and a.platform=c.platform and a.`date`=c.date;



--insert overwrite table tmp.temp_cyp_revenue partition(qt='${qt2}') 
--select a.dt, a.platform, b.typename, a.appid, round(a.payamount, 4) as payamount, a.payment_user, c.user_num as dau, round(a.payamount/c.user_num, 4) as arpu, a.arppu, round(a.payment_user/c.user_num, 4) as payment_rate from 
--(select appid, typename from warehouse.app_from_db) b join 
--(select month(`date`) as dt, platform, appid, sum(payamount) as payamount, round(sum(payamount)/count(distinct accountid), 4) as arppu, count(distinct accountid) as payment_user from warehouse.payment_day where `date`>='${day}' and `date`<='${day2}' and payamount<=10000000 group by month(`date`), platform, appid) a on a.appid=b.appid 
--join (select appid from tmp.temp_cyp_app_summary where qt='${qt}' and dau>=50 and validdays>=30) d on a.appid=d.appid 
--join (select * from  tmp.temp_cyp_dau where qt='2016_q1_month') c on a.appid=c.appid and a.platform=c.platform and a.dt=c.date;
--



--=============================================================
--retran tmp.temp_cyp_retain_q4
--=============================================================
--select a.platformtype, b.typename, avg(retain_d1_rate) as retain_d1_rate, avg(retain_d7_rate) as retain_d7_rate, avg(retain_d30_rate) as retain_d30_rate, count(distinct a.appid) as app_num from tmp.temp_cyp_retain_q4 a join warehouse.app_from_db b on a.appid=b.appid group by a.platformtype, b.typename;



--arpu formula one
--select t.platform, t.typename,count(appid) as app_num, round(avg(avg_arpu), 2) as avg_arpu, round(avg(median_arpu),2) as median_arpu, round(avg(7th_arpu), 2) as avg_7th_arpu from 
--(select platform, typename, appid, avg(arpu) as avg_arpu, round(percentile_approx(arpu, array(0.5))[0],2) as median_arpu, round(percentile_approx(arpu, array(0.7))[0],2    ) as 7th_arpu from tmp.temp_cyp_revenue where appid<>'7CF98C2DABF843B848D547E589B89A6C' and user_num>=30 group by platform, typename, appid) t group by t.platform, t.typename;

--arpu formula two
--select platform, typename, count(distinct appid) as app_num, round(avg(arpu), 2) as avg_arpu, round(percentile_approx(arpu, array(0.5))[0],2) as median_arpu, round(percentile_approx(arpu, array(0.7))[0],2) as 7th_arpu from tmp.temp_cyp_revenue where appid<>'7CF98C2DABF843B848D547E589B89A6C' and user_num>=30 group by platform, typename;



--select typename, avg(arpu) as avg_arpu, percentile_approx(arpu, array(0.5))[0] as median_arpu, percentile_approx(lt, array(0.5))[0] as median_lt, percentile_approx(lt, array(0.7))[0] as 7th_lt, 
--percentile_approx(arpu, array(0.5))[0]*percentile_approx(lt, array(0.5))[0] as ltv from tmp.temp_cyp_ltv group by typename;

--====================================================
-- LTV 
--====================================================

--******* step1  **********
--drop table if exists tmp.temp_cyp_new_user_v2;
--CREATE TABLE `tmp.temp_cyp_new_user_v2`(
--  `dt` string, 
--  `appid` string, 
--  `accountid` string, 
--  `platform` int)
--	partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--
--
--insert overwrite table tmp.temp_cyp_new_user_v2 partition(qt='${qt}') 



--drop table if exists tmp.temp_cyp_new_user;
--CREATE TABLE tmp.temp_cyp_new_user as 
--select from_unixtime(cast(a.firstlogintime as int), 'yyyy-MM-dd') as dt, a.appid,  a.accountid, a.platform from 
--(select * from tmp.temp_cyp_app_summary where qt='${qt}' and dau>=500 and validdays>=30) b join 
--(select * from warehouse.account_rolling where firstlogintime>=unix_timestamp('${day}', 'yyyy-MM-dd') and firstlogintime<=unix_timestamp('${day2}', 'yyyy-MM-dd')) a on a.appid=b.appid;


--
--drop table if exists tmp.temp_cyp_new_user_daily_login;
--create table tmp.temp_cyp_new_user_daily_login as 
--select concat(b.dt, '_', b.appid) as flag, a.dt, a.platform, count(distinct b.accountid) as dau from 
--(select * frqm tmp.temp_cyp_new_user) b 
--join (select `date` as dt, platform, appid, accountid   
--from warehouse.online_day where `date`>='${day}' and `date`<='${day2}' and duration>=10 and duration<=86400) a 
--on a.appid=b.appid and a.accountid=b.accountid and a.platform=b.platform group by concat(b.dt, '_', b.appid), a.dt, a.platform; 


--drop table if exists tmp.temp_cyp_new_user_daily_login_v2;
--create table tmp.temp_cyp_new_user_daily_login_v2 as 
--select a.*, coalesce(b.dau, 0) as dau from 
--(select t1.*, t2.dt from (select platform, flag from tmp.temp_cyp_new_user_daily_login group by platform, flag) t1 
--join (select distinct dt from tmp.temp_cyp_new_user_daily_login) t2 on 1=1) a 
--left outer join tmp.temp_cyp_new_user_daily_login b 
--on a.dt=b.dt and a.flag=b.flag and a.platform=b.platform;

--drop table tmp.temp_cyp_daily_retain;
--create table tmp.temp_cyp_daily_retain as 
--select t.*, round(t.dau/t.first_1_user, 4)<=0.013 as low_retain from 
--(select a.*, FIRST_VALUE(dau) OVER(PARTITION by flag, platform ORDER BY dt) AS first_1_user 
--from (select * from tmp.temp_cyp_new_user_daily_login_v2 where dt>=split(flag,'_')[0]) a) t;


--找出连续N日 retain <= 0.013
--set hive.auto.convert.join = false;
--drop table tmp.temp_cyp_user_life_time;
--create table tmp.temp_cyp_user_life_time as 
--select a.platform, a.flag, min(a.dt) as min_dt 
--from tmp.temp_cyp_daily_retain a 
--join tmp.temp_cyp_daily_retain b 
--on date_add(a.dt,1)=b.dt and a.low_retain=b.low_retain and a.platform=b.platform and a.flag=b.flag 
--join tmp.temp_cyp_daily_retain c 
--on date_add(a.dt, 2)=c.dt and a.low_retain=c.low_retain and a.platform=c.platform and a.flag=c.flag 
--where a.low_retain=true group by a.platform, a.flag;

--drop table tmp.temp_cyp_user_life;
--create table tmp.temp_cyp_user_life as 
--select a.platform, a.flag, coalesce(datediff(b.min_dt, split(b.flag,'_')[0]), datediff(a.max_dt, split(a.flag,'_')[0]), 0) as dts 
--from 
--(select platform, flag, max(dt) as max_dt from tmp.temp_cyp_daily_retain where first_1_user>= 3000 group by platform, flag) a 
--left outer join 
--tmp.temp_cyp_user_life_time b 
--on a.platform=b.platform and a.flag=b.flag;
--
--
--
--select b.platform, a.typename, avg(dts) lt from warehouse.app_from_db a join (select * from tmp.temp_cyp_user_life where split(flag, '_')[0]) b on a.appid=split(b.flag, '_')[1] group by b.platform, a.typename;


----******* step2  **********
--新用户每日付费情况
--drop table if exists tmp.temp_cyp_new_user_daily_payamount;
--create table tmp.temp_cyp_new_user_daily_payamount as 
--select concat(b.dt, '_', b.appid) as flag, a.`date` as dt, a.platform, a.appid, b.accountid, a.payamount from 
--(select * from tmp.temp_cyp_new_user) b 
--join (select `date`, platform, appid, accountid, sum(payamount) as payamount 
--from warehouse.payment_day where `date`>='${day}' and `date`<='${day2}' 
--and payamount<=10000000 group by date, platform, appid, accountid) a 
--on a.appid=b.appid and a.accountid=b.accountid and a.platform=b.platform; 


----******* step3  **********
--构建全日期，每批新用户每天的付费情况
--drop table if exists tmp.temp_cyp_new_user_payamount_v2;
--create table tmp.temp_cyp_new_user_payamount_v2 as 
--select a.*, coalesce(b.new_user_pay, 0) as new_user_pay, coalesce(b.payamount, 0) payamount from 
--(select t1.*, t2.dt from (select platform, flag from tmp.temp_cyp_new_user_daily_payamount group by platform, flag) t1 join (select distinct dt from tmp.temp_cyp_all_date where dt>='2015-10-01' and dt<='2016-04-19') t2 on 1=1) a left outer join 
--(select flag, dt, platform, sum(payamount) as payamount, count(1) as new_user_pay from tmp.temp_cyp_new_user_daily_payamount group by flag,dt,platform) b 
--on a.dt=b.dt and a.flag=b.flag and a.platform=b.platform;


------******* step4  **********
----统计15日累计付费
--drop table if exists tmp.temp_cyp_new_user_values;
--create table tmp.temp_cyp_new_user_values as 
--select * from 
--(select flag, dt, platform, 
----sum(payamount) over (partition by flag, platform order by dt rows between 0 following and 7 following) as pre_7day_num, 
--sum(payamount) over (partition by flag, platform order by dt rows between 0 following and 15 following) as pre_15day_num 
----sum(payamount) over (partition by flag, platform order by dt rows between 0 following and 30 following) as pre_30day_num 
--from tmp.temp_cyp_new_user_payamount_v2) t where dt=split(flag, '_')[0];


--drop table if exists tmp.temp_cyp_new_user_ltv;
--create table tmp.temp_cyp_new_user_ltv as 
--select a.*, b.new_user_num, a.pre_15day_num/b.new_user_num as ltv from 
--(select dt, appid, platform, count(1) as new_user_num from tmp.temp_cyp_new_user group by dt, appid, platform) b join tmp.temp_cyp_new_user_values a 
--on concat(b.dt, "_", b.appid)=a.flag and b.platform=a.platform;


--drop table if exists tmp.temp_cyp_app_overview;
--create table tmp.temp_cyp_app_overview as 
--select '${qt}', d.companyname, d.appname, d.typename, a.platform, a.appid, a.payamount, a.payment_user, a.payment_rate, a.pay_dates, b.dau, b.actives_days, 
--c.new_user_num, c.avg_new_user, c.valid_days, e.retain_d1_rate, e.retain_d7_rate, e.retain_d14_rate, e.retain_d30_rate, f.ltv_15 from 
--(select platform, appid, avg(payamount) as payamount, avg(payment_user) as payment_user, avg(payment_rate) as payment_rate, count(dt) as pay_dates 
--from tmp.temp_cyp_revenue where dt>='${day1}' and dt<='${day2}' and payment_rate<=0.2 group by platform, appid) a join 
--(select platform, appid, avg(user_num) as dau, count(distinct date) as actives_days from tmp.temp_cyp_dau where date>='${day1}' and date<='${day2}' group by platform, appid) b 
--on a.platform=b.platform and a.appid=b.appid join 
--(select platform, appid, count(1) as new_user_num, count(1)/count(distinct dt) as avg_new_user, count(distinct dt) as valid_days from tmp.temp_cyp_new_user where dt>='${day1}' and dt<='${day2}' group by platform, appid) c 
--on b.platform=c.platform and b.appid=c.appid join warehouse.app_from_db d on a.appid=d.appid join 
--(select platform, appid, avg(retain_d1_rate) as retain_d1_rate, avg(retain_d7_rate) as retain_d7_rate, avg(retain_d14_rate) as retain_d14_rate, 
--avg(retain_d30_rate) as retain_d30_rate from tmp.temp_cyp_retain where dt>='${day1}' and dt<='${day2}' group by platform, appid) e 
--on a.platform=e.platform and a.appid=e.appid join 
--(select split(flag, '_')[1] as appid, platform, sum(pre_15day_num)/sum(new_user_num) as ltv_15 from tmp.temp_cyp_new_user_ltv where dt>='${day1}' and dt<='${day2}' group by split(flag, '_')[1],  platform) f
--on a.platform=f.platform and a.appid=f.appid;
--

--select b.*, a.ltv_15 from (select split(flag, "_")[1] as appid, platform, round(sum(pre_15day_num)/sum(new_user_num), 4) as ltv_15 
--from tmp.temp_cyp_new_user_ltv group by split(flag, "_")[1], platform) a join tmp.temp_cyp_app_overview b on a.appid=b.appid and a.platform=b.platform;

--select '${qt}', d.companyname, d.appname, d.typename, a.platform, a.appid, a.payamount, a.payment_user, a.payment_rate, a.pay_dates, b.dau, b.actives_days, 
--c.new_user_num, c.avg_new_user, c.valid_days, e.retain_d14, f.ltv_15 from 
--(select platform, appid, avg(payamount) as payamount, avg(payment_user) as payment_user, avg(payment_rate) as payment_rate, count(dt) as pay_dates 
--from tmp.temp_cyp_revenue where dt>='${day1}' and dt<='${day2}' and payment_rate<=0.2 group by platform, appid) a join 
--(select platform, appid, avg(user_num) as dau, count(distinct date) as actives_days from tmp.temp_cyp_dau where date>='${day1}' and date<='${day2}' group by platform, appid) b 
--on a.platform=b.platform and a.appid=b.appid join 
--(select platform, appid, count(1) as new_user_num, count(1)/count(distinct dt) as avg_new_user, count(distinct dt) as valid_days from tmp.temp_cyp_new_user where dt>='${day1}' and dt<='${day2}' group by platform, appid) c 
--on b.platform=c.platform and b.appid=c.appid join warehouse.app_from_db d on a.appid=d.appid join 
--(select platform, split(flag,"_")[1] appid, sum(dau)/sum(first_1_user) as retain_d14 
--from tmp.temp_cyp_daily_retain where dt>='${day1}' and dt<='${day2}' and 
--split(flag, '_')[0] <= '2016-03-15' and datediff(dt, split(flag,'_')[0])=14 group by platform, split(flag, "_")[1]) e 
--on a.platform=e.platform and a.appid=e.appid  join 
--(select split(flag, '_')[1] as appid, platform, sum(pre_15day_num)/sum(new_user_num) as ltv_15 from tmp.temp_cyp_new_user_ltv where dt>='${day1}' and dt<='${day2}' group by split(flag, '_')[1],  platform) f
--on a.platform=f.platform and a.appid=f.appid;


