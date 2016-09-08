#!/bin/bash

source /var/rep/skd/common.sh

tableName=$1
database=$2
dataPath=$3

checkTableInfo ${tableName} ${database} ${dataPath}
