// clear && gcc -Wall -Wextra SurfaceArea.c -lm && ./a.out Map/MostOfRoutes.txt Map/SmallUnionPart.txt && rm ./a.out

#include "SharedFunctions.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {
    if (argc == 1) {
        fprintf(stderr, "Provide the filenames to map routes from the Map folder.\n");
        fprintf(stderr, "Example: ./a.out Map/MostOfRoutes.txt Map/NorthRoute.txt\n");
        fprintf(stderr, "You can put as many files as you want. The result will be outputted to stdout seperated by a new line.\n");
        return EXIT_FAILURE;
    }

    long double * returned = CalculateSurfaceAreas(argc-1, argv+1);
    for (int i = 0; i < argc-1; i++) printf("%0.100LF\n", returned[i]);
    free(returned);
    return EXIT_SUCCESS;
}