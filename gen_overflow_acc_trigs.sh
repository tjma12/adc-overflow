#!/bin/bash

input=$1
chan_list=$2
ifo=$3
output_directory=$4
segment_list=$5
pad=$6
#echo ${input}

num=`echo $((${input}+1))|bc`

result=`sed -n "${num}p" < ${chan_list}`

#echo $result

python gen_single_channel_acc_trigs.py --channel ${result} --ifo ${ifo} --outdir ${output_directory} --seg-list ${segment_list} --padding ${pad}
