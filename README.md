# load_multiple_data-save_mat
Load multiple numerical data files with various columns in a directory and save the matrix to a MATLAB .mat file
The filenames of the text files to be loaded are restricted to the format:
 'Some non-numeric characters"+"numbers starting with 1" + extension
 The extension could be text files with three character, like .txt, .dat,...
 
 Examples: if the files are abc1,abc2,..., abc1539 with 300 rows and 5 columns, then a 3D matrix with dimension (1539,300,5) will be saved into a mat file for further analysis in MATLAB

Usage:
1. select the first file with the above pattern starting with 1, ex: abc1.
2. The output file abc.mat will contain a matrix with the dimension of (# of files, # of rows, # of columns)


