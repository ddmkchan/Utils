#!/bin/bash

#db to hive for one

source /var/rep/skd/common.sh

date_curr=`date -d "1 day ago" "+%Y%m%d"`
date_10d_ago=`date -d "10 day ago" "+%Y%m%d"`
echo $date_curr
dir="/data/rawdata/$date_curr"
echo $dir
cd $dir

tableName=$1
database=$2



if [[ $tableName =~ article_user_\d* ]] || [[ $tableName =~ comment_articl_\d* ]]
then
        sed -i 's/"from"/"source_type"/' $tableName.txt
else
        sed -i '1d' $tableName.txt

fi

echo "load data local inpath '${tableName}.txt' overwrite into table ${database}.${tableName} partition (dt=$date_curr)"

hive -e "load data local inpath '${tableName}.txt' overwrite into table ${database}.${tableName} partition (dt=$date_curr)"

if [ $tableName != clickstream ]&&[ $tableName != gxq_app_action_logs ]&&[ $tableName != T_INVEST ]&&[ $tableName != user_combine_fund_shares ]&&[ $tableName != gxq_vir_asset_trading_record ]&&[ $tableName != itc_policy ]&&[ $tableName != jfz_app_logs ]&&[ $tableName != T_GAMBLING_USER_STATS ]&&[ $tableName != ttfund_user_asset ]&&[ $tableName != gxq_scoin_task_record ]
then
	hive -e "use ${database}; alter table ${database}.${tableName} drop partition (dt=$date_10d_ago)"
fi
