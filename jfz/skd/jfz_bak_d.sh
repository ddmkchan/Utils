#!/bin/bash
##################脚本备份##############

source /var/rep/skd/common.sh

fileName=`basename $0`
back_path="/var/bak"
if [ ! -d ${back_path} ]; then
  echo ${back_path} "not exists"
  exit 1
fi

cd ${back_path}
date_curr=`date -d "1 day ago" "+%Y%m%d"`
date_7ago=`date -d "7 day ago" "+%Y%m%d"`

echo "----------------------------zip start------------------------------"
zip -q -r ${back_path}/$date_curr.zip /var/rep
check $? 'zip data' ${fileName}
echo "----------------------------zip end------------------------------"

rm -rf $date_7ago.zip 

echo "----------------------------mysqldump start------------------------------"
mysqldump -u root -pMysql1 jfz_result > ${back_path}/jfz_result_$date_curr.sql
check $? 'mysql dump' ${fileName}
echo "----------------------------mysqldump end------------------------------"

echo "----------------------------scp copy data start------------------------------"
scp /var/bak/$date_curr.zip jinfuzi@10.1.2.51:~/azkabanTest/bak/$date_curr.zip
#check $? 'scp shell copy' ${fileName}

scp /var/bak/jfz_result_$date_curr.sql jinfuzi@10.1.2.51:~/azkabanTest/bak/jfz_result_$date_curr.sql
#check $? 'scp sql copy' ${fileName}
echo "----------------------------scp copy data end------------------------------"

echo "-------------------------------success!-------------------------------------"


