import nuphase_data_reader
from balloonthreshold import BalloonThreshold
import os
from os import path

#Grab list of all TSV files:
TSV_files = []
mydir = "../SouthPole_Radiosonde/data/2018"
for root, dirs, files in os.walk(mydir):
    for filename in files:
        print(filename)
        TSV_files.append(mydir+filename)

TSV_files = sorted(TSV_files)
print(TSV_files)

runnumbers = []

first_run = 500 #change this as you find balloons so that you don't have to keep starting over at run 500

for bfile in TSV_files:
    #grab times from this balloon
    thresholdtimes = BalloonThreshold(bfile)
    print('')
    print('')
    print('new balloon file: ', bfile)

    for PA_run in range(first_run,4103): #loop over runs

        try:
            d = nuphase_data_reader.Reader("/project2/avieregg/nuphase/telem/root",PA_run)

            #print(d.N())

            #grab first and last time in run:
            d.setEntry(0)
            h = d.header()
            readout_time_i = h.readout_time[0]
        
            d.setEntry(d.N()-1)
            h = d.header()
            readout_time_f = h.readout_time[0]
            #print(readout_time_i)
            #print(readout_time_f)
            print(PA_run, thresholdtimes[0]-readout_time_i)
            #if threshold is between the two run times, save run and exit for loop
            if readout_time_i < thresholdtimes[0] < readout_time_f:
                print('success!',PA_run)
                runnumbers.append(PA_run)
                first_run = runnumbers[-1] #set beginning of loop to = current run. This works because the runs are in consecutive order and so are the balloons.

                break
            #if balloon time is before current run, assume that the phased array was not on and continue to new balloon file
            elif thresholdtimes[0]<readout_time_i:

                print('Phased Array likely not on during this balloon run. Continue')
                first_run = PA_run
                #PA_run=4103
                break
        #move on to next run if current run doesn't exist
        except:
            print("Run " + str(PA_run) + " doesn't exist. Moving on to the next run.")

print(runnumbers)
