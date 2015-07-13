#!/bin/bash
userapps_dir=$1
outdir=$2
ifo=$3

mkdir -p $outdir

if [ ifo = "L1" ]; then
  find $1/trunk/*/l1/models/ -maxdepth 2 | grep '.mdl' > $2/models_temp.txt 
else
  find $1/trunk/*/h1/models/ -maxdepth 2 | grep '.mdl' > $2/models_temp.txt
fi

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
done < $2/models_temp.txt > $2/$3_model_info.txt

rm $2/models_temp.txt
