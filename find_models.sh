#!/bin/bash

find /home/tjmassin/svn/cds_user_apps/trunk/*/h1/models/ -maxdepth 2 | grep '.mdl' > /home/tjmassin/adc_overflow_condor/h1_model_temp.txt

while read line
do
	base=`basename $line`
	if [ "${base}" != "l1lscpsl.mdl" ]
        then
		echo -en `basename $line`'\t'
		if (cat $line | grep -q 'overflow=1')
		then
			echo -en  'cumulative \t'
		else
			echo -en 'not_cumulative \t'
		fi
	fi
	cat $line | grep -Eo 'ndcuid=[0-9]{1,3}'
done < /home/tjmassin/adc_overflow_condor/h1_model_temp.txt > h1_model_info.txt
