#!/bin/bash

input=$1
start_time=$2
end_time=$3
chan_list=$4
ifo=$5
model_info=$6

#echo ${input}

num=`echo $((${input}+1))|bc`

result=`sed -n "${num}p" < ${chan_list}`

#echo $result

python gen_single_channel_trigs.py --gps-start-time ${start_time} --gps-end-time ${end_time} --channel ${result} --ifo ${ifo} --model-info ${model_info}
