def delete_b(st):
    n=len(st)
    st1=""
    for i in range(0,n):
        if st[i]==',':
            pass
        else:
            st1+=st[i]
    return st1
from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
cnx=mysql.connector.connect(user="root",password="thearshia.g80",host='127.0.0.1',database='cars')
cursor=cnx.cursor()
q="INSERT INTO cars_detail VALUES(%s,%s,%s,%s,%s,%s,%s);"
print("Name of the car:")
print("Make = ",end="")
name_make=input()
print("Model = ",end="")
name_model=input()
sites=[]
price=[]
mile=[]
accident=[]
owner=[]
for j in range(1,6):
    site_c='https://www.truecar.com/used-cars-for-sale/listings/'+name_make+'/'+name_model+'/?/page='+str(j)+'&sort[]=best_match'
    sites.append(site_c)
for site in sites:
    r=requests.get(site)
    t=r.text
    soup=BeautifulSoup(t,'html.parser')
    resu_price=soup.find_all('',attrs={"class":"heading-3 margin-y-1 font-weight-bold","data-test":"vehicleCardPricingBlockPrice"})
    resu_mile=soup.find_all('',attrs={"class":"font-size-1 text-truncate", "data-test":"vehicleMileage"})
    resu_accident_owners_use=soup.find_all('',{"class":"vehicle-card-location font-size-1 margin-top-1", "data-test":"vehicleCardCondition", "data-qa":"ConditionHistory"})
    resu_color=soup.find_all('', {"class":"vehicle-card-location font-size-1 margin-top-1 text-truncate" ,"data-test":"vehicleCardColors" ,"data-qa":"ExteriorInteriorColor"})
    n=len(resu_price)
    for i in range(0,n):
        data_price=resu_price[i]
        data_now_price=data_price.text
        data_mile=resu_mile[i]
        data_now_mile=data_mile.text
        data_accident_owner_use=resu_accident_owners_use[i]
        data_now_accident_owner_use=data_accident_owner_use.text
        data_list=data_now_accident_owner_use.split()
        data_now_accident=data_list[0]
        if data_now_accident[0]=="N":
            data_now_accident='0'
        data_now_owner=data_list[2]
        data_now_use=data_list[4]
        data_color=resu_color[i]
        data_now_color=data_color.text
        data_list=data_now_color.split()
        data_now_color_exterior=data_list[0]
        data_now_color_interior=data_list[2]
        print("Mileage = ",data_now_mile," | ","Price = ",data_now_price," | ","Accidents = ",data_now_accident," | ","Owners = ",data_now_owner," | ","Use = ",data_now_use," | ","Exterior Color = ",data_now_color_exterior," | ","Interior Color = ",data_now_color_interior)
        data_final=(data_now_mile,data_now_price,data_now_accident,data_now_owner,data_now_use,data_now_color_exterior,data_now_color_interior)
        price.append(data_now_price)
        data_list=data_now_mile.split()
        mile.append(data_list[0])
        accident.append(data_now_accident)
        owner.append(data_now_owner)
        cursor.execute(q ,data_final)
print("DATA INSERTED TO DB TOO!")
cnx.commit()
cursor.close()
cnx.close()
#### ML begins
print("-- MACHINE LEARNING BEGINS NOW --")
price1=list(map(lambda x: x[1:],price))
price1=list(map(delete_b,price1))
mile=list(map(delete_b,mile))
from sklearn import tree
x=[]
y=[]
n=len(price)
for i in range(0,n):
    x1=[mile[i],accident[i],owner[i]]
    x.append(x1)
    y.append(price1[i])
clf=tree.DecisionTreeClassifier()
clf=clf.fit(x,y)
print("Mile = ",end="")
mile_new=input()
print("Accident = ",end="")
accident_new=input()
print("Owner = ",end="")
owner_new=input()
new_data=[mile_new,accident_new,owner_new]
answer=clf.predict([new_data])
print("ML prediction is that its worth $" , int(answer[0]))
