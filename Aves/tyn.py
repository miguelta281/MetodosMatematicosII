#!/usr/bin/env python
# coding: utf-8

# In[1]:
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.io import wavfile
import pandas as pd
import matplotlib.gridspec as gridspec

def stereo (data): #data 2D
    canal1 =[]
    canal2 = []
    for i in range(len(data)):
        canal1.append(data[i][0])
        canal2.append(data[i][1])
    
    canal1 = np.array(canal1)
    canal2 = np.array(canal2)

    return (canal1,canal2)

def spectrograma2D (canal, fs,c=0,d = 1, log = 0,cmapp = "hot" ,a = 10, b = 10): 
    """
    canal: Vector con las frecuencias
    fs: frecuencia de muestreo
    cmapp: escala de color de la figura
    log: Uso de la escala logaridmica para las potencias, 0 -->no, 1-->si
    a,b: Tamaño de la figura
    """
    Sxx, f, t, im= plt.specgram(canal,Fs=fs, cmap = cmapp)
    #f, t, Sxx = signal.spectrogram(canal, fs,nperseg = npersegg )
    Sxx = (Sxx / np.max(Sxx))
    if log == 0:
        plt.figure(figsize=(a,b))
        plt.pcolormesh(t, f, Sxx, cmap= cmapp)
        plt.ylabel('Frecuencia [Hz]', fontsize = 16)
        plt.xlabel('Tiempo [s]', fontsize = 16)
        plt.ylim(c,d)
        plt.colorbar()    
        plt.show()
        
    elif log == 1:
        plt.figure(figsize=(a,b))
        plt.pcolormesh(t, f, 10*np.log10(Sxx), cmap= cmapp)
        plt.ylabel('Frecuencia [Hz]', fontsize = 16)
        plt.xlabel('Tiempo [s]', fontsize = 16)
        plt.colorbar()    
        plt.show()
    
    return (t,f,Sxx)

def spectrograma3D (canal, fs, log = 0,cmapp = "hot" ,a = 10, b = 10):
    f, t, Sxx = signal.spectrogram(canal, fs)
    Sxx = (Sxx / np.max(Sxx))
    if log == 0:
        fig = plt.figure(figsize=(a,b))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(t[None,:], f[:,None], Sxx, cmap= cmapp)
        ax.set_xlabel('Tiempo [s] ')
        ax.set_ylabel('Frecuencia [Hz]')
        ax.set_zlabel('Potencia')
        plt.show()
        
    elif log == 1:
        fig =plt.figure(figsize=(a,b))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(t[None,:], f[:,None], 10*np.log10(Sxx), cmap= cmapp)
        ax.set_xlabel('Tiempo [s] ')
        ax.set_ylabel('Frecuencia [Hz]')
        ax.set_zlabel('Potencia')
        plt.show()

def matr (f,t,Sxx):
    a1 = []
    for i in range(len((f))):
        b1 = []
        for j in range(len(t)):
            b1.append(Sxx[i][j])
        a1.append(np.array(b1))
    a2 = pd.DataFrame(a1)
    a2.index = f
    return a2

def huella (f,t,Sxx,name,potencia):
    data = matr(f,t,Sxx)
    data.index = f
    
    l = []
    b = []
    h = []
    for i in range(0,data.shape[1]):
        #print(i)
        s = []
        jaja  =data.index
        for j in range(len(data.iloc[:,0])):
            k = jaja[j]
            if (data.iloc[:,i][k] > potencia):
                s.append(j)
        l.append(s)
    for i in range(len(l)):
        c = []
        for j in range(len(l[i])):
            #print(l[i][j])
            c.append(f[l[i][j]])
        b.append(c)
        
    for i in range(len(b)):
        for j in range(len(b[i])):
            h.append(b[i][j])
    
    h.sort()
    
    plt.figure(figsize=(6,6))
    plt.plot(h,'*', label = name)
    plt.ylabel('Frecuencia [Hz]', fontsize = 16)
    plt.legend()
    plt.show()
    
    return h,data

def huella_p (f,t,Sxx,name,dis_val):
    
    huellaa = []
    huellaa, data = huella(f,t,Sxx,name,dis_val)
    
    pp = np.zeros((int(np.max(huellaa)+10), len(huellaa)))
    p = []
    for i in range(len(huellaa)):
        jiji = data.index
        indice = int(np.where(data.index == huellaa[i])[0])
        pp[int(jiji[indice])] = np.max(data.iloc[indice])
        p.append(np.max(data.iloc[indice]))

    
    hhh = np.array(huellaa)
    ppp = np.array(p)
    
    plt.figure(figsize=(16,8))
    plt.subplots_adjust(hspace=0.5)   
        
    plt.subplot(121)
    fff = np.linspace(0,len(pp),len(pp))
    ttt = np.linspace(0,len(pp[0]),len(pp[0]))
    plt.pcolormesh(ttt, fff, pp, cmap= "hot")
    plt.ylim(int(np.min(huellaa)-10),int(np.max(huellaa)+10))
    #plt.ylim(4000,5000)
    plt.ylabel('Frecuencia [Hz]', fontsize = 16)
    plt.colorbar()
    
    plt.subplot(122)
    plt.stem(hhh, ppp)
    plt.ylabel('Potencia', fontsize = 16)
    plt.xlabel('Frecuencia [Hz]', fontsize = 16)
    
     
    plt.show()
    
  
             
    return hhh, ppp 
