from glob import glob
import os
from re import match
import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from scipy.io import savemat
#from re import match
from tkinter import filedialog

# open a dialog asking for first file to load
root=tk.Tk()
root.withdraw()
root.filename=filedialog.askopenfilename(initialdir ='~/')

#Move and print the directory
directory=os.path.dirname(root.filename)
os.chdir(directory)
directory=directory+'/'
print(directory)

#Obtain the basename of the files and extract the extension
file_name=os.path.basename(root.filename)[:-5]
first, ext = os.path.splitext(root.filename)
#a list of files under this directory
all_files=glob(directory+r'*')

#Extract the pattern and print the number of files
valid=list([])
for files in all_files:
    if match(directory+file_name+r'\d+'+ext, files):
        valid.append(files)
n=len(valid)
print("Number of files loaded: "+str(n))

#load the first data and get the dimension of the matrix
#matrix (# of files, # of rows, # of columns)
data1=np.loadtxt(root.filename)
matrix=np.zeros([n,data1.shape[0],data1.shape[1]],dtype=float)
matrix[0,:,:]=data1
#load the rest files
from printProgressBar import *

printProgressBar(0, n, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
for i in range(1,n):
    temp=np.loadtxt(directory+file_name+str(i+1)+ext)
    matrix[i,:,:]=temp
    printProgressBar(i+1, n, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
#save the .mat files for MATLAB
savemat(file_name+'.mat',mdict={'matrix':matrix})
print(matrix.shape)
