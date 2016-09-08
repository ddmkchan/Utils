#!/bin/bash

tableName=$1
database=$2
dataPath=$3

head -1 ${dataPath}/${tableName}.txt > ${dataPath}/${tableName}.tableInfo
