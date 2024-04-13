// clear && gcc -Wall -Wextra MakeIntPoints.c -lm && ./a.out Map/MostOfRoutes.txt Map/SmallUnionPart.txt && rm ./a.out

#include "SharedFunctions.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

FILE* kmlFile;
FILE* txtFile;
int pointNum;

void setupFileVars() {
    pointNum = 0;
    kmlFile = fopen("../Points.kml", "w+");
    txtFile = fopen("../Points.txt", "w+");
    if (kmlFile == NULL || txtFile == NULL) {
        fprintf(stderr, "Unable to write to a file. Either ../Points.kml or ../Points.txt.\n");
        exit(EXIT_FAILURE);
    }
    fprintf(kmlFile, "<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmlns=\"http://www.opengis.net/kml/2.2\"><Document><name>Untitled layer</name>");
}
void writeToFiles(long double points[]) {
    fprintf(txtFile, "%Lf,%Lf\n", points[0], points[1]);
    fprintf(kmlFile, "<Placemark><name>Point %d</name><styleUrl>#icon-1899-0288D1-nodesc</styleUrl><Point><coordinates>%Lf,%Lf,0</coordinates></Point></Placemark>", pointNum, points[0], points[1]);
    pointNum++;
}

int getUserInputNumPoints() {
    int numPoints;
    fprintf(stdout, "How many points on the map do you want? ");
    scanf("%d", &numPoints);
    if (numPoints <= 0) {
        fprintf(stderr, "Invalid Number of points typed in.\n");
        exit(EXIT_FAILURE);
    }
    return numPoints;
}

void removeNewLines(char line[]) {
    for (int i = strlen(line)-1; i >= 0; i--) {
        if (line[i] == '\n') {
            line[i] = '\0';
            break;
        }
    }
}

void assignPoints(char* filename, long double distanceBetween) {
    FILE *f;
    f = fopen(filename, "r");
    if (f == NULL) {
        fprintf(stderr, "Unable to read file: \"%s\". It may not exist.\n", filename);
        return;
    }


    long double prevLine[2];
    int firstLine = 1;
    char line[100];
    long double distanceRemaining = distanceBetween;
    while(fgets(line, 100, f)) {
        removeNewLines(line);

        long double curLine[2];
        getCoordsFromLine(line, curLine);
        if (!firstLine) {
            while (distanceRemaining - distanceFromPoints(prevLine, curLine) < 0.0000001) {
                long double xDif = (curLine[0] - prevLine[0]) ? curLine[0] - prevLine[0] : 0.000001;
                long double angle = fabs(atan((curLine[1]-prevLine[1])/xDif));
                angle = fmod(angle, (3.1415 / 2.0));
                // printf("%Lf\n", ((angle*180)/3.1415));

                if (prevLine[1] < curLine[1]) prevLine[1] += (sin(angle)*distanceRemaining);
                else prevLine[1] -= (sin(angle)*distanceRemaining);

                if (prevLine[0] < curLine[0]) prevLine[0] += (cos(angle)*distanceRemaining);
                else prevLine[0] -= (cos(angle)*distanceRemaining);


                distanceRemaining = distanceBetween;
                writeToFiles(prevLine);
                printf("%Lf %Lf; %Lf %Lf; %Lf %Lf %Lf\n", prevLine[0], prevLine[1], curLine[0], curLine[1], distanceRemaining, distanceFromPoints(prevLine, curLine), angle);
            }
            distanceRemaining -= distanceFromPoints(prevLine, curLine);
        }
        prevLine[0] = curLine[0];
        prevLine[1] = curLine[1];
        firstLine = 0;
    }

    fclose(f);
}

int main(int argc, char* argv[]) {
    if (argc == 1) {
        fprintf(stderr, "Provide the filenames to map routes from the Map folder.\n");
        fprintf(stderr, "Example: ./a.out Map/MostOfRoutes.txt Map/NorthRoute.txt\n");
        fprintf(stderr, "You can put as many files as you want.\n");
        return EXIT_FAILURE;
    }
    long double totalDistance = 0;
    long double * returned = CalculateSurfaceAreas(argc-1, argv+1);

    for (int i = 0; i < argc-1; i++) totalDistance += returned[i];

    int numPoints = getUserInputNumPoints();

    setupFileVars();

    long double distanceBetween = totalDistance / numPoints;
    for (int i = 1; i < argc; i++) assignPoints(argv[i], distanceBetween);

    fprintf(kmlFile, "</Document></kml>");
    fclose(kmlFile);
    fclose(txtFile);
    free(returned);
    return EXIT_SUCCESS;
}