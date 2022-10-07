import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import geopandas as gpd
from prettytable import PrettyTable
#pr,pd,par,pad must vary for different age groups . n must depend upon no of available hosp beds,icu wards,etc.give apt values for R0start and R0end
from scipy.integrate import odeint
#x0 depends upon the lockdown period,c depends upon incubation period.also c must depend upon a few other env conditions if poss#
import numpy as np
import math
import csv
Path=r"C:\Users\Admin\Desktop\Corona Prophecy"
import mysql.connector
import urllib.request as request
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import json

def get_data_datewise():
    response=request.urlopen("https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise/history")
    cont=response.read()
    raw=json.loads(cont)
    data_datewise=[]
    for i in range(len(raw['data']['history'])) :
        d1={}
        d1['date']=raw['data']['history'][i]['day']
        d1['total']=raw['data']['history'][i]['total']
        x=raw['data']['history'][i]['statewise']
        for j in range(0,len(x)-1,1) :
            if x[j]['state']=='State Unassigned':
                x.pop(j)
        d1['statewise']=raw['data']['history'][i]['statewise']    
        data_datewise.append(d1)
    return data_datewise

def mysql_update():  #may take heck a lot of time due to ginormous data(about 10  mins in my system)

    mydb=mysql.connector.connect(host="localhost",port=3306,user="root",passwd="3.1415926535") 
    mycursor=mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS coronadata")
    mydb.close()
    mydb=mysql.connector.connect(host="localhost",port=3306,user="root",passwd="3.1415926535",database="coronadata") #user needs to give own credentials
    mycursor=mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS covid_india( Idate char(10),Iinfected integer,Irecovered integer,Iactive integer,Ideath integer)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS covid_statewise( Sdate char(10),Sname char(60) NOT NULL,Sinfected integer,Srecovered integer,Sactive integer,Sdeath integer)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS covid_ip( Sdate char(10),Sname char(60) NOT NULL,Sinfected integer,Srecovered integer,Sactive integer,Sdeath integer)")
    data=get_data_datewise()
    mycursor.execute("DELETE FROM covid_india;")
    mydb.commit()
    mycursor.execute("DELETE FROM covid_statewise;")
    mydb.commit()
    mycursor.execute("CREATE TABLE IF NOT EXISTS HospitalBeds(StateUT char(60),NumPrimaryHealthCentersHMIS integer,NumCommunityHealthCentersHMIS integer,NumSubDistrictHospitalsHMIS integer,NumDistrictHospitalsHMIS integer,TotalPublicHealthFacilitiesHMIS integer,NumPublicBedsHMIS integers,NumRuralHospitalsNHP18 integer,NumRuralBedsNHP18 integer, NumUrbanHospitalsNHP18 integer,NumUrbanBedsNHP18 integer)")
    csv_data = csv.reader(open(r'C:\Users\Admin\Desktop\Corona Prophecy\CSVFiles\HospitalBedsIndia.csv'))
    # execute and insert the csv into the database.
    temp=1
    for row in csv_data:
        print(row)
        del row[0]
        for i in range(len(row)):
            if row[i]=="":
                row[i]="NULL"
        TEM=tuple(row)
        print(TEM)
        sqlc="INSERT INTO HospitalBeds VALUES(\"{0[0]}\",{0[1]},{0[2]},{0[3]},{0[4]},{0[5]},{0[6]},{0[7]},{0[8]},{0[9]},{0[10]})".format(TEM)
        print(sqlc)
        if temp!=1:
            mycursor.execute(sqlc)
        temp+=1
    mydb.commit()
    for i in range(len(data)) :
        I=[]
        date=data[i]['date']
        Iinf=data[i]['total']['confirmed']
        Irecv=data[i]['total']['recovered']
        Iactv=data[i]['total']['active']
        Ideath=data[i]['total']['deaths']
        I.append(date)
        I.append(Iinf)
        I.append(Irecv)
        I.append(Iactv)
        I.append(Ideath)
        tI=tuple(I)
        for j in range(len(data[i]['statewise'])):
            if j!=1:
                S=[]
                Sname=data[i]['statewise'][j]['state']
                Sinf=data[i]['statewise'][j]['confirmed']
                Srecv=data[i]['statewise'][j]['recovered']
                Sactv=data[i]['statewise'][j]['active']
                Sdeath=data[i]['statewise'][j]['deaths']
                S.append(date)
                S.append(Sname)
                S.append(Sinf)
                S.append(Srecv)
                S.append(Sactv)
                S.append(Sdeath)
                tS=tuple(S)
                sqlcomm="INSERT INTO covid_statewise VALUES({0[0]},\"{0[1]}\",{0[2]},{0[3]},{0[4]},{0[5]})".format(tS)
                mycursor.execute(sqlcomm)
        sqlcomm1="INSERT INTO covid_india VALUES({0[0]},{0[1]},{0[2]},{0[3]},{0[4]})".format(tI)
        mycursor.execute(sqlcomm1)
        mydb.commit()
    mydb.close()

