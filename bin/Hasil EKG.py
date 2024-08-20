from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# from tkinter import StringVar
# from tkinter import Label

import tkinter as tk #tampilan
import numpy as np #matematis
import serial as sr #arduino dgn python
import time #realtime
import matplotlib.pyplot as plt #membuat grafik


#----- Global Variabel ---------
data = np.array([])
cond = False
R = [] #Isinya nilai tertinggi setiap data yg masuk
Status = []
counter = 0

#----- plot Data --------------------------------
def update_counter(milis):
    global counter
    counter += float(milis)  

def zero_counter():
    global counter
    counter = 0 

def plot_data():
    global cond,data


    if (cond == True):
        a = s.readline()
        a = str(a,'utf-8')
        dataArray = a.split(',')

        print(dataArray[0])
        print(dataArray[1])

        update_counter(dataArray[1])
        if(float(dataArray[0]) > 5 ): #treshold
            BPM = round(float(60000/counter),2) 

            if BPM < 60 :
                # Label1.config(text = status)
                status = "Slow AF" #deatakny lemah

            elif BPM >= 60 and BPM <=100:
                status = "Normal" 
                
            elif BPM >= 101 and BPM <= 150:
                # direction.set("Rapid AF")
                status = "Rapid AF" #cukup cepat
                
            elif BPM > 150:
                # direction.set("Uncontrol AF")
                status = "Uncontrol AF" 

            R.append(counter)
            R.append(BPM)
            R.append(status)

            zero_counter()
        
            root.update()
            Label1 = tk.Button(root, text = status)
            Label1.place(x=300, y = 450)
            
        if(len(data) < 500):
            data = np.append(data,float(a[0:4]))
        else:
            data[0:499] = data[1:500]
            data[499] = float(a[0:4])
        #data_sp = np.append(data_sp,sp)
        #ax.clear()
        #ax.plot(data)
        lines.set_xdata(np.arange(0,len(data)))
        lines.set_ydata(data)
        
        print(R)
        
        # print(a)

        # signal = (data > 500)
        # plt.plot(signal.nonzero()[0], data[signal], 'ro')
        # plt.show()

        canvas.draw()

    root.after(1, plot_data)

def plot_start():
    global cond
    cond = True
    s.reset_input_buffer()

def plot_stop():
    global cond
    cond = False

#---Main gui -------------------------------

root = tk.Tk()
root.title('Serial Plot GUI')
root.configure(background='light blue')
root.geometry("700x500") #windows size pixel

#----- Plot Oject di GUI --------
#add figure 
fig = Figure()
ax = fig.add_subplot(111)

ax.set_title('AD8232')
ax.set_xlabel('waktu')
ax.set_ylabel('tinggi')
ax.set_xlim(0,500)
ax.set_ylim(0,50)
lines = ax.plot([],[])[0]


canvas = FigureCanvasTkAgg(fig, master=root) #Tk Drawing area
canvas.get_tk_widget().place(x=10, y=10, width=500, height=400)
canvas.draw()

#----- Button --------------------------------
root.update()
start = tk.Button(root, text = "Start", font = ('calbiri',12),command = lambda: plot_start())
start.place(x=100, y = 450)

root.update()
stop = tk.Button(root, text = "Stop", font = ('calbiri',12), command = lambda: plot_stop())
stop.place(x = start.winfo_x()+start.winfo_reqwidth() + 20, y = 450)




#----- Serial Port ---------
s = sr.Serial('COM3', 9600)
s.reset_input_buffer()


root.after(1,plot_data)
root.mainloop()