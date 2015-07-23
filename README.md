# adc-overflow
This code base is used to search for ADC/DAC overflows in LIGO instruments.
Developed by TJ Massinger for use in the LVC.

The purpose of this code is to generate an appropriate set of condor dag and sub files to search for ADC/DAC overflows and generate sngl_burst XML files containing triggers. The generated DAG will call the executable <b>gen_overflow_acc_trigs.sh</b>, which is a wrapper around the python script <b>gen_single_channel_acc_trigs.py</b>.

<i>*** This code does not currently perform a segment database query due to the fact that the average user doesn't have a robot cert to perform segment database query from a Condor process. The user must instead run a segment database query and provide the results as an argument to the program. ***</i>


Instructions for running on an LDAS cluster:

#### 1. Source GWpy user environment

source /home/detchar/opt/gwpysoft/etc/gwpy-user-env.sh

#### 2. Run a segment database query to generate science segments for this time

Results of the segment database query should be piped through ligolw_print and stored in a whitespace delimited text file.

Example call:

```
ligolw_segment_query_dqsegdb --segment-url https://dqsegdb5.phy.syr.edu --query-segments --include-segments H1:DMT-DC_READOUT_LOCKED --gps-start-time 1117742416 --gps-end-time 1117747816 | ligolw_print -t segment -c start_time -c end_time -d ' ' > segment_list.txt
```

The resulting segment_list.txt should look like:

```
1117742416 1117743020
1117745521 1117747816
```

#### 3. Run gen_overflows_condor.sh 

This script will go through the entire process of generating an appropriate condor DAG that should be submit-ready. It will generate a directory structure containing log files and executables in the designated output directory.

Syntax:

```
 ./gen_overflows_condor.sh {start_gps} {end_gps} {L,H} {build directory} {trigger directory} {segment list}
```

Example call:

```
./gen_overflows_acc_condor.sh 1117742416 1117747816 H /home/tjmassin/git_repos/adc-overflow/dev/acc/ /home/tjmassin/temp_triggers/ segment_list.txt
```

The process is as follows:

a. Set up a directory structure to store all information regarding models and overflow channels, as well as condor dag, sub, and log files.
The location of this structure is specified by the {build directory} argument

b. Grab model-wide cumulative overflow channels to see if any channel in a given model has overflowed during the time period of interest. This is done using <b>plot_overflow_accum.py</b>.

c. Generate a list of models that have at least one overflow.

d. Generate a list of channels contained in those overflowing models and mark them for further follow-up.

e. Generate condor DAG and sub files that allow the search code to farm the computation out channel-by-channel.

f. Copy over the search executables to the condor run directory and create log file directory.

#### 4. Submit the DAG generated by the previous step

Example: 

```
condor_submit_dag ADC_1115717416_1115740270.dag
```

Logging information will be stored in the directory "log_{start_gps}_ADC"




