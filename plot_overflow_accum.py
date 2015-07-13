from gwpy.timeseries import TimeSeries
from glue import datafind
from numpy import diff
import sys


#usage: %prog --gps-start-time --gps-end-time --channel-list 
start_gps = float(sys.argv[1])
end_gps = float(sys.argv[2])
ifo = 'H'
frames = 'H1_M'
channel_list = str(sys.argv[3])
out_file = str(sys.argv[4])

fP = open(out_file,'w')

chan_list = []
chan_read = open(channel_list)
for line in chan_read.readlines():
    chan_list.append(line)



connection = datafind.GWDataFindHTTPConnection()
cache = connection.find_frame_urls(ifo, frames, start_gps, end_gps, urltype='file')

for chan in chan_list:

    chan1 = chan[:-1]
    data1=TimeSeries.read(cache, chan1, start=start_gps, end=end_gps)

    if any(diff(data1)>0):
        print >> fP, chan1


fP.close()



