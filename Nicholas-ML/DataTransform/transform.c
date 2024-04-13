// clear && gcc -Wall -Wextra transform.c -lm && ./a.out DataOriginal.csv Output.csv && rm ./a.out

#include "../CoordsAsInt/SharedFunctions.c" //For getting doubles from line of file
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

FILE* Data_Original;
FILE* Data_Output;

FILE* Int_Points_File;
int Int_Points_File_Line_Count;
long double** Int_Points_File_Contents;

int changeCoords = 1;
int changeDate = 1;

int argumentErrorChecking(int argc) {
    if (argc < 3) {
        fprintf(stderr, "You need two arguments, the original data csv file, and the output data csv file\n");
        fprintf(stderr, "./a.out <Orginal Data File> <Output Data File>\n");
        return 1;
    }
    return 0;
}
int setupFiles(char* argv[]) {
    Data_Original = fopen(argv[1], "r");
    Data_Output = fopen(argv[2], "w");
    Int_Points_File = fopen("../Points.txt", "r");
    if (Data_Original == NULL) {
        fprintf(stderr, "Unable to read the original datafile: \"%s\". Check for typos.\n", argv[1]);
        return 1;
    }
    if (Data_Output == NULL) {
        fprintf(stderr, "Unable to write to the output datafile: \"%s\". Check for permissions.\n", argv[2]);
        return 1;
    }
    if (Int_Points_File == NULL) {
        fprintf(stderr, "Unable to read the Int Coodinates file: \"../Points.txt\". Make sure to run \"MakeIntPoints.c\" in the \"CoordsAsInt\" folder first.\n");
        return 1;
    }
    return 0;
}
void closeFiles() {
    fclose(Data_Original);
    fclose(Data_Output);
    fclose(Int_Points_File);
}

// This function was adapted from the following link:
// https://stackoverflow.com/questions/12733105/c-function-that-counts-lines-in-file
int count_lines()
{
    FILE* file = fopen("../Points.txt", "r");
    if (file == NULL) return -1;
    char buf[65536];
    int counter = 0;
    for(;;)
    {
        size_t res = fread(buf, 1, 65536, file);
        if (ferror(file))
            return -1;

        size_t i;
        for(i = 0; i < res; i++)
            if (buf[i] == '\n')
                counter++;

        if (feof(file))
            break;
    }
    fclose(file);
    return counter;
}
int setupIntFileContents() {
    char line[1000];

    Int_Points_File_Line_Count = count_lines();
    if (Int_Points_File_Line_Count == -1) {
        fprintf(stderr, "Somthing went wrong when getting the line number count from \"../Points.txt\".\n");
        return 1;
    }

    Int_Points_File_Contents = malloc(sizeof(long double*)*Int_Points_File_Line_Count);
    if (Int_Points_File_Contents == NULL) {
        fprintf(stderr, "Malloc failed. Not enough memory?\n");
        return 1;
    }
    for (int i = 0; i < Int_Points_File_Line_Count; i++) {
        Int_Points_File_Contents[i] = malloc(sizeof(long double)*2);
        if (Int_Points_File_Contents[i] == NULL) {
            fprintf(stderr, "Malloc failed. Not enough memory?\n");
            return 1;
        }
        Int_Points_File_Contents[i][0] = 0;
        Int_Points_File_Contents[i][1] = 0;

        if (feof(Int_Points_File)) {
            fprintf(stderr, "The Line Count returned a value that's too high.\n");
            continue;
        }
        if (fgets(line, 1000, Int_Points_File) == NULL) {
            fprintf(stderr, "Failed to read line %d from file \"../Points.txt\".\n", i);
            continue;
        }

        getCoordsFromLine(line, Int_Points_File_Contents[i]);
        // printf("%Lf %Lf\n", Int_Points_File_Contents[i][0], Int_Points_File_Contents[i][1]);
    }

    return 0;
}
void freeIntFileContents() {
    for (int i = 0; i < Int_Points_File_Line_Count; i++) {
        free(Int_Points_File_Contents[i]);
    }
    free(Int_Points_File_Contents);
}

