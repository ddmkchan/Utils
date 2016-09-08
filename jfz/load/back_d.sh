## 日任务回滚

cd "/var/rep/shell"

if [ $# != 2 ]
then
	echo "Usage: $0 date_begin date_end"
	exit
else
	date_begin=$1
	date_end=$2
fi

while [ $date_begin -le $date_end ]
do
	date_time=`date "+%Y-%m-%d %H:%M:%S"`
	echo "[ "$date_time" ]" $date_begin  begin
        cd ../load
        sh semtohive1.sh $date_begin
	date_begin=`date -d "$date_begin 1 day" "+%Y%m%d"`

done

