import nuphase_data_reader
from balloonthreshold import BalloonThreshold

filepath = #Enter file path here
thresholdtimes = BalloonThreshold(filepath)
print(thresholdtimes)

runnumbers = []

for x in range(500,4103):
    PA_run = x
    try:
        d = nuphase_data_reader.Reader("/project2/avieregg/nuphase/telem/root",PA_run)

        #print(d.N())

        d.setEntry(0)
        h = d.header()
        readout_time_i = h.readout_time[0]
    
        d.setEntry(d.N()-1)
        h = d.header()
        readout_time_f = h.readout_time[0]
        #print(readout_time_i)
        #print(readout_time_f)

        if readout_time_i < thresholdtimes[0] < readout_time_f:
            runnumbers.append(x)
        else:
            pass
    except:
        print("Run " + str(x) + " doesn't exist. Moving on to the next run.")

print(runnumbers)
