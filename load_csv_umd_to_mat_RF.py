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
all_files=glob(directory+r'*'+ext)
prefix = os.path.basename(os.path.commonprefix(all_files))

print("There are "+ str(len(all_files))+" "+ext+" files in this directory starting with "+prefix)

#load the first data and get the dimension of the matrix
#matrix (# of rows, # of files)

data1=np.loadtxt(root.filename,delimiter=',',skiprows=54,usecols=5)# check the columns
saiz=[data1.shape[0],len(all_files)]
matrix=np.empty(saiz)
print(saiz)

#Extracting bias
bias=np.loadtxt(root.filename,delimiter=',',skiprows=54,usecols=3)
#Extracting frequency
freq_tmp=np.genfromtxt(root.filename,dtype=str, delimiter=',',skip_header=48,usecols=0,max_rows=1)
freq_tmp2=str(freq_tmp).rstrip("MHz")
freq_tmp3=freq_tmp2.lstrip("Frequency Value: ")
frequency=float(freq_tmp3)*1e6
print('frequency is at'+ str(frequency/1e9)+'GHz')
RFpower=np.empty(len(all_files))

index=0
for files in all_files:
    print(str(files))
    temp=np.genfromtxt(files,delimiter=',',skip_header=54,usecols=5)# check the columns
    matrix[:,index]=temp
    temp2=np.genfromtxt(files,dtype=str, delimiter=',',skip_header=49,usecols=0,max_rows=1)
    temp3=str(temp2).rstrip("dBm")
    temp4=temp3.lstrip("Power Value: ")
    RFpower[index]=float(temp4)
    print(RFpower[index])
    index=index+1

RF_indx=RFpower.argsort()
sorted_RF=RFpower[RF_indx]
sorted_matrix=matrix[:,RF_indx]
#save the .mat files for MATLAB
savemat(prefix.strip("_-")+'.mat',mdict={'dR':sorted_matrix,'RF':sorted_RF,'f':frequency,'bias':bias})
print("The size of the saved dR matrix is "+ str(sorted_matrix.shape))
print("The size of the saved RF is "+ str(sorted_RF.shape))
print("The size of the saved bias is "+ str(bias.shape))
print("The saved RF frequency is "+ str(frequency/1e9)+'GHz')
