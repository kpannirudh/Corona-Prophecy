import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import pandas as pd
import geopandas as gpd
from scipy.integrate import odeint
import numpy as np
import math
import csv
Path=r"C:\Users\Admin\Desktop\Corona Prophecy"
import mysql.connector
import urllib.request as request
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import json
import threading
from datetime import date

highConf=""
highDeath=""
highRec=""
inf=0
rec=0
dea=0

def mysqltopd(TabName,Constraint, db_connection):
    df = pd.read_sql('SELECT * FROM {} where {}'.format(TabName,Constraint), con=db_connection)
    df.head()
    return df

def piechart_state(slices,Title): 
    labels=['Active','Recovered','Deaths']
    exp=[]
    for i in range(len(slices)):
        exp.append(0.05)        

    plt.pie(slices,labels=labels,textprops=dict(size=13,color='black'),radius=1,autopct='%2.2f%%',explode=exp,shadow=False,startangle=90)
    str1='Status of the '+str(slices[0]+slices[1]+slices[2])+' Confirmed cases in '+Title+'\n\n\n'
    plt.title(str1,color='black',size=15)
    plt.subplots_adjust(left=0.13,right=0.9,top=0.8,bottom=0.3)
    plt.savefig("{}\Pie chart of {}.png".format(Path,Title),bbox_inches='tight', dpi=200)
    plt.clf()
    
def showmapAI(show_data,ToCompare,CoCo,Title):
    map_data = gpd.read_file('Indian_States.shp')
    map_data.rename(columns = {'st_nm':'Sname'}, inplace = True)
    map_data['Sname'] = map_data['Sname'].str.replace('&','and')
    map_data['Sname'].replace('Arunanchal Pradesh',
                                  'Arunachal Pradesh', inplace = True)
    #map_data['Sname'].replace('Telangana', 'Telengana', inplace = True)
    map_data['Sname'].replace('NCT of Delhi', 
                                  'Delhi', inplace = True)
    map_data['Sname'].replace('Andaman and Nicobar Island', 
                                  'Andaman and Nicobar Islands', 
                                   inplace = True)
    #show_data[ToCompare] = show_data[ToCompare].map(int)
    merged = pd.merge(map_data, show_data, on='Sname')
    merged.head()

    fig, ax = plt.subplots(1, figsize=(13, 12))
    ax.axis('off')

    ax.set_title(Title, fontsize=25)
    merged.plot(column =ToCompare,cmap=CoCo, linewidth=0.8, ax=ax, edgecolor='0.8', legend = True)
    fig.tight_layout()
    fig.savefig("{}\{}.png".format(Path,Title), dpi=100)
    plt.clf()
    