mysql_update()

def graphs_india() :
    t=input('Which data would you like to visualize? : ')#Confirmed or Active or Recovered or Deaths (as given,look out for upper case)
    t1=t.lower()
    data=get_data_datewise()
    x=[]
    y=[]
    for i in range(len(data)):
        tempx=data[i]['date']
        tempy=data[i]['total'][t1]
        x.append(tempx)
        y.append(tempy)
    plt.figure(figsize=(25,8))
    axes=plt.axes()
    axes.grid(linewidth=1,color='dimgray')
    axes.set_facecolor('ivory')
    axes.set_xlabel('\nDate',size=20,color='deepskyblue')
    axes.set_ylabel(t,size=20,color='deepskyblue')
    axes.xaxis.set_major_locator(ticker.MultipleLocator(7))
    plt.xticks(rotation=30,size=8,color='black')
    plt.yticks(size=15,color='black')
    plt.tick_params(size=9,color='black')

    #the below part of code(as comments) shows values on each date,but it looks clumsy due to too many values.Add it if you want to.It is pretty neat right now
    #for k in range(len(y)):
        #if k%2==0 :
            #H=(y[k])
            #axes.annotate(H,xy=(x[k],y[k]+50),color='black',size='7')
        #else :
            #axes.annotate((y[k]),xy=(x[k],y[k]-50),color='black',size='7')
    str='COVID 19 IN INDIA : '+ t +'\n'
    plt.title(str,size=40,color='black')
    axes.plot(x,y,color='cyan',marker='.',linewidth=2,markersize=8,markeredgecolor='cyan')
    plt.subplots_adjust(left=0.13,right=0.97,top=0.8,bottom=0.2)
    plt.show()
      
def graphs_state():
    s=input('Which state\'s data would you like to visualize? : ')#first letter of each word in state's name must be capitalized(watch out!)
    t=input('Which data would you like to visualize? : ')
    t1=t.lower()
    data=get_data_datewise()
    x=[]
    y=[]
    for i in range(len(data)):
        tempx=data[i]['date']
        for j in range(len(data[i]['statewise'])) :   
            if data[i]['statewise'][j]['state']==s :
                tempy=data[i]['statewise'][j][t1]
        x.append(tempx)
        y.append(tempy)
    plt.figure(figsize=(25,8))
    axes=plt.axes()
    axes.grid(linewidth=1,color='dimgray')
    axes.set_facecolor('ivory')
    axes.set_xlabel('\nDate',size=20,color='deepskyblue')
    stry=t+'\t'
    axes.set_ylabel(stry,size=20,color='deepskyblue')
    axes.xaxis.set_major_locator(ticker.MultipleLocator(7))
    plt.xticks(rotation=30,size=8,color='black')
    plt.yticks(size=15,color='black')
    plt.tick_params(size=9,color='black')

    #the below part of code(as comments) shows values on each date,but it looks clumsy due to too many values.Add it if you want to.It is pretty neat right now
    #for k in range(len(y)):
        #if k%2==0 :
           #axes.annotate(str(y[k]),xy=(x[k],y[k]+50),color='black',size='7')
        #else :
            #axes.annotate(str(y[k]),xy=(x[k],y[k]-50),color='black',size='7')
    str='COVID 19 IN '+s+ ':' + t
    plt.title(str,size=40,color='black')
    axes.plot(x,y,color='cyan',marker='.',linewidth=2,markersize=8,markeredgecolor='cyan')
    plt.subplots_adjust(left=0.13,right=0.97,top=0.9,bottom=0.13)
    plt.show()

