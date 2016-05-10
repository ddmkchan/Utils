--drop table tmp.temp_cyp_triprecord;
--create table tmp.temp_cyp_triprecord(
--	latlng               string,
--	province               string,
--	city               string,
--	street               string,
--	distance               int,
--	poi_name               string,
--	poi_type               string,
--	lat               string,
--	lon               string) 
--	partitioned by (dt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY ' ' LINES TERMINATED BY '\n' stored as textfile;

--add jar udf-0.0.1.jar;
--create temporary function day_of_week as 'data.eye.dc.udf.DayOfWeek';
--select t.*, int(download_num)-int(last_1_time) as down  from 
--(select dt, title, download_num, LAG(download_num, 1, -1) OVER (PARTITION by title order by dt) last_1_time from  tmp.kc_game_info) t where t.last_1_time!=-1;



--select n,ts, rt, tm, so s_lat, sa s_lon, eo e_lat, ea e_lon from launch_triprecord.p_triprecord where so<>'' and sa<>'' and eo<>'' and ea<>'' and tm>10 limit 3000;

--select substring(c,0,10) dt, so, sa, eo, ea from launch_triprecord.p_triprecord where coalesce(so, '')<>'' and coalesce(sa, '')<>'' and coalesce(eo, '')<>'' and coalesce(eo, '')<>'' and substring(c, 0, 10)>='2015-04-26' and substring(c, 0, 10)<='2015-04-28';

--drop table tmp.temp_cyp_min_poi;
--create table tmp.temp_cyp_min_poi as select split(latlng, ',')[0] as s_lat, split(latlng, ',')[1] as s_lng, *, 
--ROW_NUMBER() OVER(PARTITION BY latlng ORDER BY distance) as rn from tmp.temp_cyp_triprecord;

drop table tmp.temp_cyp_trip_with_poi;
create table tmp.temp_cyp_trip_with_poi as 
select st, et, n, ts, rt, tm, coalesce(b.city, '未知') city1, coalesce(c.city, '未知') city2, coalesce(b.street, '未知') street1,  coalesce(c.street, '未知') street2, coalesce(b.poi_name, '未知') as start_poi, coalesce(c.poi_name, '未知') as end_poi from 
(select * from launch_triprecord.p_triprecord where substring(c, 0, 10) in ('2015-04-29','2015-04-30','2015-05-01','2015-05-05', '2015-09-22') and coalesce(so, '')<>'' and coalesce(sa, '')<>'' and coalesce(eo, '')<>'' and coalesce(eo, '')<>'') a 
left outer join (select * from tmp.temp_cyp_min_poi where rn=1) b on a.so=b.s_lng and a.sa=b.s_lat 
left outer join (select * from tmp.temp_cyp_min_poi where rn=1) c on a.eo=c.s_lng and a.ea=c.s_lat;



--select * from tmp.temp_cyp_trip_with_poi where city1='深圳市' and street1<>'未知' and street2<>'未知' and start_poi<>'未知' and end_poi<>'未知' limit 100;
