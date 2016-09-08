export LANG=zh_CN.UTF-8
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
    date_curr1=`date -d "1 day ago" "+%Y-%m-%d"`
elif [ $# == 1 ]
then
    date_curr=$1
    date_curr1=`date -d "$1" "+%Y-%m-%d"`

else
        echo "Usage $0 or $0 date_curr date_dt"
        exit
fi

#date_curr=20160124
#date_curr1=2016-01-24
dir="/var/sem/report/$date_curr1"
echo $dir
cd $dir
for table_name in `ls *.txt`
do
  table=${table_name%%.*}
  table=${table/-/_}
  table=${table/@/_}
  table=${table/./_}
  table=${table/类/}
  echo $table 
  echo $table_name 
  sed -i '1d' $table_name
  hive -e "load data local inpath '$table_name' overwrite into table jfz_rawdata.$table partition (dt=$date_curr)"
done
date_10d_ago=`date -d "10 day ago" "+%Y-%m-%d"`
cd ..
rm -rf $date_10d_ago 
echo "##############time_end:"`date -d "0 day ago" "+%Y-%m-%d %H:%M:%S"`"#######################"
exit

