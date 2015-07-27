from gwpy.timeseries import TimeSeries
from glue import datafind
from numpy import diff
import sys


#usage: %prog --gps-start-time --gps-end-time --channel-list 
start_gps = float(sys.argv[1])
end_gps = float(sys.argv[2])
channel_list = str(sys.argv[3])
out_file = str(sys.argv[4])
ifo = str(sys.argv[5])
frames = ifo + '1_M'
seg_file = str(sys.argv[6])
padding = float(sys.argv[7])



fP = open(out_file,'w')

chan_list = []
chan_read = open(channel_list)
for line in chan_read.readlines():
    chan_list.append(line)

seg_list = []
seg_read = open(seg_file)
for line in seg_read.readlines():
    seg_list.append(map(int,line.split()))


connection = datafind.GWDataFindHTTPConnection()
cache = connection.find_frame_urls(ifo, frames, start_gps, end_gps, urltype='file')

for chan in chan_list:
    chan1 = chan[:-1]
    for seg in seg_list:
        if (seg[1] - seg[0] > padding):
            data1=TimeSeries.read(cache, chan1, start=seg[0], end=(seg[1] - padding))
            if any(diff(data1.value)>0):
                print >> fP, chan1
                break


fP.close()



