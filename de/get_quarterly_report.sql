set hive.cli.print.header=true;

--=============================================================
--游戏次数分类统计
--=============================================================
select t2.logintimes_flag, count(t2.uid) as total from 
(select uid, qt, (case when t.duration>=0 and t.duration<=10 then 'duration_lv1'
                    when t.duration>10 and t.duration<=30 then 'duration_lv2' 
                    when t.duration>30 and t.duration<=60 then 'duration_lv3' 
                    when t.duration>60 and t.duration<=120 then 'duration_lv4' 
                    when t.duration>120 and t.duration<=240 then 'duration_lv5' 
                    else 'duration_lv6' end) as duration_flag, 
            (case when t.logintimes>=0 and t.logintimes<1 then 'logintimes_lv1' 
                    when t.logintimes>=1 and t.logintimes<=3 then 'logintimes_lv2' 
                    when t.logintimes>=4 and t.logintimes<=5 then 'logintimes_lv3'
                    when t.logintimes>=6 and t.logintimes<=10 then 'logintimes_lv4'
                    when t.logintimes>=11 and t.logintimes<=20 then 'logintimes_lv5'
                    else 'logintimes_lv6' end) as logintimes_flag 
from (select * from tmp.temp_cyp_uid_summary) t ) t2 group by t2.qt,t2.logintimes_flag order by logintimes_flag;

--=============================================================
------游戏时长分类统计
--=============================================================
select t2.duration_flag, count(t2.uid) as total from 
(select uid, qt, (case when t.duration>=0 and t.duration<=3 then 'duration_lv1-1'
                    when t.duration>3 and t.duration<=5 then 'duration_lv2-1' 
                    when t.duration>5 and t.duration<=10 then 'duration_lv3-1' 
                    when t.duration>10 and t.duration<=30 then 'duration_lv2' 
                    when t.duration>30 and t.duration<=60 then 'duration_lv3' 
                    when t.duration>60 and t.duration<=120 then 'duration_lv4' 
                    when t.duration>120 and t.duration<=240 then 'duration_lv5' 
                    else 'duration_lv6' end) as duration_flag  
from (select * from tmp.temp_cyp_uid_summary) t ) t2 group by t2.qt,t2.duration_flag order by duration_flag;


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
--select a.platform, b.typename, a.appid, a.accountid, a.validdays from  
--(select appid, typename from warehouse.app_from_db) b join 
--(select platform, appid, accountid, count(distinct `date`) as validdays, sum(duration) as duration from warehouse.online_day where `date`>='${day}' and `date`<='${day2}' and platform in (1,2) 
--group by platform, appid, accountid) a on a.appid=b.appid join (select appid from tmp.temp_cyp_app_summary where dau>=200 and validdays>=30) c on a.appid=c.appid; 
--
--
----=============================================================
----一日玩家比例 step2
----=============================================================
--select t1.platform, t2.typename, t1.oneday_user, t2.total_user, round(t1.oneday_user/t2.total_user, 2) as ratio from  
--(select platform, typename, count(accountid) as oneday_user  from tmp.temp_cyp_oneday_user_quarterly where validdays=1 group by platform, typename) t1 join 
--(select platform, typename, count(accountid) as total_user from tmp.temp_cyp_oneday_user_quarterly group by platform, typename) t2 on t1.platform=t2.platform 
--and t1.typename=t2.typename order by platform, typename;


