##########################################################
## 功能：从mysql导数据到hive
##########################################################

## 全表
table="
d_thirdplatform_fee_conf
d_jfz_channel_conf
d_flow_url_conf
d_gxq_channel_conf
d_bp_click_conf
d_simulate_model_conf
d_cfgl_invest_adviser_conf
d_tuig_cfgl_channel_conf
d_cfgl_vip_test_account_conf
"

mysql_comm="mysql -h10.1.2.74 -uroot -pMysql!@#1 -Djfz_result --default-character-set=utf8"
dir="/data/conf"

for table_name in `echo $table`
do
    echo $table_name
    echo "select * from jfz_result.${table_name}" | $mysql_comm | sed '1d' > ${dir}/${table_name}.txt
    cnt=`wc -l ${dir}/${table_name}.txt | awk -F" " '{print $1 }' `
    if [ $cnt -le 0 ]
    then
        exit
    fi

    hive -e "load data local inpath \"${dir}/${table_name}.txt\" overwrite into table jfz_result.$table_name" 

done

##分区表
table="
"
date_curr=`date -d "$date_begin 1 day ago" "+%Y%m%d"`

mysql_comm="mysql -h10.1.2.74 -uroot -pMysql!@#1 -Djfz_result --default-character-set=utf8"
dir="/data/conf"

for table_name in `echo $table`
do
    echo $table_name
    echo "select * from jfz_result.${table_name} where stat_date=$date_curr" | $mysql_comm | sed '1d' > ${dir}/${table_name}.txt
    cnt=`wc -l ${dir}/${table_name}.txt | awk -F" " '{print $1 }' `
    if [ $cnt -le 0 ]
    then
        exit
    fi

    hive -e "load data local inpath \"${dir}/${table_name}.txt\" overwrite into table jfz_result.$table_name partition (dt=$date_curr)" 

done
