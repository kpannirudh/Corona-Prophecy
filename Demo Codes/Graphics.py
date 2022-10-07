import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import geopandas as gpd
from prettytable import PrettyTable
import matplotlib.pyplot as plt  #pr,pd,par,pad must vary for different age groups . n must depend upon no of available hosp beds,icu wards,etc.give apt values for R0start and R0end
from scipy.integrate import odeint#x0 depends upon the lockdown period,c depends upon incubation period.also c must depend upon a few other env conditions if poss#
import numpy as np
import math
import csv
Path=r"C:\Users\Admin\Desktop\Corona Prophecy"

def Temp1(Input,DATE):
        L=[]
        with open(r"C:\Users\Admin\Desktop\Corona Prophecy\CSVFiles\{}".format(Input),mode='r') as dem1:
                read=csv.reader(dem1)
                i=1
                for row in read:
                        if i==1:
                                L.append(row)
                        i=i+1
                        print(row)
                        if row[0]==DATE:
                                L.append(row)
        with open(r"C:\Users\Admin\Desktop\Corona Prophecy\CSVFiles\TempCSV.csv",mode='w') as dem2:
                writer=csv.writer(dem2)
                writer.writerows(L)                       
        df1=pd.read_csv(r"C:\Users\Admin\Desktop\Corona Prophecy\CSVFiles\TempCSV.csv")
        df1.head()
        print(df1)
        return df1

def showmapAI(show_data,ToCompare,CoCo,Title):
    #function to display map with the given data.. parameters: list with columns "Sr.No", "States/UT","Active","Recovered","Deceased","Total"
    map_data = gpd.read_file('Indian_States.shp')
    
    map_data.rename(columns = {'st_nm':'States/UT'}, inplace = True)

    map_data['States/UT'] = map_data['States/UT'].str.replace('&','and')
    map_data['States/UT'].replace('Arunanchal Pradesh',
                                  'Arunachal Pradesh', inplace = True)
    map_data['States/UT'].replace('Telangana', 
                                  'Telengana', inplace = True)
    map_data['States/UT'].replace('NCT of Delhi', 
                                  'Delhi', inplace = True)
    map_data['States/UT'].replace('Andaman and Nicobar Island', 
                                  'Andaman and Nicobar Islands', 
                                   inplace = True)

    show_data[ToCompare] = show_data[ToCompare].map(int)

    merged = pd.merge(map_data, show_data, on='States/UT')
    merged.head()

    fig, ax = plt.subplots(1, figsize=(13, 12))
    ax.axis('off')

    ax.set_title(Title, fontsize=25)
    merged.plot(column =ToCompare,cmap=CoCo, linewidth=0.8, ax=ax, edgecolor='0.8', legend = True)
    fig.savefig("{}.png".format(Title), dpi=100)

def Optionb(root):
        global Titimg, himg, Proph, Stats, Abo
        Titimg = Image.open(r"{}\Titlelogo.jpg".format(Path))
        Titimg=Titimg.resize((300,100), Image.ANTIALIAS)
        Titimg = ImageTk.PhotoImage(Titimg)
        himg = Image.open(r"{}\Home.jpg".format(Path))
        himg=himg.resize((180,60), Image.ANTIALIAS)
        himg = ImageTk.PhotoImage(himg)
        Proph = Image.open(r"{}\Prophecy.jpg".format(Path))
        Proph=Proph.resize((185,60), Image.ANTIALIAS)
        Proph = ImageTk.PhotoImage(Proph)
        Stats = Image.open(r"{}\Stats.jpg".format(Path))
        Stats=Stats.resize((185,60), Image.ANTIALIAS)
        Stats = ImageTk.PhotoImage(Stats)
        Abo= Image.open(r"{}\About.jpg".format(Path))
        Abo=Abo.resize((180,60), Image.ANTIALIAS)
        Abo= ImageTk.PhotoImage(Abo)
        Optionb=tk.Frame(master=root,relief=tk.RAISED, width=int(root.winfo_screenwidth())/2, height=int(root.winfo_screenheight())/10,bg="Royalblue")
        Title=tk.Label(master=Optionb,text="Corona Prophecy",fg="white",bg="Royalblue1",borderwidth=0,font=("Baskerville Old Face",32),image=Titimg)
        Title.pack(side=tk.LEFT, fill=tk.X,padx=(0,10))
        BHome=tk.Button(master=Optionb,image=himg,borderwidth=0,command=lambda:[root.destroy(),homescr()])
        BHome.pack(side=tk.LEFT,fill=tk.X,pady=10)
        BStats=tk.Button(master=Optionb,image=Stats,borderwidth=0,command=lambda:[root.destroy(),Statsscr()])
        BStats.pack(side=tk.LEFT,fill=tk.X,padx=50,pady=10)        
        BSIR=tk.Button(master=Optionb,image=Proph,borderwidth=0,command=lambda:[root.destroy(),SIRscr()])
        BSIR.pack(side=tk.LEFT,fill=tk.X,padx=(0,50),pady=10)
        BAbout=tk.Button(master=Optionb,image=Abo,borderwidth=0,command=lambda:[root.destroy(),Aboutscr()])
        BAbout.pack(side=tk.LEFT,fill=tk.X,padx=(0,150),pady=10)
        Optionb.grid(row=0, column=0)
        
