##########################################################
## 功能：从hive按时间区间导数据到mysql
## 用法：./load_all.sh tablename yyyymmdd   导数据到mysql
##########################################################

if [ $# == 2 ]
then
    table_name=$1
    date_curr=$2
    date_end=$2
    mysql_comm="mysql -h192.168.20.89 -ujfz_data -pjfzData!1 -Djfz_result --default-character-set=utf8"
elif [ $# == 3 ]
then
    table_name=$1
    date_curr=$2
    date_end=$3
    mysql_comm="mysql -h192.168.20.89 -ujfz_data -pjfzData!1 -Djfz_result --default-character-set=utf8"
else
	echo "Usage: $0 tablename yyyymmdd or $0 tablename yyyymmdd yyyymmdd"
	exit
fi


dir="/var/data"


hive -e "
select * from jfz_result.${table_name} where dt >= ${date_curr} and dt<= ${date_end}
" > ${dir}/${table_name}.txt.${date_curr}

cnt=`wc -l ${dir}/${table_name}.txt.${date_curr} | awk -F" " '{print $1 }' `
if [ $cnt -le 0 ]
then
    exit
fi

echo "
delete from $table_name where stat_date between $date_curr and $date_end;
" | $mysql_comm

echo "
load data local infile '${dir}/${table_name}.txt.${date_curr}' into table $table_name character set utf8 FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'
" | $mysql_comm

rm "${dir}/${table_name}.txt.${date_curr}"
