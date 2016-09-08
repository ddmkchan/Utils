##########################################################
##业务数据入库
##########################################################
#!/bin/bash
source $HOME/.bash_profile
export LANG=zh_CN.UTF-8
## 日任务执行

cd "/var/rep/shell"

if [ $# == 0 ]
then
    date_curr=`date -d "1 day ago" "+%Y%m%d"`
elif [ $# == 1 ]
then
    date_curr=$1
else
        echo "Usage $0 or $0 date_curr date_dt"
        exit
fi
date_10d_ago=`date -d "10 day ago" "+%Y%m%d"`
echo $date_curr
dir="/data/rawdata/$date_curr"
echo $dir
cd $dir
for table_name in `ls *.txt`
do
  echo ${table_name%%.*}
  echo $table_name 
  sed -i '1d' $table_name 
  hive -e "load data local inpath '$table_name' overwrite into table jfz_rawdata.${table_name%%.*} partition (dt=$date_curr)"
  if [ $table_name != clickstream.txt ]&&[ $table_name != gxq_app_action_logs.txt ]&&[ $table_name != T_INVEST.txt ]&&[ $table_name != user_combine_fund_shares.txt ]&&[ $table_name != gxq_vir_asset_trading_record.txt ]&&[ $table_name != itc_policy.txt ]&&[ $table_name != jfz_app_logs.txt ]&&[ $table_name != T_GAMBLING_USER_STATS.txt ]&&[ $table_name != ttfund_user_asset.txt ]&&[ $table_name != gxq_scoin_task_record.txt ]
  then
     hive -e "use jfz_rawdata; alter table jfz_rawdata.${table_name%%.*} drop partition (dt=$date_10d_ago)" 
  fi
done
cd ..
rm -rf $date_10d_ago 
echo "##############time_end:"`date -d "0 day ago" "+%Y-%m-%d %H:%M:%S"`"#######################"
exit

