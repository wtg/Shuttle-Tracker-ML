#!/usr/bin/env python
import csv
import datetime

class Datapoint:
     def __init__(self, idnum, latitude, longitude, dtime, source):
         self.ID = int(idnum)
         self.lat = float(latitude)
         self.lon = float(longitude)
         self.dt = datetime.datetime(int(dtime[:4]), int(dtime[5:7]), \
                 int(dtime[8:10]), int(dtime[11:13]), \
                 int(dtime[14:16]), int(dtime[17:19]))
         self.source = source

     def __repr__(self):
         return str(self.ID) + " " +  str(self.lat) + ", " + \
                 str(self.lon) + " " + str(self.dt) + " " + self.source

if __name__ == "__main__":
    file = open("Data.csv")
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(Datapoint(row[0], row[1], row[2], row[3], row[4]))
    trips = []
    currentTrips = {}
    for dPoint in rows:
        cID = dPoint.ID
        if cID not in currentTrips:
            currentTrips[cID] = [dPoint]
        else:
            timeDiff = dPoint.dt - currentTrips[cID][-1].dt
            if int(str(timeDiff).split(":")[-2]) > 15:
                trips.append(currentTrips[cID])
                currentTrips[cID] = [dPoint]
            else:
                currentTrips[cID].append(dPoint)
    for remainder in currentTrips:
        trips.append(currentTrips[remainder])
    print(trips)
