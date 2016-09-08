#!/bin/bash

file='/var/rep/skd/azkaban_session_id'
current=`date +%s`
lastModified=`stat -c "%Y" $file`
echo "current session id is: `cat $file`"

if [ $((${current} - ${lastModified})) -gt $((60 * 60 * 12)) ] || [ "$1" = "force" ]; then
	echo "session id too old, update";
	responseJson=`curl -k -X POST --data "action=login&username=azkaban&password=AzkabanCdp1" https://localhost:8443`
	echo ${responseJson} | jq '."session.id"' | sed 's/"//g' > ${file}
        echo "updated session id is: `cat $file`"
else
	echo "session id is new enough";
fi


