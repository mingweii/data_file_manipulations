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
first, ext = os.path.splitext(root.filename)
first=os.path.basename(root.filename)

#a list of files under this directory
if ext=="":
    all_f=glob(first[:-1]+r'[0-9]*')
else:
    all_f=glob(first[:-1]+r'*'+ext)

all_files=sorted(all_f)
n=len(all_files)
prefix=os.path.basename(os.path.commonprefix(all_files))
print("There are "+ str(n)+ " "+ext+" files in this directory starting with "+ prefix)
#load the first data and get the dimension of the matrix
#matrix (# of files, # of rows, # of columns)

from printProgressBar import *

printProgressBar(0, n, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
data1=np.loadtxt(root.filename,skiprows=4,usecols=2)
if data1.ndim==1:
    matrix=np.empty([data1.shape[0],1,n])
    for i in range(0,n):
        temp=np.loadtxt(prefix+str(i)+ext,skiprows=4,usecols=2)
        matrix[:,0,i]=temp
        printProgressBar(i, n, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
else:
    matrix=np.empty([data1.shape[0],data1.shape[1],n])
    for i in range(0,n):
        temp=np.loadtxt(prefix+str(i)+ext,skiprows=4,usecols=2)
        matrix[:,:,i]=temp
        printProgressBar(i, n, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
#save the .mat files for MATLAB
savemat(prefix+'.mat',mdict={'matrix':matrix})
print("\n")
print(matrix.shape)
