#!/bin/bash

function check() {
  errorCode=$1
  commandName=$2
  file=$3
  line=$4
  if [ ${errorCode} -ne 0 ]; then
    echo ERROR at [${file}:line ${BASH_LINENO}] : [${commandName}] executed with error code:[${errorCode}]
    exit 1
  fi
}

function getTableInfo() {
  tableName=$1
  hiveDatabase=$2
  exceptedInfo=`hive -e "desc ${hiveDatabase}.${tableName}" | awk '{ print $1 }' | sed "s/^dt$/@@/g" | sed ':a;N;$!ba;s/\n/\t/g' | awk -F "\t@@" '{print $1}'`
  echo $exceptedInfo
}

function checkTableInfo() {
  tableName=$1
  hiveDatabase=$2
  txtPath=$3

  echo '----------------- check table :' ${tableName} 'start -------------------'

  actualInfo=$(head -1 ${txtPath}/${tableName}.tableInfo | tr '[A-Z]' '[a-z]')

  if [ "${actualInfo}" == "" ]; then
    echo "*************** [WARNING] Empty txt file [Table:" ${tableName} "] ***************"
    return 3
  fi

  databaseLower=$(echo ${hiveDatabase} | tr '[A-Z]' '[a-z]')
  tableNameLower=$(echo ${tableName} | tr '[A-Z]' '[a-z]')

  if [ ! -f "/var/rep/skd/table_info/${databaseLower}.${tableNameLower}.info" ]; then
          echo "*************** [WARNING] New added table, table not exists [Table:" ${tableNameLower} "] ***************"
          return 1
  fi

  exceptedInfo=$(head -1 /var/rep/skd/table_info/${databaseLower}.${tableNameLower}.info | tr '[A-Z]' '[a-z]')

  echo $actualInfo
  echo $exceptedInfo

  isOracle ${actualInfo}
  ret=$?
  if [ ${ret} -eq 0 ]; then
    echo "*************** [WARNING] Oracle SQL [Table:" ${tableNameLower} "] ***************"
    return 0
  fi

  if [ "${actualInfo}" == "${exceptedInfo}" ]; then
    echo '----------------- check table :' ${tableNameLower} 'end, nodiff -------------------'
    return 0;
  fi
  echo '*************** [ERROR] No expected change [Table:' ${tableNameLower} '] ***************'
  return 2;
}


function updateTableInfo() {
  database=$1
  target=$2

  hive -e "use ${database}; show tables;" > ${target}/table.list

  cat ${target}/table.list | while read line
  do
	 hive -e "desc ${database}.${line}" | awk '{ print $1 }' | sed "s/^dt$/@@/g" | sed ':a;N;$!ba;s/\n/\t/g' | awk -F "\t@@" '{print $1}' > ${target}/${database}.${line}.info
  done
}

function isOracle() {
  input=$1
  if [[ "$input" =~ "sql>" ]];then
    return 0
  else
    return 1
  fi
}

#diffTableInfo user_src /data/rawdata/20150924 jfz_rawdata
#updateTableInfo jfz_rawdata /var/rep/shell/table_info

#  isOracle "SQL>"
#  ret=$?
#  echo $ret
#  if [ ${ret} -eq 0 ]; then
#    echo "*************** [WARNING] Oracle SQL ***************"
#  fi