def homescr():
        home=tk.Tk()
        home.configure(bg='white')
        home.title("CoronaVirus Prophecy - Home")
        home.columnconfigure(0,weight=1)
        home.rowconfigure([0,1],weight=1)
        home.rowconfigure(2,weight=3)
        Optionb(home)
        Toggleb=tk.Frame(master=home,relief=tk.RAISED, width=home.winfo_screenwidth(), height=int(home.winfo_screenheight())/10,bg='white')
        Inf = Image.open(r"{}\Infected.jpg".format(Path))
        Inf=Inf.resize((260,135), Image.ANTIALIAS)
        Inf = ImageTk.PhotoImage(Inf)
        Infe=tk.Label(master=Toggleb,image=Inf)
        Infe.pack(side=tk.LEFT)
        InfeI=tk.Label(master=Toggleb,text="9,10,100",fg="black",bg="white",font=("Baskerville Old Face",32))
        InfeI.pack(side=tk.LEFT, fill=tk.X,padx=(10,10))
        Death = Image.open(r"{}\Deaths.jpg".format(Path))
        Death=Death.resize((270,135), Image.ANTIALIAS)
        Death = ImageTk.PhotoImage(Death)
        Deathe=tk.Label(master=Toggleb,image=Death)
        Deathe.pack(side=tk.LEFT)
        DeatheI=tk.Label(master=Toggleb,text="9,10,100",fg="black",bg="white",font=("Baskerville Old Face",32))
        DeatheI.pack(side=tk.LEFT, fill=tk.X,padx=(10,10))
        Rec = Image.open(r"{}\Recovered.jpg".format(Path))
        Rec=Rec.resize((280,135), Image.ANTIALIAS)
        Rec = ImageTk.PhotoImage(Rec)
        Reco=tk.Label(master=Toggleb,image=Rec)
        Reco.pack(side=tk.LEFT)
        RecoI=tk.Label(master=Toggleb,text="9,10,100",fg="black",bg="white",font=("Baskerville Old Face",32))
        RecoI.pack(side=tk.LEFT, fill=tk.X,padx=(10,0))
        Toggleb.grid(row=1,column=0)
        showmapAI(show_data=Temp1("StatewiseTestingDetails.csv",DATE="22-04-2020"),ToCompare="TotalSamples",CoCo="PuBuGn",Title="State Testings")
        PFrame=tk.Frame(master=home,relief=tk.RAISED, width=home.winfo_screenwidth(), height=int(home.winfo_screenheight())/2,bg='white')
        Map = Image.open(r"C:\Users\Admin\Desktop\State Testings.png")
        Map=Map.resize((500,500), Image.ANTIALIAS)
        Map = ImageTk.PhotoImage(Map)
        Mapr=tk.Label(master=PFrame,image=Map)
        Mapr.pack(fill=tk.BOTH,side=tk.RIGHT)
        Map1 = Image.open(r"{}\State_wise.png".format(Path))
        Map1=Map1.resize((500,500), Image.ANTIALIAS)
        Map1 = ImageTk.PhotoImage(Map1)
        Mapr1=tk.Label(master=PFrame,image=Map1)
        Mapr1.pack(fill=tk.BOTH,side=tk.RIGHT)
        PFrame.grid(row=2,column=0)
        home.mainloop()

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

def Statsscr():
        sta=tk.Tk()
        sta.configure(bg='white')
        sta.title("CoronaVirus Prophecy - About")
        sta.columnconfigure(0,weight=1)
        sta.rowconfigure(0,weight=1)
        sta.rowconfigure(1,weight=5)
        Optionb(sta)

def SIRscr():
        global SIR
        SIR=tk.Tk()
        SIR.configure(bg='white')
        SIR.title("CoronaVirus Prophecy - About")
        SIR.columnconfigure(0,weight=1)
        SIR.rowconfigure(0,weight=1)
        SIR.rowconfigure(1,weight=5)
        Optionb(SIR)
        
homescr()