def load_scr():
    global inf,rec,dea,highConf, highDeath, highRec,HConf, HRec, HDeath
    loads=tk.Tk()
    loads.configure(bg='white')
    loads.geometry("500x220")
    loads.title("CoronaVirus Prophecy - Loading....")
    Percent=tk.Label(master=loads,text="0%",fg="black",bg="white",font=("Baskerville Old Face",14))
    Percent.pack()
    Info=tk.Label(master=loads,text="Loading Data from API! Please Wait...",fg="black",bg="white",font=("Baskerville Old Face",14))
    Info.pack()
    Opimg = Image.open(r"C:\Users\Admin\Desktop\Corona Prophecy\Logo.jpg")
    Opimg=Opimg.resize((450,200), Image.ANTIALIAS)
    Opimg = ImageTk.PhotoImage(Opimg)
    Opimg1=tk.Label(image=Opimg)
    Opimg1.pack()
    def mysql_update():
        global inf, rec, dea, highConf, highDeath, highRec,HConf, HRec, HDeath
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
        for i in range(len(data)) :
                I=[]
                Percent['text']=(str(round((i+1)*50/(len(data)),2)))+"%"
                DATE=data[i]['date']
                Iinf=data[i]['total']['confirmed']
                Irecv=data[i]['total']['recovered']
                Iactv=data[i]['total']['active']
                Ideath=data[i]['total']['deaths']
                I.append(DATE)
                I.append(Iinf)
                I.append(Irecv)
                I.append(Iactv)
                I.append(Ideath)
                tI=tuple(I)
                for j in range(len(data[i]['statewise'])):
                    S=[]
                    Sname=data[i]['statewise'][j]['state']
                    Sinf=data[i]['statewise'][j]['confirmed']
                    Srecv=data[i]['statewise'][j]['recovered']
                    Sactv=data[i]['statewise'][j]['active']
                    Sdeath=data[i]['statewise'][j]['deaths']
                    S.append(DATE)
                    S.append(Sname)
                    S.append(Sinf)
                    S.append(Srecv)
                    S.append(Sactv)
                    S.append(Sdeath)
                    tS=tuple(S)
                    sqlcomm="INSERT INTO covid_statewise VALUES(\"{0[0]}\",\"{0[1]}\",{0[2]},{0[3]},{0[4]},{0[5]})".format(tS)
                    mycursor.execute(sqlcomm)
                sqlcomm1="INSERT INTO covid_india VALUES(\"{0[0]}\",{0[1]},{0[2]},{0[3]},{0[4]})".format(tI)
                mycursor.execute(sqlcomm1)
                mydb.commit()
        mydb.close()
        mydb=mysql.connector.connect(host="localhost",port=3306,user="root",passwd="3.1415926535",database="coronadata") #user needs to give own credentials
        mycursor=mydb.cursor()
        today = date.today()
        dat = today.strftime("%Y-%m-%d")
        showmapAI(show_data=mysqltopd("covid_statewise","Sdate=\"{}\"".format(dat),mydb),ToCompare="Sinfected",CoCo="inferno_r",Title="Confirmed COVID Cases")
        Percent['text']="75.00%"
        file=mysqltopd("covid_india","Idate=\"{}\"".format(dat),mydb)
        for index, rows in file.iterrows(): 
            my_list =[rows.Iactive, rows.Irecovered, rows.Ideath]
        piechart_state(my_list,"India")
        Percent['text']="100.00%"
        mycursor.execute("SELECT Sname, Sinfected from covid_statewise where Sinfected=(SELECT MAX(Sinfected) from covid_statewise) and Sdate=\"{}\"".format(dat))
        read=mycursor.fetchall()
        highConf=read[0][0]
        HConf=int(read[0][1])
        mycursor.execute("SELECT Sname, Sdeath from covid_statewise where Sdeath=(SELECT MAX(Sdeath) from covid_statewise) and Sdate=\"{}\"".format(dat))
        read=mycursor.fetchall()
        highDeath=read[0][0]
        HDeath=int(read[0][1])
        mycursor.execute("SELECT Sname,Srecovered from covid_statewise where Srecovered=(SELECT MAX(Srecovered) from covid_statewise) and Sdate=\"{}\"".format(dat))
        read=mycursor.fetchall()
        highRec=read[0][0]
        HRec=int(read[0][1])
        mycursor.execute("SELECT Iinfected from covid_india where Idate=\"{}\"".format(dat))
        read=mycursor.fetchall()
        inf=int(read[0][0])
        mycursor.execute("SELECT Ideath from covid_india where Idate=\"{}\"".format(dat))
        read=mycursor.fetchall()
        dea=int(read[0][0])
        mycursor.execute("SELECT Irecovered from covid_india where Idate=\"{}\"".format(dat))
        read=mycursor.fetchall()
        rec=int(read[0][0])
        loads.destroy()
        homescr()
    timer1=threading.Timer(2.0,mysql_update)
    timer1.start()
    loads.mainloop()
    
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
        Toggleb.columnconfigure([0,1,2,3,4,5],weight=1)
        Toggleb.rowconfigure(0,weight=1)
        Inf = Image.open(r"{}\Infected.jpg".format(Path))
        Inf=Inf.resize((260,135), Image.ANTIALIAS)
        Inf = ImageTk.PhotoImage(Inf)
        Infe=tk.Label(master=Toggleb,image=Inf,bg="white")
        Infe.grid(row=0, column=0,sticky="nsew")
        InfeI=tk.Label(master=Toggleb,text=str(inf),fg="black",bg="white",font=("Baskerville Old Face",32))
        InfeI.grid(row=0,column=1,sticky="nsew")
        Death = Image.open(r"{}\Deaths.jpg".format(Path))
        Death=Death.resize((270,135), Image.ANTIALIAS)
        Death = ImageTk.PhotoImage(Death)
        Deathe=tk.Label(master=Toggleb,image=Death,bg="white")
        Deathe.grid(row=0,column=2,sticky="nsew")
        DeatheI=tk.Label(master=Toggleb,text=str(dea),fg="black",bg="white",font=("Baskerville Old Face",32))
        DeatheI.grid(row=0,column=3,sticky="nsew")
        Rec = Image.open(r"{}\Recovered.jpg".format(Path))
        Rec=Rec.resize((280,135), Image.ANTIALIAS)
        Rec = ImageTk.PhotoImage(Rec)
        Reco=tk.Label(master=Toggleb,image=Rec,bg="white")
        Reco.grid(row=0,column=4,sticky="nsew")
        RecoI=tk.Label(master=Toggleb,text=str(rec),fg="black",bg="white",font=("Baskerville Old Face",32))
        RecoI.grid(row=0,column=5,sticky="nsew")
        Toggleb.grid(row=1,column=0,sticky="nsew")
        PFrame=tk.Frame(master=home,relief=tk.RAISED, width=home.winfo_screenwidth(), height=int(home.winfo_screenheight())/2,bg='white')
        PFrame.rowconfigure(0,weight=1)
        PFrame.columnconfigure(0,weight=1)
        PFrame.columnconfigure([1,2],weight=2)
        Map = Image.open(r"{}\Confirmed COVID Cases.png".format(Path))
        Map=Map.resize((500,500), Image.ANTIALIAS)
        Map = ImageTk.PhotoImage(Map)
        Mapr=tk.Label(master=PFrame,image=Map,bg="white")
        Mapr.grid(row=0,column=2,sticky="nsew")
        Map1 = Image.open(r"{}\Pie chart of India.png".format(Path))
        Map1=Map1.resize((450,500), Image.ANTIALIAS)
        Map1 = ImageTk.PhotoImage(Map1)
        Mapr1=tk.Label(master=PFrame,image=Map1,bg="white")
        Mapr1.grid(row=0,column=1,sticky="nsew")
        AFrame=tk.Frame(master=PFrame,relief=tk.RAISED, width=(home.winfo_screenwidth())/7, height=int(home.winfo_screenheight())/2,bg='black')
        AFrame.rowconfigure([0,1,2],weight=1)
        AFrame.columnconfigure(0,weight=1)
        HighC=tk.Label(master=AFrame,borderwidth=3,text="Highest"+"\n"+"Confirmed Cases -"+"\n"+highConf+"\n("+str(HConf)+")",fg="white",bg="Red",font=("Baskerville Old Face",16))
        HighD=tk.Label(master=AFrame,borderwidth=3,text="Highest"+"\n"+"Deaths -"+"\n"+highDeath+"\n("+str(HDeath)+")",fg="white",bg="grey",font=("Baskerville Old Face",16))
        HighR=tk.Label(master=AFrame,borderwidth=3,text="Highest"+"\n"+"Recovered -"+"\n"+highRec+"\n("+str(HRec)+")",fg="white",bg="green",font=("Baskerville Old Face",16))
        HighC.grid(row=0,column=0,sticky="nsew")
        HighD.grid(row=1,column=0,sticky="nsew")
        HighR.grid(row=2,column=0,sticky="nsew")
        AFrame.grid(row=0,column=0,sticky="nsew")
        PFrame.grid(row=2,column=0,sticky="nsew")
        home.mainloop()

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


load_scr()




