from gwpy.timeseries import TimeSeries
from glue import datafind
from numpy import diff
import sys
from optparse import OptionParser

parser = OptionParser(
    version = " ",
    usage = "%prog --start_gps --end_gps --chan_list --output_file --ifo --segments --padding",
    description = "Finds models that have at least one saturation in them.")

parser.add_option("-s","--start-gps",metavar = "start_gps", help = "GPS start time",type="float")

parser.add_option("-e","--end-gps",metavar = "end_gps", help = "GPS end time ",type="float")

parser.add_option("-c","--chan-list",metavar = "chan_list", help = "Channel list",type="string")

parser.add_option("-o","--outfile",metavar = "outfile", help = "Output file",type="string")

parser.add_option("-i","--ifo",metavar = "ifo", help = "IFO",type="string")

parser.add_option("-l","--seg-file",metavar = "seg_file", help = "Segments",type="string")

parser.add_option("-p","--padding",metavar = "padding", help = "Padding",type="float")

args,others = parser.parse_args()

#usage: %prog --gps-start-time --gps-end-time --channel-list 
start_gps = args.start_gps
end_gps = args.end_gps
channel_list = args.chan_list
out_file = args.outfile
ifo = args.ifo
frames = ifo + '1_M'
seg_file = args.seg_file
padding = args.padding



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



