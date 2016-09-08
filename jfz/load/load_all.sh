##########################################################
## 功能：从hive全表导数据到mysql
## 用法：./load_all.sh tablename   导数据到mysql
##       ./load_all.sh tablename 1 导数据到infobright
##########################################################

if [ $# == 1 ]
then
    table_name=$1
    mysql_comm="mysql -h192.168.20.89 -ujfz_data -pjfzData!1 -Djfz_result --default-character-set=utf8"
elif [ $# == 2 ]
then
    table_name=$1
    mysql_comm="/usr/local/infobright-4.0.7-x86_64/bin/mysql -uroot -Djfz_result --default-character-set=utf8"

    if [ $2 != 1 ]
    then
	    echo "Usage: $0 tablename or $0 tablename 1"
    	exit
    fi
else
	echo "Usage: $0 tablename or $0 tablename 1"
	exit
fi


dir="/var/data"


hive -e "select * from jfz_result.${table_name}" > ${dir}/${table_name}.txt
cnt=`wc -l ${dir}/${table_name}.txt | awk -F" " '{print $1 }' `
if [ $cnt -le 0 ]
then
    exit
fi

echo "
truncate table $table_name
" | $mysql_comm


echo "
load data local infile '${dir}/${table_name}.txt' into table $table_name character set utf8 FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';
" | $mysql_comm

rm "${dir}/${table_name}.txt"
