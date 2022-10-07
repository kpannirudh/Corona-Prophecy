import matplotlib.pyplot as plt  #pr,pd,par,pad must vary for different age groups . n must depend upon no of available hosp beds,icu wards,etc.give apt values for R0start and R0end
from scipy.integrate import odeint#x0 depends upon the lockdown period,c depends upon incubation period.also c must depend upon a few other env conditions if poss#
import tkinter as tk
import numpy as np
import math
def R(t):
    return (R0start-R0end)/(1+math.e**(-(t+x0))) + R0end
def b(t):
    return R(t)*0.5
def n(t):
    return 0.6+(Beds*100/N)
def r1(t):
    return 0.5
def d1(t):
    return 0.5
def cp(y,t,N,b,c,p,a1,a2,n,r,r1,d1,pr,pd,par,pad):
    S,E,Ia,Is,A,R,D=y
    N=S+E+Ia+Is+A+R+D
    dSdt=-b(t)*Is*S/N
    dEdt=b(t)*Is*S/N-c*E
    dIadt=c*p*E-a1*n(t)*Ia-r1(t)*pr*Ia-d1(t)*pd*Ia
    dIsdt=c*(1-p)*E-a2*n(t)*Is-r1(t)*pr*Ia-d1(t)*pd*Is
    dAdt=a1*n(t)*Ia+a2*n(t)*Is-r*par*A-(1-r)*pad*A
    dRdt=r*par*A+r1(t)*pr*Ia+r1(t)*pr*Is
    dDdt=(1-r)*pad*A+d1(t)*pd*Is+d1(t)*pd*Ia
    return dSdt,dEdt,dIadt,dIsdt,dAdt,dRdt,dDdt
Beds=72616
N=82722262
R0start=16
R0end=10
x0=2
p=0.5
c=0.6
a1,a2=0.3,0.7
r=0.4
pr,pd,par,pad=0.7,0.3,0.9,0.1

t=np.linspace(0,50,51)
S0,E0,Ia0,Is0,A0,R0,D0=N-56746,0.1*(N),0.6*(24835),0.4*(24835),0.5*(24835),31316,704
y0=S0,E0,Ia0,Is0,A0,R0,D0
info=odeint(cp,y0,t,args=(N,b,c,p,a1,a2,n,r,r1,d1,pr,pd,par,pad))
S,E,Ia,Is,A,R,D=info.T
for i in range(0,51):
    print(S[i])


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



def Aboutscr():
        Ab=tk.Tk()
        Ab.configure(bg='white')
        Ab.title("CoronaVirus Prophecy - About")
        Ab.columnconfigure(0,weight=1)
        Ab.rowconfigure(0,weight=1)
        Ab.rowconfigure(1,weight=5)
        Optionb(Ab)
        AboutI="""
        The Coronavirus Dashboard

Last updated: 13 May

This Coronavirus dashboard provides an overview of the 2019 Novel Coronavirus COVID-19 (2019-nCoV) epidemic. This dashboard is built with R using the Rmakrdown framework and can easily reproduce by others. The code behind the dashboard available here

Data

The input data for this dashboard is the coronavirus R package (dev version). The data and dashboard is refreshed on a daily bases. The raw data pulled from the Johns Hopkins University Center for Systems Science and Engineering (JHU CCSE) Coronavirus repository

Packages

Dashboard interface - the flexdashboard package.
Visualization - the plotly package for the plots and leaflet for the map
Data manipulation - dplyr, and tidyr
Tables - the DT package
Deployment and reproducibly

The dashboard was deployed to Github docs. If you wish to deploy and/or modify the dashboard on your Github account, you can apply the following steps:

Fork the dashboard repository, or
Clone it and push it to your Github package
Here some general guidance about deployment of flexdashboard on Github page - link
For any question or feedback, you can either open an issue or contact me on Twitter.

Contribution

The Map tab was contributed by Art Steinmetz on this pull request. Thanks Art!"""
        AbI=tk.Label(master=Ab,text=AboutI,fg="black",bg="white",font=("Baskerville Old Face",14))
        AbI.grid(row=1,column=0)