----=============================================================
--首日付费用户
----=============================================================
--drop table if exists tmp.temp_cyp_new_user_has_payment;
--create table tmp.temp_cyp_new_user_has_payment as 
--select a.*, b.user_num, round(a.first_day_payment_user_num/b.user_num, 4) as rate from 
--(select from_unixtime(cast(firstpaytime as int), 'yyyy-MM-dd') as `date`, platform, appid, count(accountid) as first_day_payment_user_num 
--from warehouse.account_rolling where firstpaytime=firstlogintime 
--group by from_unixtime(cast(firstpaytime as int), 'yyyy-MM-dd'), platform, appid) a join tmp.temp_cyp_dau b on a.appid=b.appid and a.`date`=b.`date` and a.platform=b.platform;

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
--create table tmp.temp_cyp_dau as 
--select t.`date` as dt, t.platform, b.typename, t.appid, t.user_num from 
--(select appid, typename from warehouse.app_from_db) b join 
--(select `date`, platform, appid, count(distinct accountid) as user_num from warehouse.online_day where `date`>='${day}' and `date`<='${day2}' and platform in (1,2) 
--group by `date`, platform, appid) t on t.appid=b.appid join (select appid from tmp.temp_cyp_app_summary where dau>=200 and validdays>=30) t2 on t.appid=t2.appid;

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
--create table tmp.temp_cyp_revenue as 
--select a.`date` as dt, a.platform, b.typename, a.appid, round(a.payamount, 4) as payamount, a.payment_user, c.user_num, round(a.payamount/c.user_num,2) as arpu, a.arppu, round(a.payment_user/c.user_num, 4) as payment_rate from 
--(select appid, typename from warehouse.app_from_db) b join 
--(select `date`, platform, appid, sum(payamount) as payamount, round(sum(payamount)/count(distinct accountid),2) as arppu, count(distinct accountid) as payment_user from warehouse.payment_day where `date`>='${day}' and `date`<='${day2}' and payamount<=10000000 group by `date`, platform, appid) a on a.appid=b.appid 
--join (select appid from tmp.temp_cyp_app_summary where dau>=50 and validdays>=30) d on a.appid=d.appid 
--join tmp.temp_cyp_dau c on a.appid=c.appid and a.platform=c.platform and a.`date`=c.`date`;




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

--drop table if exists tmp.temp_cyp_ltv;
--create table tmp.temp_cyp_ltv as 
--select b.typename, a.appid, a.accountid, c.arpu, round(a.`date`_diff/30, 4) as lt from 
--(select appid, avg(arpu) as arpu from tmp.temp_cyp_revenue where appid<>'7CF98C2DABF843B848D547E589B89A6C' and user_num>=30 group by appid) c join 
--(select * from tmp.temp_cyp_life_time where start_`date`>='2014-09-30' and end_`date`<='2015-09-30' and duration>=60 
--and logintimes>=10 and round(`date`_diff/30, 2) >=0.5) a on a.appid=c.appid join 
--(select appid, typename from warehouse.app_from_db) b on a.appid=b.appid;



--retrain
--drop table if exists tmp.temp_cyp_retain_q3;
--create table tmp.temp_cyp_retain_q3 as 
--select a.platformtype, b.typename, a.appid, round(sum(retain_d1_rate)/count(statitime), 4) as retain_d1_rate, 
--round(sum(retain_d7_rate)/count(statitime), 4) as retain_d7_rate, round(sum(retain_d30_rate)/count(statitime), 4) as retain_d30_rate 
--from tmp.app_retain_day a join (select appid, typename from warehouse.app_from_db) b on a.appid=b.appid 
--group by a.platformtype, b.typename, a.appid;

--drop table if exists tmp.temp_cyp_retain_q3;
--create table tmp.temp_cyp_retain_q3 as 
--select t.platformtype, t.typename, avg(t.retain_d1_rate) as retain_d1_rate2, round(sum(t.retain_d1_rate)/count(t.appid), 4) as retain_d1_rate,  round(sum(t.retain_d7_rate)/count(t.appid), 4) as retain_d7_rate, 
--round(sum(t.retain_d30_rate)/count(t.appid), 4) as retain_d30_rate, count(t.appid) as app_num from 
--(select a.platformtype, b.typename, a.appid, round(sum(retain_d1_rate)/count(statitime), 4) as retain_d1_rate, 
--round(sum(retain_d7_rate)/count(statitime), 4) as retain_d7_rate, round(sum(retain_d30_rate)/count(statitime), 4) as retain_d30_rate 
--from tmp.app_retain_day a join (select appid, typename from warehouse.app_from_db) b on a.appid=b.appid 
--group by a.platformtype, b.typename, a.appid) t group by t.platformtype, t.typename;





--=====================================================
--dragon net app DAU
--=====================================================
--drop table if exists tmp.temp_cyp_dragon_net_dau;
--create table tmp.temp_cyp_dragon_net_dau as 
--select t.`date`, t.platform, b.typename, t.appid, t.user_num from 
--(select appid, typename from warehouse.app_from_db) b join 
--(select `date`, platform, appid, count(distinct accountid) as user_num from warehouse.online_day where `date`>='${day}' and `date`<='${day2}' and platform in (1,2) 
--group by `date`, platform, appid) t on t.appid=b.appid join (select distinct appid from tmp.temp_dragon_net_retain) t2 on t.appid=t2.appid;