def piechart_india():
    t=input('Which data would you like to visualize? : ')
    t1=t.lower()
    data1=get_data_datewise()
    data=data1[len(data1)-1]
    tot=data['total'][t1]
    slices=[]
    labels=[]
    exp=[]
    rest=0
    for i in range(len(data['statewise'])):
        if ((data['statewise'][i][t1])/tot)*100>3 :            
            templ=data['statewise'][i]['state']
            labels.append(templ)
            temps=data['statewise'][i][t1]
            slices.append(temps)
        else :
            rest=rest+data['statewise'][i][t1]
    slices.append(rest)
    labels.append('Other States')
    for i in range(len(slices)):
        exp.append(0.05)
    
    plt.pie(slices,labels=labels,textprops=dict(size=10,color='black'),radius=1.3,autopct='%2.2f%%',explode=exp,shadow=False,startangle=90)
    str1='Share of each State in India : '+t+'\n\n'
    plt.title(str1,color='black',size=13)
    plt.show()

def piechart_state():
    s=input('Which state\'s data would you like to visualize? : ')#first letter of each word in state's name must be capitalized(watch out!)
    data1=get_data_datewise()
    data=data1[len(data1)-1]
    slices=[]
    labels=['Active','Recovered','Deaths']
    for i in range(len(data['statewise'])):
        if data['statewise'][i]['state']==s:
            confirmed=str(data['statewise'][i]['confirmed'])
            slices.append(data['statewise'][i]['active'])
            slices.append(data['statewise'][i]['recovered'])
            slices.append(data['statewise'][i]['deaths'])
            break
    exp=[]
    for i in range(len(slices)):
        exp.append(0.05)        

    plt.pie(slices,labels=labels,textprops=dict(size=10,color='black'),radius=1.3,autopct='%2.2f%%',explode=exp,shadow=False,startangle=90)
    str1='Status of the '+confirmed+' Confirmed cases in '+s+'\n\n\n'
    plt.title(str1,color='black',size=15)
    plt.subplots_adjust(left=0.13,right=0.9,top=0.8,bottom=0.3)
    plt.show()    
    plt.show()    

def barchart():
    t=input('Which data would you like to visualize? : ')
    t1=t.lower()
    data1=get_data_datewise()
    data=data1[len(data1)-1]
    states=[]
    num=[]
    for i in range(len(data['statewise'])) :
        s=data['statewise'][i]['state']
        states.append(s)
        y=data['statewise'][i][t1]
        num.append(y)
    x=[]
    for i in range(1,len(num)+1):
        x.append(i)
    plt.figure(figsize=(100,10))    
    axes=plt.axes()    
    plt.bar(x,num,tick_label=states,width=0.75,color='red')
    locator={'deaths':500,'confirmed':10000,'recovered':10000,'active':5000}
    axes.yaxis.set_major_locator(ticker.MultipleLocator(locator[t1]))
    plt.ylabel('Number of Cases',size=20)
    plt.xticks(rotation='vertical',size=8,color='black')
    plt.yticks(size=10,color='black')
    str='COVID 19 IN INDIA : '+ t +'\n'
    plt.title(str,size=20,color='black')
    plt.subplots_adjust(left=0.13,right=0.9,top=0.85,bottom=0.3)
    plt.show()    

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

