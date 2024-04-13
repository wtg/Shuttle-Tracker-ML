#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Since doubles can't store super precise numbers calculations could be off
// Too hard to implement though with pow and sqrt functions
// long int coordToLongInt(char* coord) {
//     char* findDecimal = coord;
//     while (findDecimal[0] != '.') findDecimal++;
//     int multiplyBy10ToPowerOf = 0;
//     while (findDecimal[0] != '\0') {
//         *findDecimal = *(findDecimal+1);
//         findDecimal++;
//         multiplyBy10ToPowerOf++;
//     }
//     //ensure value is multipled by 10^7 to make it fit as an int
//     while (multiplyBy10ToPowerOf < 8) {
//         findDecimal[-1] = '0';
//         findDecimal[0] = '\0';
//         findDecimal++;
//         multiplyBy10ToPowerOf++;
//     }
//     return atoi(coord);
// }

void getCoordsFromLine(char* line, long double toStore[]) {
    int curVal = 0;
    char* lastComma = line;
    int charsWentThrough = 0;
    while (curVal != 2) {
        if (lastComma[charsWentThrough] == ',' || lastComma[charsWentThrough] == '\n') {
            char temp[100];
            strncpy(temp, lastComma, charsWentThrough);
            temp[charsWentThrough] = '\0';
            toStore[curVal] = atof(temp);

            curVal++;
            lastComma = lastComma+charsWentThrough+1;
            charsWentThrough = 0;
        } else {
            charsWentThrough++;
        }
    }
}

long double distanceFromPoints(long double uno[], long double dos[]) {
    return sqrt(pow(uno[0]-dos[0], 2.0) + pow(uno[1]-dos[1], 2.0));
}

long double* CalculateSurfaceAreas(int size, char** filenames) {
    long double* toReturn = malloc(sizeof(long double)*size);
    char line[100];
    for (int i = 0; i < size; i++) {
        FILE *f;
        f = fopen(filenames[i], "r");
        if (f == NULL) {
            fprintf(stderr, "Unable to read file: \"%s\". It may not exist.\n", filenames[i]);
            continue;
        }

        long double totalDistance = 0;
        long double prevLine[2];
        int firstLine = 1;
        while(fgets(line, 100, f)) {
            long double curLine[2];
            getCoordsFromLine(line, curLine);
            if (!firstLine) {
                totalDistance += distanceFromPoints(prevLine, curLine);
            }
            prevLine[0] = curLine[0];
            prevLine[1] = curLine[1];
            firstLine = 0;
        }
        toReturn[i] = totalDistance;
        fclose(f);
    }
    return toReturn;
}