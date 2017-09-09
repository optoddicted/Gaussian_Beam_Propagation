# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 20:39:36 2017

@author: pravin
"""
import numpy as np

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
    return w,zr,Ig,x,y
    
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
    
def Gauss_Beam_Lens(lm,wo,zr,z,f):
    
    Ig,x,Z = Gauss_Beam_Prop(lm,wo,z)
    z = np.max(Z);
    
    if z == f:
        M = f/zr                # Magnification
    else:            
        rr = zr/(z-f)
        Mr = np.abs(f/(z-f))
        M  = Mr/(1+rr*rr)**0.5    # Magnification
            
    wf = M*wo                    # waist at focus
    zf = M*M*(z-f)+f            # Waist position    
    
    I,x,Z = Gauss_Beam_Prop(lm,wf,zf)
    Ib = np.fliplr(I)
    print("Initial=",z,"Final=",zf)
    Ia = np.concatenate((Ig,Ib),axis=1)
    zf = z+zf
    return z, zf, Ia, wf
    