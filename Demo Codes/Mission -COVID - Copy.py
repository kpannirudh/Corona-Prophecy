import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
import geopandas as gpd
#pr,pd,par,pad must vary for different age groups . n must depend upon no of available hosp beds,icu wards,etc.give apt values for R0start and R0end
from scipy.integrate import odeint
#x0 depends upon the lockdown period,c depends upon incubation period.also c must depend upon a few other env conditions if poss#
import numpy as np
import math
import csv
Path=r"C:\Users\Admin\Desktop\Corona Prophecy"
import sqlite3
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

def csv_to_mysql():
    mydb=sqlite3.connect(database=r"C:\Users\Admin\Desktop\Corona Prophecy\coronadata")
    mycursor=mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS HospitalBeds(State_UT char(60),NumPrimaryHealthCenters_HMIS integer,NumCommunityHealthCenters_HMIS integer,NumSubDistrictHospitals_HMIS integer,NumDistrictHospitals_HMIS integer,TotalPublicHealthFacilities_HMIS integer,NumPublicBeds_HMIS integers,NumRuralHospitals_NHP18 integer,NumRuralBeds_NHP18 integer, NumUrbanHospitals_NHP18 integer,NumUrbanBeds_NHP18 integer)")
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
    mycursor.close()
csv_to_mysql()

