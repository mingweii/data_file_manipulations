from glob import glob
import os
import re
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
directory=directory+'/' # Change the orientation of the slash for Windows or Mac systems
print(directory)
first, ext=os.path.splitext(root.filename)
#a list of files under this directory
all_f=glob(directory+r'*'+ext)
all_files=sorted(all_f,key=os.path.getmtime) #sort the file list by modified time.

prefix = os.path.basename(os.path.commonprefix(all_files))

print("There are "+ str(len(all_files))+" "+ext+" files in this directory starting with "+prefix)

#load the first data and get the dimension of the matrix
#matrix (# of rows, # of columns, # of files)

data1=np.loadtxt(root.filename,delimiter=',',skiprows=50,usecols=(3,4))# check the columns
saiz=[data1.shape[0],len(all_files)]
matrix=np.empty(saiz)
print(saiz)

#Extracting bias
bias=np.loadtxt(root.filename,delimiter=',',skiprows=50,usecols=3)

Bfield=np.empty(len(all_files))

index=0
for files in all_files:
    print(str(files))
    temp=np.loadtxt(files,delimiter=',',skiprows=50,usecols=4)# check the columns
    matrix[:,index]=temp
    temp2=np.genfromtxt(files,dtype=str, delimiter=',',skip_header=44,usecols=0,max_rows=1)
    temp3=str(temp2).lstrip("Set Magnet field (T): ")
    Bfield[index]=float(temp3)
    print(Bfield[index])
    index=index+1

B_indx=Bfield.argsort()
sorted_B=Bfield[B_indx]
sorted_matrix=matrix[:,B_indx]
#save the .mat files for MATLAB
savemat(prefix.strip("_-")+'.mat',mdict={'dR':sorted_matrix,'B':sorted_B,'bias':bias})
print("The size of the saved dR matrix is "+ str(sorted_matrix.shape))
print("The size of the saved Bfield is "+ str(sorted_B.shape))
print("The size of the saved bias is "+ str(bias.shape))
