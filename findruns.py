import os
from os import path
import matplotlib.pyplot as plt
import numpy as np
import nuphase_data_reader
from scipy.fftpack import fft
from BalloonThreshold import BalloonThreshold

def ReturnFFTForPlot(t,v):
    fft = np.fft.fft(v)
    N = len(v)
    freqs = np.fft.fftfreq(len(v),d=t[1]-t[0])
    db = 10.0*np.log10(np.abs(fft[:int(N/2)]/1000)**2/50.0)
    return(freqs[:int(N/2)],db)

mydir = "./data/2018/"

def findrunnumbers(directorypath):
    #Grab list of all TSV files:
    TSV_files = []
    #mydir = "../SouthPole_Radiosonde/data/2018"
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

    return runnumbers

#runnumbers = findrunnumbers(mydir)
#print(runnumbers)
#runnumbers = [518,525,552,619,694,774,914,1153,1264,1376,1487,1730]
runnumbers = [517,518,519]


def plotfunction(runlist):
    all_dbs = defaultdict(list)
    all_freqs = defaultdict(list)
    
    for r in runlist:
        d = nuphase_data_reader.Reader("/project2/avieregg/nuphase/telem/root",r)
        d.setEntry(0)
        #all_dbs[j].append(np.max(db))
        startevent = 500
        endevent = d.N()
        numofevents = endevent-startevent
        for i in range(0,numofevents):
            d.setEntry(i)
            h = d.header()
            readout_time = h.readout_time[0]
            for j in [0,1,2,3,4,6,7]:
                t = d.t()
                wf = d.wf(j)
                freqs,db = ReturnFFTForPlot(t,wf)
                freqs=freqs[1:]
                db=db[1:]
                all_dbs[j].append(np.max(dbs))
                all_freqs[j].append(freqs[np.argmax(db)])
                #print(all_dbs)
                #print(all_freqs[j])
                #all_dbs.update({j:all_dbs[j]+np.max(db)})
                
                
        plt.figure(1)
        for j in [0,1,2,3,4,6,7]:
            plt.subplot(4,2,j+1)
            print(len(all_dbs[j]))
            plt.scatter(np.linspace(startevent,endevent,numofevents),np.asarray(all_dbs[j]),label='Channel'+str(j))
            plt.xlabel('Run Number')
            plt.ylabel('~dB')
            #plt.ylim([-60.0,-15.0])
            #plt.title('Channel'+str(j)
            plt.legend()
            plt.grid(True)
            
        plt.figure(2)
        for j in [0,1,2,3,4,6,7]:
            plt.subplot(4,2,j+1)
            plt.scatter(np.linspace(startevent,endevent,numofevents), np.asarray(all_freqs[j])*1000,label='Channel'+str(j))
            plt.xlabel('Run Number')
            plt.ylabel('Frequency (MHz)')
            #plt.ylim([-60.0,-15.0])
            #plt.title('Channel'+str(j)
            plt.legend()
            plt.grid(True)
        plt.show()

#plotfunction(runnumbers)

def MakeSpectrogram():
    first_run = runnumbers[0]
    last_run= runnumbers[(len(runnumbers)-1)]
    freq_spacing = 2.9296874999999996 #MHz
    freq_resolution = 1 #four times what it is
    channel = 0#make spectrogram for one channel at a time
    bin_size = 10 #seconds
    #set up run list:
    runlist = np.linspace(first_run,last_run,int(last_run-first_run+1),dtype=int)
    #load data and start/end time:
    d = nuphase_data_reader.Reader("/project2/avieregg/nuphase/telem/root",first_run)
    h = d.header()
    t0 = h.readout_time[0]
    d = nuphase_data_reader.Reader("/project2/avieregg/nuphase/telem/root",last_run)
    d.setEntry(d.N()-1)
    h = d.header()
    tf = h.readout_time[0]
    event_times = []
    freqs, dbs = ReturnFFTForPlot(d.t(),d.wf(0))
    all_dbs = np.zeros([int(len(freqs)/freq_resolution),int((tf-t0)/bin_size)+1])
    all_counters = np.zeros(int((tf-t0)/bin_size)+1)
    for run in runlist:
        print(run)
        if(os.path.exists('/project2/avieregg/nuphase/telem/root/run'+str(run)+'/event.root')):
            d = nuphase_data_reader.Reader("/project2/avieregg/nuphase/telem/root",run)
            #event_list = np.arange(0,d.N(),100,dtype=int)
            for i in range(0,d.N()):
                d.setEntry(i)
                h = d.header()
                ts = h.readout_time[0]
                #get FFT 
                freqs, new_dbs = ReturnFFTForPlot(d.t(),d.wf(channel))
                #new_dbs = np.zeros(int(len(dbs)/freq_resolution))
                #for d_count in range(0,int(len(dbs)/freq_resolution)):
                #    new_dbs[d_count]=sum(dbs[d_count*freq_resolution:d_count*freq_resolution+freq_resolution])/freq_resolution
                all_dbs[:,int((ts-t0)/bin_size)]=all_dbs[:,int((ts-t0)/bin_size)]+new_dbs
                all_counters[int((ts-t0)/bin_size)]=all_counters[int((ts-t0)/bin_size)]+1
                event_times.append(h.readout_time[0])
    plt.imshow(all_dbs/all_counters,aspect='auto',extent=[0,(tf-t0)/3600.0,freqs[-1]*1000,freqs[0]*1000])
    plt.title(str(run))
    plt.xlabel('Time (hr)')
    plt.ylabel('Frequency (MHz)')
    plt.colorbar()
    plt.show()
    
MakeSpectrogram()
