Here are descriptions for what each of the files do:

balloonthreshold.py:
  This is a python script that checks whether the balloon was close to ARA5 or not. Here are the steps on what it does:
    1) It takes in a balloon file and reads through it to get all the latitudes, longitudes, altitudes, and times
    2) Converts times into unix time
    3) Converts the latitudes and longitudes into distances, and gives you an array of distances
    4) It also makes different plots comparing the values if you choose to make them
    5) From the distances, you calculate the times it was close to ARA5 based on the threshold you set
    6) The function then returns this array of threshold times
    
findruns.py:
  This is a python script that finds the different runs where the balloon was close to ARA5. Here are the steps on what it does:
    1) It takes in a bunch of balloon tsv files
    2) For each balloon file, the balloonthreshold function is used to calculate the threshold times
    3) Then all the runs are looped over
    4) If the threshold time is between two run times, the run is then saved into an array
    5) This is repeatedly done until all runs have been looped over for each balloon file
    6) The function outputs the run numbers that were collected
