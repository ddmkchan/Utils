#!/bin/bash


# file config
FILE_LIST="http://getdb.jinfuzi.com/data"
DIST_DIR="/data/rawdata/"
ZIP_SECRET="fghryug4564"
DEBUG=1 #1为开启，0为关闭


LOG_FILE="$DIST_DIR/get_db.log"
# function defined
function retry_times()
{
	echo $*
	times=3	
	while [ $times -gt 0 ]	
	do
		let times--
		`$*`
		if [ $? -eq 0 ]
		then
			return 0
		fi
	done
	return 1
}

function write_info_log()
{
	time=`date +'%Y%m%d %H:%M:%S'`
	echo "$time [info] $1" >> $LOG_FILE
}

function write_debug_log()
{
	if [ $DEBUG -eq 1 ]
	then
		time=`date +'%Y%m%d %H:%M:%S'`
		echo "$time [debug] $1" >> $LOG_FILE
	fi
}

function write_error_log()
{
	time=`date +'%Y%m%d %H:%M:%S'`
	echo "$time [error] $1" >> $LOG_FILE
}

# variable
list_file="list.txt"
yes_date=`date --date='yesterday' +'%Y%m%d'`
if [ ! -d $DIST_DIR ]
then
	mkdir -p $DIST_DIR	
fi
cd $DIST_DIR

rm -rf $yes_date


mkdir $yes_date

cd $yes_date

wget_cmd="wget --no-check-certificate $FILE_LIST/$yes_date/filelist.txt -O $list_file"

retry_times $wget_cmd

if [ $? -eq 0 ]
then
	write_debug_log "get file list success"
else
	write_error_log "get file list failed"
fi


cat $list_file | while read line
do
	url=`echo $line | awk '{print $1}'` 
	md5=`echo $line | awk '{print $2}'` 
	bn=`basename $url`
	wget_cmd="wget --no-check-certificate $url -O $bn"
	retry_times $wget_cmd
	if [ $? -eq 0 ]
	then
		write_debug_log "[$url] wget success"
	else
		write_error_log "[$url] wget failed"
	fi
	echo "$md5  $bn" > md5_tmp
	md5sum -c md5_tmp
	if [ $? -eq 0 ]
	then
		write_debug_log "[$bn] md5 success"
	else
		write_error_log "[$bn] md5 failed"
	fi
	unzip -u -P $ZIP_SECRET $bn
	if [ $? -eq 0 ]
	then
		write_debug_log "[$bn] unzip success"
	else
		write_error_log "[$bn] unzip failed"
	fi
	rm $bn

	tableName=${bn%%.*}
	database="jfz_rawdata"
	localDataPath=${DIST_DIR}/${yes_date}


	sh /var/rep/skd/update_azkaban_session.sh

	session=`head -1 /var/rep/skd/azkaban_session_id`

	sleep 5s

	curl -k --get --data "session.id=${session}" --data "ajax=executeFlow" --data "project=jfz_skd_system" --data "flow=to_hive_single" --data "flowOverride[param.tableName]=${tableName}" --data "flowOverride[param.database]=${database}" --data "flowOverride[param.localDataPath]=${localDataPath}" https://localhost:8443/executor

done 

rm md5_tmp
rm list.txt

write_info_log "Get db success!!!"
