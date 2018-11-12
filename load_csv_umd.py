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
all_files=sorted(all_f)
prefix = os.path.basename(os.path.commonprefix(all_files))

print("There are "+ str(len(all_files))+" "+ext+" files in this directory starting with "+prefix)

#load the first data and get the dimension of the matrix
#matrix (# of rows, # of columns, # of files)

data1=np.loadtxt(root.filename,delimiter=',',skiprows=54,usecols=(2,3,4,5))
saiz=[data1.shape[0],data1.shape[1],len(all_files)]
matrix=np.empty(saiz)
index=0
for files in all_files:
    temp=np.loadtxt(files,delimiter=',',skiprows=54,usecols=(2,3,4,5))
    matrix[:,:,index]=temp
    index=index+1
#save the .mat files for MATLAB
savemat(prefix+'.mat',mdict={'matrix':matrix})
print("The size of the saved matrix is "+ str(matrix.shape))
