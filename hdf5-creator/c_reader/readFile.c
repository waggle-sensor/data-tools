/*

Sub-setter for the data file written in C. It reads the file and
subsets it for the nodeid by creating a directory and saves the
data for each subsystem in a separate file

Due to the restriction on the number of file buffers that can be opened at a time,
this just writes to subsystems. It is still slow, though faster than using some combination
of grep, awk etc. as this is made for a specific purpose.

The speed is reduced as this program has to still go through the whole data file for each node.
It can probably be made faster by using some file which tells to start reading at a specific line number
and stop reading at a specific line number

Author : Nikhil Garg
Email : nikhil.garg@data61.csiro.au

*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>
#include <time.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include "readFile.h"

#if defined(__GNUC__) && !defined(__INTEL_COMPILER)
static const double NaN = 0.0 / 0.0;
#endif


int main(int argc, char **argv){
    arguments *args;
    int rc;
    int i;
    if (argc < 3){
        printf("Incorrect number of arguments\n");
        usage();
        exit(1);
    }
    args = malloc(sizeof(arguments));

    args->data_file = NULL;
    args->node_names_file = NULL;
    args->subsystem_name_file = NULL;
    args->node_name = NULL;

    i = 1;
    while (i < argc){
        if (argv[i][0] != '-'){
            usage();
        }
        switch (argv[i][1]){
            case 'i':
                i++;
                args->data_file = argv[i];
                i++;
                break;
            case 'f':
                i++;
                args->node_names_file = argv[i];
                i++;
                break;
            case 's':
                i++;
                args->subsystem_name_file = argv[i];
                i++;
                break;
            case 'n':
                i++;
                if (i <= argc){
                    args->node_name = argv[i];
                }
                i++;
                break;
            default:
                usage();
                break;
        }
    }
    rc = readFile(args);
    if (rc != 0){
        printf("Error running readFile function\n");
    }
    free(args);
    return 0;
}


int readFile(arguments* args){
    char *token;
    FILE *fp;
    char *line = NULL;
    char *oldLine = NULL;
    size_t len = 0;
    int rowCount = 0;
    int old_rowCount = 0;
    int colCount = 0;
    ssize_t read;
    clock_t start_t;
    clock_t end_t;
    double time_taken;
    int i, j, old_i;
    int numNodes = 0;
    int nodeId_length = 0;
    int subsys_max_length = 0;
    int numSubsys = 0;
    int* subsys_length;
    int* node_line_count;

    char** nodenames;
    char** subsys_names;
    int** subsys_line_count;
    char* fileout = NULL;
    char node_suffix[7];
    struct stat dir_stats = {0};
    struct stat file_stats = {0};
    FILE** fileHandle = NULL;
    char node_dir_name[12];

//  get the number of nodes in the file and the length of the string
    get_file_info(args->node_names_file, &numNodes, &nodeId_length);
    get_file_info(args->subsystem_name_file, &numSubsys, &subsys_max_length);
//  allocate an integer array to store the number of lines for each node
    node_line_count = malloc(sizeof(int) * numNodes);
    memset(node_line_count, 0, sizeof(int) * numNodes);

//  allocate an character array for the node ids
    nodenames = alloc2d_c(numNodes, nodeId_length);
    subsys_names = alloc2d_c(numSubsys, subsys_max_length);

    subsys_length = malloc(sizeof(int) * numSubsys);
    memset(subsys_length, 0, sizeof(int) * numSubsys);

    subsys_line_count = alloc2d_i(numNodes, numSubsys);

    for (i = 0; i < numNodes; i++){
        for (j = 0; j < numSubsys; j++){
            subsys_line_count[i][j] = 0;
        }
    }
//  open the file again to store the node ids
    fp = fopen(args->node_names_file, "r");
    if (fp == NULL){
        printf("Unable to read file %s\n", args->node_names_file);
        exit(EXIT_FAILURE);
    }

    numNodes = 0;
    while ((read = getline(&line, &len, fp)) != -1){
        strncpy(nodenames[numNodes], line, nodeId_length);
        numNodes++;
    }

    fclose(fp);

//  open the file again to store the node ids
    fp = fopen(args->subsystem_name_file, "r");
    if (fp == NULL){
        printf("Unable to read file %s\n", args->subsystem_name_file);
        exit(EXIT_FAILURE);
    }

    numSubsys = 0;
    while ((read = getline(&line, &len, fp)) != -1){
        subsys_length[numSubsys] = strlen(line)-1;
        strncpy(subsys_names[numSubsys], line, subsys_length[numSubsys]);
        numSubsys++;
    }

    fclose(fp);

    fileout = malloc(sizeof(char));
    if (args->node_name != NULL){
        strncpy(&node_suffix[0], &args->node_name[6], 7);
        strncpy(&node_dir_name[0], "node_", 5);
        strncpy(&node_dir_name[5], node_suffix, 7);

        if (stat(node_dir_name, &dir_stats) != 0 && !S_ISDIR(dir_stats.st_mode))
        {
          printf("Directory node_%s doesnt exist\n", node_suffix);
          if(mkdir(node_dir_name, S_IRUSR | S_IWUSR | S_IXUSR) != 0){
            printf("Unable to make directory %s\n", node_dir_name);
            exit(EXIT_FAILURE);
          }
        }
        fileHandle = malloc(sizeof(FILE*) * numSubsys);
        for (i = 0; i < numSubsys; i++){
            fileout = realloc(fileout, 11+subsys_length[i]+5+1);
            for (int count = 0; count < 11; count++){
              fileout[count] = node_dir_name[count];
            }
            fileout[11] = '/';
            for (int count = 0; count < subsys_length[i]; count++){
              fileout[count+12] = subsys_names[i][count];
            }
            strncpy(&fileout[12+subsys_length[i]], ".csv", 5);
            fileHandle[i] = fopen(fileout, "w");
            if (fileHandle[i] == NULL){
                printf("Unable to open file %s\n", fileout);
                exit(EXIT_FAILURE);
            }
        }
    }

//  open the data file and walk through it to find out the number of lines of each node
    fp = fopen(args->data_file, "r");

    if (fp == NULL){
        printf("Unable to read %s file\n", args->data_file);
        exit(EXIT_FAILURE);
    }

    oldLine = malloc(sizeof(char));
    start_t = clock();
    while ((read = getline(&line, &len, fp)) != -1){
        if (line != NULL && strlen(line) > 0){
            oldLine = realloc(oldLine, (strlen(line) * sizeof(char))+1);
            strncpy(oldLine, line, strlen(line)+1);
        }
        colCount = 0;
        token = strtok(line, ",");
        old_i = 0;
        while (token != NULL){
            if (colCount == 1){
                i = 0;
                while (i < numNodes) {
                    if (strncmp(token, nodenames[i], nodeId_length) == 0){
                        node_line_count[i] += 1;
                        old_i = i;
                        break;
                    } else {
                        i++;
                    }
                }
            }
            if (colCount == 2){
                j = 0;
                while (j < numSubsys){
                    if (strncmp(token, subsys_names[j], subsys_length[j]) == 0){
                        subsys_line_count[old_i][j] += 1;
                        if (args->node_name != NULL && strncmp(args->node_name, nodenames[old_i], nodeId_length) == 0){
                            fwrite(oldLine, 1, strlen(oldLine), fileHandle[j]);
                            fflush(fileHandle[j]);
                        }
                        break;
                    } else {
                        j++;
                    }
                }
            }
            colCount++;
            token = strtok(NULL, ",");
        }
        rowCount++;
    }
    fclose(fp);
    end_t = clock();
    time_taken = ((double)(end_t - start_t))/CLOCKS_PER_SEC;

    if (args->node_name == NULL){
      printf("Time taken %f\n", time_taken);
      printf("Number of rows = %d \n", rowCount);
    }

    if (args->node_name != NULL){
        for (i = 0; i < numSubsys; i++){
            fclose(fileHandle[i]);
        }
    }

    if (args->node_name == NULL) {
        fp = fopen("node_line_count.csv", "w");
        if (fp == NULL) {
          printf("Unable to open node_line_count.csv\n");
          exit(EXIT_FAILURE);
        }
        fprintf(fp, "%14s,%12s,%10s,%10s,%10s,%10s,%10s,%10s,%10s,%10s,%10s,%10s\n",
            "NodeId", "Node", subsys_names[0], subsys_names[1], subsys_names[2],
            subsys_names[3], subsys_names[4], subsys_names[5], subsys_names[6],
            subsys_names[7], subsys_names[8], subsys_names[9]);
        for (i = 0; i < numNodes; i++) {
          fprintf(fp, "%14s,", nodenames[i]);
          fprintf(fp, "%12d,", node_line_count[i]);
          for (j = 0; j < numSubsys; j++) {
            if (j == numSubsys-1){
              fprintf(fp, "%10d", subsys_line_count[i][j]);
            } else {
              fprintf(fp, "%10d,", subsys_line_count[i][j]);
            }
          }
          fprintf(fp, "%s", "\n");
        }
        fclose(fp);
    }
    free(fileHandle);

    // section to read a file with the number of rows read previously
    // if the file is present, it compares the current row count with the
    // previous row count.
    // If the file is not present, it skips the comparison,
    // and just writes the file

    if (args->node_name != NULL) {
        int exist = stat("file_row_count.txt", &file_stats);
        if (exist == 1){
            fp = fopen("file_row_count.txt", "r+");
            fscanf(fp, "%d", &old_rowCount);
            if (rowCount != old_rowCount) {
                if (rowCount < old_rowCount) {
                    rowCount += old_rowCount;
                    fwrite(&rowCount, 1, sizeof(int), fp);
                } else if (rowCount > old_rowCount) {
                    fwrite(&rowCount, 1, sizeof(int), fp);
                }
            }
        } else {
            fp = fopen("file_row_count.txt", "w");
            fwrite(&rowCount, 1, sizeof(int), fp);
        }
        fclose(fp);
    }

    //free all of the allocated memory
    free(node_line_count);
    free(subsys_length);
    free(oldLine);
    free(fileout);
    free2d_c(nodenames, numNodes);
    free2d_c(subsys_names, numSubsys);
    free2d_i(subsys_line_count, numNodes);
    return 0;
}


static void usage(){
    printf("Usage: readFile -i <data file> \n");
    printf("                -f <node name file> \n");
    printf("                -s <subsystem name file> \n");
    printf("                -n <node name> \n");
}


int subsetFile(char* fileIn, char* fileOut, int linecount){
    FILE *fin, *fout;
    int count = 0;
    ssize_t read;
    size_t len = 0;
    char* line = NULL;
    fin = fopen(fileIn, "r");
    if (fin == NULL){
        printf("Unable to read file %s\n", fileIn);
        exit(EXIT_FAILURE);
    }
    fout = fopen(fileOut, "w");
    if (fout == NULL){
        printf("Unable to open file %s for writing\n", fileOut);
        exit(EXIT_FAILURE);
    }
    while ((read = getline(&line, &len, fin)) != -1){
        if (line != NULL && strlen(line) > 0){
            if (count >= linecount){
                fwrite(line, 1, strlen(line), fout);
                fflush(fout);
            } else {
                count++;
            }
        }
    }
    fclose(fin);
    fclose(fout);
    return 0;
}

static double str2double(char* token){
    char* end = NULL;
    double value = NaN;
    if (token != NULL){
        value = strtod(token, &end);
    }
    if (token == NULL || end == token){
        fprintf(stderr, "Could not convert %s to double\n", (token != NULL) ? token : "NULL");
        exit(1);
    }
}

int max(int a, int b){
    if (a > b){
        return a;
    } else {
        return b;
    }
}

//for character arrays
char** alloc2d_c(int numrows, int numcols){
    int i;
    char** outarr = malloc(numrows * sizeof(char*));
    for (i = 0; i < numrows; i++){
        outarr[i] = malloc(numcols * sizeof(char));
    }
    return outarr;
}

void free2d_c(char** inarr, int numrows){
    int i;
    for (i = 0; i < numrows; i++){
        free(inarr[i]);
    }
    free(inarr);
}

//for double arrays
double** alloc2d_d(int numrows, int numcols){
    int i;
    double** outarr = malloc(numrows * sizeof(double*));
    for (i = 0; i < numrows; i++){
        outarr[i] = malloc(numcols * sizeof(double));
    }
    return outarr;
}

void free2d_d(double** inarr, int numrows){
    int i;
    for (i = 0; i < numrows; i++){
        free(inarr[i]);
    }
    free(inarr);
}

//for integer arrays
int** alloc2d_i(int numrows, int numcols){
    int i;
    int** outarr = malloc(numrows * sizeof(int*));
    for (i = 0; i < numrows; i++){
        outarr[i] = malloc(numcols * sizeof(int));
    }
    return outarr;
}

void free2d_i(int** inarr, int numrows){
    int i;
    for (i = 0; i < numrows; i++){
        free(inarr[i]);
    }
    free(inarr);
}

void get_file_info(char* filename, int* file_length, int* max_row_length){
    FILE* fp;
    ssize_t read;
    size_t len;
    char *line = NULL;

    fp = fopen(filename, "r");
    if (fp == NULL){
        printf("Unable to open file %s\n", filename);
        exit(EXIT_FAILURE);
    }

    while ((read = getline(&line, &len, fp)) != -1){
        (*file_length) += 1;
        (*max_row_length) = max(*max_row_length, strlen(line));
    }
    (*max_row_length) -= 1;

    fclose(fp);
}
