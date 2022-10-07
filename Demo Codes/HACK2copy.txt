import matplotlib.pyplot as plt  #pr,pd,par,pad must vary for different age groups . n must depend upon no of available hosp beds,icu wards,etc.give apt values for R0start and R0end
from scipy.integrate import odeint#x0 depends upon the lockdown period,c depends upon incubation period.also c must depend upon a few other env conditions if poss#
import tkinter as tk
import numpy as np
import math
def R(t):
    return (R0start-R0end)/(1+(math.e)**(-1*3*(t-x0))) + R0end
def b(t):
    return R(t)*0.25
def r1(t):
    return 0.4
def d1(t):
    return 0.09
def cp(y,t,N,b,c,p,a1,a2,r,r1,d1,pr,pd,par,pad):
    S,E,Ia,Is,A,R,D,n=y
    N=S+E+Ia+Is+A+R+D
    dndt=t/300
    dSdt=-b(t)*Is*S/N
    dEdt=b(t)*Is*S/N-c*E
    dIadt=c*p*E-a1*n*Ia-r1(t)*pr*Ia-d1(t)*pd*Ia
    dIsdt=c*(1-p)*E-a2*n*Is-r1(t)*pr*Ia-d1(t)*pd*Is
    dAdt=a1*n*Ia+a2*n*Is-r*par*A-(1-r)*pad*A
    dRdt=r*par*A+r1(t)*pr*Ia+r1(t)*pr*Is
    dDdt=(1-r)*pad*A+d1(t)*pd*Is+d1(t)*pd*Ia
    return dSdt,dEdt,dIadt,dIsdt,dAdt,dRdt,dDdt,dndt

N=500000
R0start=80
R0end=1
x0=55
p=0.5
c=0.5
a1,a2=0.05,0.03
r=0.8
pr,pd,par,pad=0.5,0.009,0.6,0.009

t=np.linspace(0,200,201)
S0,E0,Ia0,Is0,A0,R0,D0,n0=N-1,1,0,0,0,0,0,0.6
y0=S0,E0,Ia0,Is0,A0,R0,D0,n0
info=odeint(cp,y0,t,args=(N,b,c,p,a1,a2,r,r1,d1,pr,pd,par,pad))
S,E,Ia,Is,A,R,D,n=info.T
def plotcurve(t, S, E, Ia, Is, A, R, D):
  f, ax = plt.subplots(1,1,figsize=(10,4))
  ax.plot(t, S, 'b', alpha=0.7, linewidth=2, label='Susceptible')
  ax.plot(t, E, 'y', alpha=0.7, linewidth=2, label='Exposed')
  ax.plot(t, Ia, 'r', alpha=0.7, linewidth=2, label='Infected (asym)')
  ax.plot(t, Is, 'c', alpha=0.7, linewidth=2, label='Infected (sym)')
  ax.plot(t, A, 'm', alpha=0.7, linewidth=2, label='Admitted')
  ax.plot(t, R, 'g', alpha=0.7, linewidth=2, label='Recovered')
  ax.plot(t, D, 'k', alpha=0.7, linewidth=2, label='Dead')
  ax.plot(t, S+E+Ia+Is+A+R+D, 'c--', alpha=0.7, linewidth=2, label='Total')
  ax.set_title("STAY HOME, STAY SAFE!")
  ax.set_xlabel('Time (days)')
  f.suptitle("COVID-19 PROPHECY",fontsize=20,color="b")
  ax.yaxis.set_tick_params(length=0)
  ax.xaxis.set_tick_params(length=0)
  ax.grid(b=True, which='major', c='w', lw=2, ls='-')
  legend = ax.legend()
  legend.get_frame().set_alpha(0.5)
  for spine in ('top', 'right', 'bottom', 'left'):
      ax.spines[spine].set_visible(False)
  plt.show()
plotcurve(t,S,E,Ia,Is,A,R,D)  
  


    
    
    
    
   

