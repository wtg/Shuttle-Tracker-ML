# Data

This is for processing and changing the data to prepare for the machine learning. This can include changing the coordinates to my integer system, changing from my integer system to coordinates, and organizing the data and removing useless data points.

## ADataProcessor.py

This takes a csv file with its columns seperated by commas and makes it easier to digest. The time is also converted from a string to integer to aviod possible problems with machine learning.<br><br>

Input:
```bash
python ADataProcessor.py Output.csv output
```
Output:<br>
  - output/AllBusses.txt. A file containing all the buses data from the table. The time is now represented as an int and the field for "user" or "system" is gone.
  - output/BusXXX.txt. A file containing only buses XXX information. It is organized the same as above, but the bus ID isn't inside each row anymore.


# AutoConvertCoords.py

This takes in a csv file and automatically changes the coordiantes to my integer system. ../CoordinatesToIntWork/PointsOutput.txt is a requires file to run.

Input:
```bash
python AutoConvertCoords.py DataOriginal.csv Output.csv
```
Output:
  - Output.csv with the coordiantes from DataOriginal.csv now as my integer system


# ConvertIntsToCoords.py

This takes in a csv file and changes my integer system back to coordiantes. ../CoordinatesToIntWork/PointsOutput.txt is a requires file to run.

Input:
```bash
python ConvertIntsToCoords.py Output.csv Output2.csv
```
Output:
  - Output2.csv with the integer coordiante system from Output.csv now as back as normal coordinates