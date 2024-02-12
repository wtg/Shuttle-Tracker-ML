# Coordinates to Int

Coordinates are represented as two floating point numbers. Obviously no new ground was broken, but when doing machine learning that's two inputs. Considering we know the exact route the buses are taken well in advance we can simplify this.<br><br>
The goal of this folder is to convert the coordinates from two inputs to one. To achieve this we need to map both bus routes as a simple integer value that will represent a specific point on the route. So the number 1 may represent a coordinate (0,0) and a number 20 may represent (10, 20) and so on.<br><br>
The final result of this folder is PointsOutput.txt and PointsOutput.kml. The txt file has all coordinates represented as one input that are represented by the ints. PointsOutput.kml is a way to visually see the integer values and their coordinates on a map.

## Coordinates/map.kml

A file that you can import to Google MyMaps which has the routes of the shuttle bus in many different formats. This file was exported from Google MyMaps and was used to obtain all relevent points that, when connected, make up the shuttle route automatically.

## Coordinates/HorseshoeCoordinates.txt

This file contains the points that, when connected, make up a route of the circluar horshoe in front of the Union.

## Coordinates/NorthCoordinates.txt

This file contains the points that, when connected, make up a route of exclusivly for the North shuttle route.

## Coordinates/WestCoordinates.txt

This file contains the points that, when connected, make up a route of exclusivly for the West shuttle route.

## Coordinates/AlmostWholeRoute.txt

This file contains the points that, when connected, make up a route 99% of the route except for a small line in front of the Union.

## Coordinates/SmallLipOnHorseshoe.txt

This file contains the points that, when connected, make up a route 1% of the route being only the small line in front of the Union.

## SurfaceArea.py

A file that when run will calcuate the surface area of the txt files put into the command line arguments. What's printed is the surface area of all the files that were command line arguments seperated by spaces.<br><br>

Input:
```bash
python SurfaceArea.py NorthCoordinates.txt WestCoordinates.txt HorseshoeCoordinates.txt
```
Output:
```bash
0.03260636446177257 0.03903442612718046 0.0011650168076891702
```

## PointsOnRouteMaker.py

When run, this file will make the goal of this entire directory relevent. It calls SurfaceArea.py to get the total distance of all the files put into the command line (follows same command line argument logic as SurfaceArea.py). It then asks the amount of points you want evenly distributed along all routes (Due to floating point inaccuracy the number is more of a suggestion than a hard cap). It'll then calucate the distance per point and make two files to represent the output.<br><br>

Input:
```bash
python PointsOnRouteMaker.py NorthCoordinates.txt WestCoordinates.txt HorseshoeCoordinates.txt
```

Output:
    PointsOutput.txt contains all points along the route with the line number subtracted by 1 being the one input the machine learning will get, and the contents of the line being the coordinate that point represents. <br>
    PointsOutput.kml contains all the points numbered by their one int that the machine learning will get an input, along with where it is on tthe map. This is importable into Google MyMaps to see the results.

## PointsOutput.txt

Made by running PointsOnRouteMaker.py. Read more about it above. Contains all points along the route with the line number subtracted by 1 being the one input the machine learning will get, and the contents of the line being the coordinate that point represents.

## PointsOutput.kml

Made by running PointsOnRouteMaker.py. Read more about it above. Contains all the points numbered by their one int that the machine learning will get an input, along with where it is on tthe map. This is importable into Google MyMaps to see the results.