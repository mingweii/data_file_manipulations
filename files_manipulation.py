
import os
import numpy as np
#import matplotlib.pyplot as plt
from scipy.io import loadmat, savemat
import h5py
#from tkinter import filedialog

def load_csv_to_mat(directory,nskiprows,usecols_list):
    from glob import glob
    import re
    #directory=directory+'/' # Change the orientation of the slash for Windows or Mac systems
#a list of files under this directory
    all_f=glob(directory+r'*.csv')
    all_files=sorted(all_f,key=os.path.getmtime) #sort the file list by modified time.
#all_files=sorted(all_f,key=os.path.basename)
    prefix = os.path.basename(os.path.commonprefix(all_files))

    print("There are "+ str(len(all_files))+" .csv files in this directory starting with "+prefix)

#load the first data and get the dimension of the matrix
#matrix (# of rows, # of columns, # of files)

    data1=np.loadtxt(all_files[0],delimiter=',',skiprows=nskiprows,usecols=usecols_list)# check the columns
    saiz=[data1.shape[0],data1.shape[1],len(all_files)]
    matrix=np.empty(saiz)
    print(saiz)
    index=0
    for files in all_files:
        temp=np.loadtxt(files,delimiter=',',skiprows=nskiprows,usecols=usecols_list)# check the columns
        matrix[:,:,index]=temp
        #print(str(files))
        index=index+1
#save the .mat files for MATLAB
    savemat(prefix+'.mat',mdict={'matrix':matrix})
    print("The size of the saved matrix is "+ str(matrix.shape))

def merge_multiple_mat(dataDir,save_to_h5=False):
    merged_data={}

    sorted_file_list=sorted(os.listdir(dataDir)) # sort the file list first by name
    for file in sorted_file_list:
        d=loadmat(dataDir+file)
        if merged_data=={}:
            merged_data=d.copy()
            merged_data.pop('__globals__')
            merged_data.pop('__header__')
            merged_data.pop('__version__')
            for i in merged_data.keys():
                merged_data[i]=np.round(np.squeeze(merged_data[i]),10)
        else:
            for i in d.keys() and merged_data.keys():
                d[i]=np.round(np.squeeze(d[i]),10)
                if np.array_equal(merged_data[i],d[i]) and (d[i]).ndim==1 and len(d[i])>1 :
                    # Only check 1D array with multiple elements.
                    merged_data[i]=merged_data[i]
                else:
                    merged_data[i]=np.dstack((merged_data[i],d[i]))
    for i in merged_data.keys():

        merged_data[i]=np.squeeze(merged_data[i])
        print(str(i)+".shape="+str(merged_data[i].shape))
    if save_to_h5==False:
        savemat('merged.mat',merged_data)
    else:
        if os.path.exists("merged.h5"):
            os.remove("merged.h5")
        with h5py.File('merged.h5', 'w') as fd:
            for i in merged_data.keys():
                fd[i] = merged_data[i]
            fd.close()
