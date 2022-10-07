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
            print(tS)
            sqlcomm="INSERT INTO covid_statewise VALUES(\"{0[0]}\",\"{0[1]}\",{0[2]},{0[3]},{0[4]},{0[5]})".format(tS)
            print(sqlcomm)
            mycursor.execute(sqlcomm)
        sqlcomm1="INSERT INTO covid_india VALUES(\"{0[0]}\",{0[1]},{0[2]},{0[3]},{0[4]})".format(tI)
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


        
                   


                
    
    
    
        
        
        
    
    


    
        
        
            
            
            
        
        
        
        
    

    
    
    
    
    


