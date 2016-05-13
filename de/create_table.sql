--drop table if exists tmp.temp_cyp_dragon_net_sum_payamount;
--CREATE table tmp.temp_cyp_dragon_net_sum_payamount(
--    appid                   string,                                      
--    payamount                float) 
--partitioned by (dt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;

--CREATE table tmp.temp_dragon_net_app as 
--select a.*,b.appid from tmp.temp_dragon_net_game a join warehouse.app_from_db b on a.app_name=b.appname and b.companyname=a.company;
--

--drop table tmp.temp_cyp_all_date;
--create table tmp.temp_cyp_all_date (
--	dt string)
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/all_date' overwrite into table tmp.temp_cyp_all_date;

drop table if exists tmp.temp_cyp_adv_game_summary_v2;
CREATE table tmp.temp_cyp_adv_game_summary_v2(
	dt string,
	adv_game_detail_id int,
	position_type_name string,
	channel_name string,
	position_name string,
	game_name string,
	company string,
	network_type string, 
	screen_type string,
	gameplay string,
	theme string)
	partitioned by (month string)  
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
----load data local inpath '/data2/yanpengchen/scripts/adv_rw' overwrite into table tmp.temp_cyp_adv_game_summary;


--drop table if exists tmp.temp_cyp_fault_codes;
--CREATE table tmp.temp_cyp_fault_codes(
--	id int,
--	sys string,
--	code string,
--	description string,
--	fault_id string)
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/remote_fault_codes_0503' overwrite into table tmp.temp_cyp_fault_codes;


--drop table if exists tmp.temp_cyp_channel_name;
--CREATE table tmp.temp_cyp_channel_name(
--value string,
--vkey string)
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/channel_name' overwrite into table tmp.temp_cyp_channel_name;


--drop table if exists tmp.temp_cyp_new_game_value;
--CREATE table tmp.temp_cyp_new_game_value(
--    name string,
--    dt string,
--    channel string,
--    channel_weight int,
--	rank int,
--    rank_weight int,
--    flag int)
--	partitioned by (month string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/new_game_value' overwrite into table tmp.temp_cyp_new_game_value;



--load data local inpath '/data2/yanpengchen/scripts/app_retain_day_q4.txt' overwrite into table tmp.temp_cyp_retain partition;


--drop table if exists tmp.tv_game_channel_day;
--CREATE table tmp.tv_game_channel_day(
--value string, vkey string,channelid int,dau int,wau int,MAU int,NewEquipNum int,NewPayPlayerNum int,FirstDayPayNum int,Amount int,RechargeNum int,appid string,
--dt string)
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--load data local inpath '/root/yanpengchen/scripts/tv_games_channel_info.txt' overwrite into table tmp.tv_game_channel_day;
--
--drop table if exists tmp.tv_game_channel_retain;
--create table tmp.tv_game_channel_retain(
--PlatformType int,appid string,dt string,retain_1 float,retain_30 float,retain_7 float,retain_d1_rate float,retain_d30_rate float, retain_d7_rate float,total_new_user_num int)
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--load data local inpath '/root/yanpengchen/scripts/tv_games_retain' overwrite into table tmp.tv_game_channel_retain;

--drop table if exists tmp.temp_dc_game_type;
--CREATE table tmp.temp_dc_game_type(
--	appid string,
--	game_type string)
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/dc_game_type.txt' overwrite into table tmp.temp_dc_game_type;


--drop table if exists tmp.temp_typename_to_dc_game_type;
--CREATE table tmp.temp_typename_to_dc_game_type(
--	typename string,
--	game_type string)
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/typename_to_dc_game_type' overwrite into table tmp.temp_typename_to_dc_game_type;


--drop table if exists tmp.temp_cyp_dau_mau;
--CREATE table tmp.temp_cyp_dau_mau(
--	platform               int,
--	dau               int,
--	wau               int,
--	mau               int,
--	appid               string,
--	dt               string) 
--	partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' stored as textfile;

--drop table if exists tmp.temp_cyp_retain;
--CREATE table tmp.temp_cyp_retain(
--    platform int,
--    appid string,
--    dt string,
--    retain_1 int,
--    retain_14 int,
--    retain_30 int, 
--    retain_7 int,
--    retain_d14_rate float,
--    retain_d1_rate float,
--    retain_d30_rate float,
--    retain_d7_rate float,
--    total_new_user_num int)
--partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' stored as textfile;


--drop table if exists tmp.temp_cyp_report_with_vin_code;
--CREATE table tmp.temp_cyp_report_with_vin_code(
--	vin_code string,
--	remote_report_id int) 
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/vcc' overwrite into table tmp.temp_cyp_report_with_vin_code;


--drop table if exists tmp.temp_cyp_ctr_train;
--CREATE table tmp.temp_cyp_ctr_train(
--	id string, 
--	click string, 
--	hour string, 
--	C1 string, 
--	banner_pos string, 
--	site_id string, 
--	site_domain string, 
--	site_category string, 
--	app_id string, 
--	app_domain string, 
--	app_category string, 
--	device_id string, 
--	device_ip string, 
--	device_model string, 
--	device_type string, 
--	device_conn_type string, 
--	C14 string, 
--	C15 string, 
--	C16 string, 
--	C17 string, 
--	C18 string, 
--	C19 string, 
--	C20 string, 
--	C21 string)
--ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' stored as textfile;
--load data local inpath '/data2/yanpengchen/train' overwrite into table tmp.temp_cyp_ctr_train;




--drop table if exists tmp.temp_cyp_sys_code;
--CREATE table tmp.temp_cyp_sys_code(
--	sys               string,
--	categroy               string) 
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/sys_code' overwrite into table tmp.temp_cyp_sys_code;
--
--
--drop table if exists tmp.temp_cyp_sys_code_map;
--CREATE table tmp.temp_cyp_sys_code_map(
--	categroy               string,
--	sys               string,
--	parent_category string,
--	parent_sys               string) 
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/sys_code_map' overwrite into table tmp.temp_cyp_sys_code_map;


--drop table if exists tmp.temp_cyp_dau_mau;
--CREATE table tmp.temp_cyp_dau_mau(
--	platform               int,
--	dau               int,
--	wau               int,
--	mau               int,
--	appid               string,
--	dt               string) 
--	partitioned by (qt string)  
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' stored as textfile;

--create table tmp.temp_cyp_fc_map(
--	sys               string,
--	target_sys               string,
--	category               string,
--	ratio               float,
--	is_match               string) 
--ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' stored as textfile;
--load data local inpath '/data2/yanpengchen/scripts/fc_map_0412' overwrite into table tmp.temp_cyp_fc_map;

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
--load data local inpath '/data2/yanpengchen/scripts/app_retain_day_q4.txt' overwrite into table tmp.temp_cyp_retain partition;
--load data local inpath '/data2/yanpengchen/winterfall/building_match/out' overwrite into table tmp.temp_cyp_triprecord partition(dt='${dt}');



--drop table tmp.temp_cyp_geocoding;
--create table tmp.temp_cyp_geocoding(
--	latlng               string,
--	province               string,
--	city               string,
--	street               string,
--	distance               int,
--	poi_name               string,
--	poi_type               string,
--	lat               string,
--	lon               string) 
--ROW FORMAT DELIMITED FIELDS TERMINATED BY ' ' LINES TERMINATED BY '\n' stored as textfile;
--load data local inpath '/data2/yanpengchen/winterfall/building_match/rs_150505' overwrite into table tmp.temp_cyp_geocoding;