// Exact function can be found here:
// https://stackoverflow.com/questions/6054016/c-program-to-find-day-of-week-given-date
int get_weekday(char * str) {
  struct tm tm;
  memset((void *) &tm, 0, sizeof(tm));
  if (strptime(str, "%d-%m-%Y", &tm) != 0) {
    time_t t = mktime(&tm);
    if (t >= 0) {
      return localtime(&t)->tm_wday; // Sunday=0, Monday=1, etc.
    }
  }
  fprintf(stderr, "ERROR: %s wasn't a valid dd-mm-yyyy date\n", str);
  return -1;
}
// dayOfWeek = 0 Monday, = 1 Tuesday, = 2 Wednesday
// timeInSeconds = seconds since 0 o'clock (not including date)
// returns seconds since Jan 1 1990
int getDayOfWeekAndTime(char* timeStr, int* dayOfWeek, int* timeInSeconds) {
    char* DDMMYYYY = calloc(sizeof(char), 15);
    // Help from: https://stackoverflow.com/questions/47640056/get-epoch-seconds-for-specific-date-in-c
    struct tm t;
    int milisecond;
    sscanf(timeStr, "%d-%d-%d %d:%d:%d +%d", &t.tm_year, &t.tm_mon, &t.tm_mday, &t.tm_hour, &t.tm_min, &t.tm_sec, &milisecond);
    sprintf(DDMMYYYY, "%d-%d-%d", t.tm_mday, t.tm_mon, t.tm_year);
    if (dayOfWeek != NULL) *dayOfWeek = get_weekday(DDMMYYYY);
    free(DDMMYYYY);
    if (timeInSeconds != NULL) *timeInSeconds = t.tm_hour*3600+t.tm_min*60+t.tm_sec+(milisecond > 5000);

    t.tm_year -= 1900;
    t.tm_mon--;
    t.tm_wday = 0;
    t.tm_yday = 0;
    t.tm_isdst = 0;
    return mktime(&t);
}

void exportCoords(long double cur[]) {
    if (changeCoords == 0) {
        fprintf(Data_Output, "%Lf,%Lf", cur[0], cur[1]);
    } else {
        //brute force method to get closest point. VERY SLOW. but reliable !!!!!!!!!!!!!!!! Make faster if needed
        //NEED BETTER ALGORITHM IF YOU HAVE TIME
        int closestPoint = 0;
        long double closestDistance = distanceFromPoints(Int_Points_File_Contents[0], cur);
        for (int i = 1; i < Int_Points_File_Line_Count; i++) {
            if (distanceFromPoints(Int_Points_File_Contents[i], cur) < closestDistance) {
                closestPoint = i;
                closestDistance = distanceFromPoints(Int_Points_File_Contents[i], cur);
            }
        }
        fprintf(Data_Output, "%d", closestPoint);
    }
}
void exportTime(char* timeStr) {
    int dayOfWeek = 0;
    int timeInSeconds = 0;
    int timeSince1990 = getDayOfWeekAndTime(timeStr, &dayOfWeek, &timeInSeconds);
    if (changeDate == 0) {
        fprintf(Data_Output, ",%d", timeSince1990);
    } else {
        fprintf(Data_Output, ",%d,%d", dayOfWeek, timeInSeconds);
    }
}
void readAndMakeCSV() {
    char line[1000];

    int prev_busNum = 0;
    long double prev_cord[2];
    char* prev_date = NULL;
    char* prev_busType = NULL;

    while (fgets(line, 1000, Data_Original)) {
        int busNum = 0;
        long double cord[2];
        char* date = calloc(sizeof(char), 100);
        char* busType = calloc(sizeof(char), 100);
        sscanf(line, "%d,%Lf,%Lf,%[^,],%[^\n]", &busNum, cord+1, cord, date, busType);
        // printf("%d,%Lf,%Lf,%s,%s\n", busNum, *(cord+1), *cord, date, busType);
        if (prev_date != NULL) {
            //busNum,Coords,Time,BusType,DeltaTime,FinalPosition
            if (prev_busNum == busNum) {
                // fprintf(Data_Output, "%d,", prev_busNum);    //busNum
                exportCoords(prev_cord);    //Coords
                exportTime(prev_date);      //Time
                // fprintf(Data_Output, ",%s", prev_busType);   //BusType
                fprintf(Data_Output, ",%d,", getDayOfWeekAndTime(date,0,0)-getDayOfWeekAndTime(prev_date,0,0)); //DeltaTime (in secs)
                exportCoords(cord); //FinalPosition
                fprintf(Data_Output, "\n");
            }
            free(prev_date);
            free(prev_busType);
        }

        prev_busNum = busNum;
        prev_cord[0] = cord[0];
        prev_cord[1] = cord[1];
        prev_date = date;
        prev_busType = busType;
    }
    free(prev_date);
    free(prev_busType);
}

int main(int argc, char* argv[]) {
    if (argumentErrorChecking(argc)) return EXIT_FAILURE;
    if (setupFiles(argv)) return EXIT_FAILURE;
    if (setupIntFileContents()) return EXIT_FAILURE;
    
    printf("Display time as seconds since Jan 1 1990 (0) or as int for day of week and time (hh-mm-ss) in seconds (1)? ");
    scanf("%d", &changeDate);

    printf("Display Coorindates as Coordinates (0) or as my fancy Int system (1)? ");
    scanf("%d", &changeCoords);

    readAndMakeCSV();

    freeIntFileContents();
    closeFiles();
    return EXIT_SUCCESS;
}