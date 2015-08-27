#!/usr/bin/python
from dqsegdb import apicalls
from glue import segments as seg

def find_segments(ifo,start_time,length,DQFlag):
    # example: ifo='H1',DQFlag='DMT-ANALYSIS_READY'
    seg_dict=apicalls.dqsegdbQueryTimes('https','dqsegdb5.phy.syr.edu',ifo,DQFlag,'1','active,known,metadata',start_time,start_time+length)
    return seg_dict

def coalesce_result_dictionary(result_dict):
    out_result_dict=result_dict
    active_seg_python_list=[seg.segment(i[0],i[1]) for i in result_dict[0]['active']]
    active_seg_list=seg.segmentlist(active_seg_python_list)
    active_seg_list.coalesce()
    out_result_dict[0]['active']=active_seg_list
    known_seg_python_list=[seg.segment(i[0],i[1]) for i in result_dict[0]['known']]
    known_seg_list=seg.segmentlist(known_seg_python_list)
    known_seg_list.coalesce()
    out_result_dict[0]['known']=known_seg_list
    return out_result_dict

def get_active_segments(ifo,start_time,length,DQFlag):
    segs=find_segments(ifo,start_time,length,DQFlag)
    coal_segs=coalesce_result_dictionary(segs)
    return coal_segs[0]['active']

def get_segment_dict(ifo,start_time,length,DQFlag):
    segs=find_segments(ifo,start_time,length,DQFlag)
    coal_segs=coalesce_result_dictionary(segs)
    return coal_segs
