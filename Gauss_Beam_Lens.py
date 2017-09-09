# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 21:38:20 2017

@author: pravin vaity
"""
" Gaussian beam Propagation through lens "

"------------------------------------------------------------------------------"
" Modules uploading "
import tkinter as Tk
from tkinter import ttk
import numpy as np
import Gauss_Beam

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

"------------------------------------------------------------------------------"
" Main GUI Window class "  
class WinDow:

    def __init__(self):      

        self.button1 = Tk.Button(frame,text='Run', command=self._display, bg="green")
        self.button1.place(x=30,y=240,height=25,width=80)
        
        self.button2 = Tk.Button(frame, text='Quit', command=_quit,bg="red")
        self.button2.place(x=30,y=400,height=25,width=80)

        
    def _display(self):
        f1 = Figure(figsize=(5, 4), dpi=100)
        a = f1.add_subplot(111)
        wo = wo_in.get()*1E-3   # Beam waist
        lm = lm_in.get()*1E-9   # Wavelength
        z  = z_in.get()*1E-2    # Lens Position
        f  = f_in.get()*1E-2    # Focal length 
        
        w,zr,Ig,x,y = Gauss_Beam.Gauss_Beam_XY(lm,wo,z)
        xmax = np.max(x)         
        Xm,xscale = Plot_Scale(xmax)        
        tick = np.linspace(-Xm,Xm,5)
        a.set_title("XY Plane")
        a.axes.set_xticks(tick, minor=False)
        a.axes.set_yticks(tick, minor=False)
        a.tick_params(labelsize=10)
        a.imshow(Ig,extent =[-Xm, Xm,-Xm, Xm])
        a.set_xlabel(xscale)
        
        self.canvas = FigureCanvasTkAgg(f1, master=root)
        self.canvas.show()
        self.canvas.get_tk_widget().place(x=165,y=25,height=350,width=350)
        
        # second figure
        if z != 0:                    
            f2 = Figure(figsize=(4, 7), dpi=100)
            b = f2.add_subplot(111)
            
            print("Z=",z)
            
            Zi,zmax,Ig,wf = Gauss_Beam.Gauss_Beam_Lens(lm,wo,zr,z,f)
            w_out.set(wf*1E3)
            if zr < f:
                f_out.set(np.inf)
            else:
                f_out.set(zmax*1E2)

            Zm,zscale = Plot_Scale(zmax)
           
            b.imshow(Ig,extent =[0, Zm,-Xm, Xm],aspect='auto')
            b.set_title("X-Z Plane")
            b.tick_params(labelsize=8)
            b.axis("off")
            b.set_ylabel(xscale)
            b.set_xlabel(zscale)
            el = Ellipse((Zm/2,0), Zm/8,Xm*1.5,angle=0.0, color=(0.5,0.5,0.4,0.4))
            b.add_artist(el)
            plt.show()
             
            self.canvas = FigureCanvasTkAgg(f2, master=root)
            self.canvas.show()
            self.canvas.get_tk_widget().place(x=540,y=25,height=350,width=450)
        
"------------------------------------------------------------------------------"        
" Functions "
   

def Plot_Scale(xmax):# creating proper axes scale for plotting 
    
    Xs = str(xmax)
    Indx = 0;
    if Xs[0]=='0':
        for ii in range(len(Xs)-1):
            if Xs[ii+2]=='0':
                Indx = Indx +1
            else:
                break
        if Indx < 3:
            Xm = xmax*1E3; xscale = str("mm")
        elif Indx < 6:
            Xm = xmax*1E6; xscale = str("$\mu$m")
    else:
        if Xs.find("e") ==-1:
            Indx = Xs.find(".")
            if Indx > 3:
                Xm = xmax*1E-3; xscale = str("Km")
            else:
                Xm = xmax; xscale = str("m") 
        else:
            Indx =Xs.find("-")
            if Indx < 6:
                Xm = xmax*1E6; xscale = str("$\mu$m")
    return Xm, xscale                
                

def _quit():
    
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                # Fatal Python Error: PyEval_RestoreThread: NULL tstate

"------------------------------------------------------------------------------"
"Initilization "                       
    
root = Tk.Tk()
root.geometry('1020x450')
root.title('Gaussian Beam Propagation Through Thin Lens')

# variable type definitions
wo_in = Tk.DoubleVar() # - Beam width
lm_in = Tk.DoubleVar() # Wavelength of light
z_in  = Tk.DoubleVar() # Lens Position
f_in  = Tk.DoubleVar() # focal length of lens

wo_in.set(1)
lm_in.set(400)
z_in.set(10)
f_in.set(20)

w_out  = Tk.DoubleVar() # - Beam width
f_out = Tk.DoubleVar() #  Rayleigh Range
#Ig_out = Tk.DoubleVar()

"------------------------------------------------------------------------------"
"  Frame for lables & input  "

frame = Tk.Frame(root, bg='grey',height=450,width=130)
frame.place(x=0,y=0,height=450,width=130)

" Input Values "
ttk.Label(frame,text="Wavelength (nm)",anchor="center").place(x=5,y=5,height=25,width=120)
lm_entry=ttk.Entry(frame,textvariable=lm_in,justify="center")
lm_entry.place(x=5,y=30,height=25,width=120)

ttk.Label(frame,text="Beam Waist (mm)",anchor="center").place(x=5,y=65,height=25,width=120)
wo_entry=ttk.Entry(frame,textvariable=wo_in,justify="center")
wo_entry.place(x=5,y=90,height=25,width=120)

ttk.Label(frame,text="Lens Position (cm)",anchor="center").place(x=5,y=125,height=25,width=120)
z_entry=ttk.Entry(frame,textvariable=z_in,justify="center")
z_entry.place(x=5,y=150,height=25,width=120)

ttk.Label(frame,text="Focal Length (cm)",anchor="center").place(x=5,y=185,height=25,width=120)
z_entry=ttk.Entry(frame,textvariable=f_in,justify="center")
z_entry.place(x=5,y=210,height=25,width=120)

" Output Value "
ttk.Label(frame,text="Focus Waist (mm)",anchor="center").place(x=5,y=277,height=25,width=120)
ttk.Label(frame,textvariable=w_out).place(x=5,y=305,height=25,width=120)

ttk.Label(frame,text="Focus Point (cm)",anchor="center").place(x=5,y=337,height=25,width=120)
ttk.Label(frame,textvariable=f_out).place(x=5,y=365,height=25,width=120)


" Main loop "
WinDow()
root.mainloop()
"----------------------------------- END --------------------------------------"