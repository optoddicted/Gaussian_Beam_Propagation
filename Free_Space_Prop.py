# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 17:28:02 2017

@author: Pravin Vaity
"""
"------------------------------------------------------------------------------"
" Modules uploading "
import tkinter as Tk
from tkinter import ttk
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

"------------------------------------------------------------------------------"
" Main GUI Window class "  
class WinDow:

    def __init__(self):      

        self.button1 = Tk.Button(frame,text='Run', command=self._display, bg="green")
        self.button1.place(x=10,y=190,height=25,width=80)
        
        self.button2 = Tk.Button(frame, text='Quit', command=_quit,bg="red")
        self.button2.place(x=10,y=360,height=25,width=80)

        
    def _display(self):
        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        wo = wo_in.get()
        lm = lm_in.get()
        z  = z_in.get()
        
        Ig,x,y = Gauss_Beam_XY(lm,wo,z)
        xmax = np.max(x)         
        Xm,xscale = Plot_Scale(xmax)        
        tick = np.linspace(-Xm,Xm,5)
        a.set_title("XY Plane")
        a.axes.set_xticks(tick, minor=False)
        a.axes.set_yticks(tick, minor=False)
        a.tick_params(labelsize=10)
        a.imshow(Ig,extent =[-Xm, Xm,-Xm, Xm])
        a.set_xlabel(xscale)
        
        self.canvas = FigureCanvasTkAgg(f, master=root)
        self.canvas.show()
        self.canvas.get_tk_widget().place(x=125,y=25,height=350,width=350)
        
        # second figure
        if z != 0:                    
            f2 = Figure(figsize=(4, 7), dpi=100)
            b = f2.add_subplot(111)
            
            Ig,x,z = Gauss_Beam_Prop(lm,wo,z)
            zmax = np.max(z);
            Zm,zscale = Plot_Scale(zmax)
            
            b.imshow(Ig,extent =[0, Zm,-Xm, Xm],aspect='auto')
            b.set_title("X-Z Plane")
            b.tick_params(labelsize=8)
            b.set_ylabel(xscale)
            b.set_xlabel(zscale)
            
            self.canvas = FigureCanvasTkAgg(f2, master=root)
            self.canvas.show()
            self.canvas.get_tk_widget().place(x=500,y=25,height=350,width=450)
        
"------------------------------------------------------------------------------"        
" Functions "
def Gauss_Beam_XY(lm,wo,z):
    if z == 0:
        z = 1E-32  
    # Beam Parameters   
    k  = 2*np.pi/lm     # Wave number
    zr = k*wo*wo/2          # Rayleigh Range
    w  = wo*(1+(z/zr)**2)**0.5 # beam radius at z
    R  = z + zr*zr/z                # curvature
    Ps = np.arctan(z/zr)              # Guoy Phase
    
    #  Display parameter
    N = 100; L = 5*w; dx = L/N;
    m  = np.linspace(-N/2,N/2,N+1);  xy = m*dx; 
    x, y   = np.meshgrid(xy,xy);   r  = (x*x+y*y)**0.5;
  
    Eg = np.exp(-(r/w)**2)*np.exp(1j*(k*z+0.5*k*r*r/R-Ps))
    I = np.abs(Eg); Ig = I*I
    w_out.set(w)
    zr_out.set(zr)
    return Ig,x,y
    
def Gauss_Beam_Prop(lm,wo,Z):
    
            # Beam Parameters   
    k  = 2*np.pi/lm     # Wave number
    zr = k*wo*wo/2          # Rayleigh Range
    wi = wo*(1+(Z/zr)**2)**0.5 # beam radius at z 
        
    #  Display parameter
    N = 100; L = 4*wi; dx = L/N;
    m  = np.linspace(-N/2,N/2,N+1);  xi = m*dx; 
    dx = Z/N;
    m  = np.linspace(0,N,N);  zi = m*dx;     
    z, x   = np.meshgrid(zi,xi);
    w  = wo*(1+(z/zr)**2)**0.5 # beam radius at z    
  
    Eg = np.exp(-(x/w)**2)
    I = np.abs(Eg); Ig = I*I
    return Ig,x,z   

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
root.geometry('980x400')
root.title('Gaussian Beam Propagation')

# variable type definitions
wo_in = Tk.DoubleVar() # - Beam width
lm_in = Tk.DoubleVar() # Wavelength of light
z_in  = Tk.DoubleVar() # Z plane

wo_in.set(1E-3)
lm_in.set(400E-9)
z_in.set(0)

w_out  = Tk.DoubleVar() # - Beam width
zr_out = Tk.DoubleVar() #  Rayleigh Range
Ig_out = Tk.DoubleVar()

"------------------------------------------------------------------------------"
"  Frame for lables & input  "

frame = Tk.Frame(root, bg='grey',height=400,width=100)
frame.place(x=0,y=0,height=400,width=100)

" Input Values "
ttk.Label(frame,text="Wavelength",anchor="center").place(x=5,y=5,height=25,width=90)
lm_entry=ttk.Entry(frame,textvariable=lm_in)
lm_entry.place(x=5,y=30,height=25,width=90)

ttk.Label(frame,text="Beam Waist",anchor="center").place(x=5,y=65,height=25,width=90)
wo_entry=ttk.Entry(frame,textvariable=wo_in)
wo_entry.place(x=5,y=90,height=25,width=90)

ttk.Label(frame,text="Z Distance",anchor="center").place(x=5,y=125,height=25,width=90)
z_entry=ttk.Entry(frame,textvariable=z_in)
z_entry.place(x=5,y=150,height=25,width=90)

" Output Value "
ttk.Label(frame,text="RayleighRange").place(x=5,y=233,height=25,width=90)
ttk.Label(frame,textvariable=zr_out).place(x=5,y=260,height=25,width=90)

ttk.Label(frame,text="Beam Radius",anchor="center").place(x=5,y=293,height=25,width=90)
ttk.Label(frame,textvariable=w_out).place(x=5,y=320,height=25,width=90)


" Main loop "
WinDow()
root.mainloop()
"----------------------------------- END --------------------------------------"