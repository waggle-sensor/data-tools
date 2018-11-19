typedef struct{
    char* node_names_file;
    char* subsystem_name_file;
    char* data_file;
    char* node_name;
} arguments;

int max(int a, int b);
static double str2double(char* token);
static void usage();
int readFile(arguments* args);
void get_file_info(char* filename, int* file_length, int* max_row_length);
int subsetFile(char* fileIn, char* fileOut, int linecount);
char** alloc2d_c(int numrows, int numcols);
int** alloc2d_i(int numrows, int numcols);
double** alloc2d_d(int numrows, int numcols);
void free2d_c(char** inarr, int numrows);
void free2d_i(int** inarr, int numrows);
void free2d_d(double** inarr, int numrows);