--=============================================================
--dragon net revenue
--=============================================================

--drop table if exists tmp.temp_cyp_dragon_net_cumulative_revenue;
--create table tmp.temp_cyp_dragon_net_cumulative_revenue as 
--select a.dt, b.flag, b.platform, sum(coalesce(b.payamount, 0)) as payamount from 
--tmp.temp_cyp_dt a left outer join tmp.temp_cyp_dragon_net_revenue_v2 b on a.dt=b.date group by a.dt, b.flag, platform;

--====================================================
-- LTV 
--====================================================

--******* step1  **********
--drop table if exists tmp.temp_cyp_new_user;
--create table tmp.temp_cyp_new_user as
--select from_unixtime(cast(a.firstlogintime as int), 'yyyy-MM-dd') as dt, a.appid,  a.accountid, a.platform from 
--(select * from tmp.temp_cyp_app_summary where dau>=500 and validdays>=90) b join 
--(select * from warehouse.account_rolling where firstlogintime>=unix_timestamp('${day}', 'yyyy-MM-dd') and firstlogintime<=unix_timestamp('${day2}', 'yyyy-MM-dd')) a on a.appid=b.appid;


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
--tmp.temp_cyp_all_date a left outer join 
--(select flag, dt, platform, sum(payamount) as payamount, count(1) as new_user_pay from tmp.temp_cyp_new_user_daily_payamount group by flag,dt,platform) b 
--on a.dt=b.dt and a.flag=b.flag and a.platform=b.platform;


----******* step4  **********
--统计15日累计付费
--drop table if exists tmp.temp_cyp_new_user_values;
--create table tmp.temp_cyp_new_user_values as 
--select * from 
--(select flag, dt, platform, sum(payamount) over (partition by flag, platform order by dt rows between 0 following and 14 following) as pre_15day_num 
--from tmp.temp_cyp_new_user_payamount_v2) t where dt=split(flag, '_')[0];


--drop table if exists tmp.temp_cyp_new_user_ltv;
--create table tmp.temp_cyp_new_user_ltv as 
--select a.*, b.new_user_num, a.pre_15day_num/b.new_user_num as ltv from 
--(select dt, appid, platform, count(1) as new_user_num from tmp.temp_cyp_new_user group by dt, appid, platform) b join tmp.temp_cyp_new_user_values a 
--on concat(b.dt, "_", b.appid)=a.flag and b.platform=a.platform;


--drop table if exists tmp.temp_cyp_app_overview;
--create table tmp.temp_cyp_app_overview as 
--select d.companyname, d.appname, b.typename, a.platform, a.appid, a.payamount, a.payment_user, a.payment_rate, a.pay_dates, b.dau, b.actives_days, 
--c.new_user_num, c.avg_new_user, c.valid_days, e.retain_d1_rate, e.retain_d7_rate, e.retain_d14_rate, e.retain_d30_rate from 
--(select platform, appid, avg(payamount) as payamount, avg(payment_user) as payment_user, avg(payment_rate) as payment_rate, count(dt) as pay_dates 
--from tmp.temp_cyp_revenue where payment_rate<=0.2 group by platform, appid) a join 
--(select platform, typename, appid, avg(user_num) as dau, count(distinct date) as actives_days from tmp.temp_cyp_dau group by platform, typename, appid) b 
--on a.platform=b.platform and a.appid=b.appid join 
--(select platform, appid, count(1) as new_user_num, count(1)/count(distinct dt) as avg_new_user, count(distinct dt) as valid_days from tmp.temp_cyp_new_user group by platform, appid) c 
--on b.platform=c.platform and b.appid=c.appid join warehouse.app_from_db d on a.appid=d.appid join 
--(select platform, appid, avg(retain_d1_rate) as retain_d1_rate, avg(retain_d7_rate) as retain_d7_rate, avg(retain_d14_rate) as retain_d14_rate, 
--avg(retain_d30_rate) as retain_d30_rate from tmp.temp_cyp_retain group by platform, appid) e 
--on a.platform=e.platform and a.appid=e.appid;
--
--select b.*, a.ltv_15 from (select split(flag, "_")[1] as appid, platform, round(sum(pre_15day_num)/sum(new_user_num), 4) as ltv_15 
--from tmp.temp_cyp_new_user_ltv group by split(flag, "_")[1], platform) a join tmp.temp_cyp_app_overview b on a.appid=b.appid and a.platform=b.platform;
