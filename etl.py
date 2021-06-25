import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="",
	  database="DatawareHouse"
	)

print(mydb)
mycursor = mydb.cursor()
#return mycursor


def get_new_record():						##get new record for changing dimension
	dimension_table='Dim_table_timestamp'
	dimension_attr={'date_id':1,'date':'01.02.2019','day':'mon','month':'jan','year':'2019'}
	return dimension_table,dimension_attr

#pk=1
def select(table,pk):
	sql="SELECT sk_date_id FROM "+table +" WHERE  date_id=%s AND flag=%s"
	val=(pk,'1')
	mycursor.execute(sql,val)
	myresult = mycursor.fetchone()
	try:
		print myresult[0]
		return myresult[0]
	except:
		return None

#sk = select('Dim_table_timestamp',pk)	

def update(table,sk):
	now = datetime.now()
	dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
	sql = "UPDATE "+ table +" SET end_date=%s, flag=%s WHERE sk_date_id=%s" 
	val = (dt_string,'0',sk)
	mycursor.execute(sql, val)
	mydb.commit()

#update('Dim_table_timestamp',[],sk)

def insert(table,val,pk):
	now = datetime.now()
	dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
	l=[]; l.extend(dt_string); l[2]=str(int(l[2])+1); dt_string=''.join(l)
	sql = "INSERT INTO "+ table  +"VALUES (%s, %s, %s, %s, %s, %s, %s)"
	val = (pk, "27.05.2020",'wednesday','may','2020',dt_string,'1')
	mycursor.execute(sql, val)
	mydb.commit()

#insert('Dim_table_timestamp (date_id,date,day,month,year,end_date,flag)',[])

def find_dim(table):
	sql='select REFERENCED_TABLE_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA="DatawareHouse" AND TABLE_NAME="'+table+'"'
	#val=(table)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	print myresult
	return [i[0] for i in myresult]
#find_dim('Fact_table_Make_Booking')
def put_data(dim_sk,fact_attr,table='Fact_table_Make_Booking'):
	mycursor.execute("select sk_date_id from Dim_table_timestamp where date_id='"+str(dim_sk[1])+"' and flag='1'")
	sk1=mycursor.fetchone()[0]
	mycursor.execute("select sk_hotel_id from Dim_table_hotel where hotel_id='"+str(dim_sk[0])+"' and flag='1'")
	sk2=mycursor.fetchone()[0]
	fact_attr="'123','b123','mmt','CNF','12.45.67','34.23.12','5','15','456','678','10','cash'"
	table="Fact_table_Make_Booking(sk_date_id,sk_hotel_id,trip_id,booking_account,booking_website,booking_status,check_in_date,check_out_date,\
	number_of_nights,number_of_guests,additional_taxes,convenience_fees,discounts,mode_of_payment)"
	sql="insert into "+table+" values ('"+str(sk1)+"','"+str(sk2)+"',"+fact_attr+")"
	mycursor.execute(sql)
	mydb.commit()
	print(mycursor.rowcount)
#put_data([1,7],123)

def get_data(table_id):
	if table_id==0:
		table='Fact_table_Make_Booking'
		mycursor.execute("select * from "+table)
	elif table_id==1:
		table='Dim_table_hotel';table2='Sub_Dim_table_hotel_brand'
		mycursor.execute("select sk_hotel_id,hotel_id,t1.name,address,telephone,t2.name,country from "+table+" as t1 JOIN "+table2+" as t2")
	else:
		table='Dim_table_timestamp'
		mycursor.execute("select sk_date_id,date_id,date,day,month,year,start_date,end_date,flag from "+table)
	myresult=mycursor.fetchall()
	#print myresult
	return myresult
#get_data()

def csvtodb(text):
	#text=text.split('\n')[1:]
	import pandas
	import numpy as np
	df=pandas.read_csv('sample.csv')
	#print df.head()
	text=np.array(df)
	for data in text:
		#print (data)
		sql="insert into Source_timestamp values ('"+str(data[0])+"','"+data[1]+"','"+data[2]+"','"+data[3]+"','"+str(data[4])+"','"+data[5]+"','"+data[6]+"')";
		mycursor.execute(sql)
		mydb.commit()
	
def delete():
	now = datetime.now()
	dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
	year=dt_string.split('-')[0]
	mycursor.execute("select sk_date_id, end_date from Dim_table_timestamp")
	result=mycursor.fetchall()
	for row in result:
		if int(str(row[1]).split('-')[0])<=int(year)-5:
			mycursor.execute("delete from Dim_table_timestamp where sk_date_id="+str(row[0]))
			mydb.commit()
				
#delete()
#csvtodb('r')		
'''
mycursor.execute("SHOW TABLES")
for x in mycursor:
	print(x)
'''

#fact_table=['Fact_table_Make_Booking']
def extract():

	mycursor.execute("select date_id,date,day,month,year from Source_timestamp")
	result=mycursor.fetchall()
	for row in result:
		date_id,date,day,month,year=row
		mycursor.execute("select sk_date_id,date,day,month,year from Dim_table_timestamp where date_id="+str(date_id)+" and flag='1'")
		old_result=mycursor.fetchone()
		try:
			#print old_result
			sk,old_date,old_day,old_month,old_year=old_result
			if old_date!=date:
				#type 2
				now = datetime.now()
				dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
				mycursor.execute("update Dim_table_timestamp set end_date='"+dt_string+"' , flag='0' where sk_date_id="+str(sk) )
				mydb.commit()
				mycursor.execute("insert into Dim_table_timestamp(date_id,date,day,month,year,flag) values ("+str(date_id)+",'"+date+"','"+day+"','"+month+"','"+year+"','1')")
				mydb.commit()
			else:
				#type 1
				#pass
				
				mycursor.execute("update Dim_table_timestamp set day='"+day+"' , month='"+month+"' , year='"+year+"' where sk_date_id="+str(sk) )
				mydb.commit()
				
		except:
			#new entry
			print "new entry"
			mycursor.execute("insert into Dim_table_timestamp(date_id,date,day,month,year,flag) values ("+str(date_id)+",'"+date+"','"+day+"','"+month+"','"+year+"','1')")
			mydb.commit()
	#mydb.commit()
	mycursor.execute("update Source_timestamp set status='inactive'")
	mydb.commit()
#extract()

def csvtodb_hotel(text):
	import pandas
	import numpy as np
	df=pandas.read_csv('sample_hotel.csv')
	#print df.head()
	text=np.array(df)
	for data in text:
		#print (data)
		sql="insert into Source_hotel values ('"+str(data[0])+"','"+data[1]+"','"+data[2]+"','"+str(data[3])+"','"+str(data[6])+"','"+data[7]+"','"+data[4]+"','"+data[5]+"')";
		mycursor.execute(sql)
		mydb.commit()

def extract_hotel():
	mycursor.execute("select hotel_id,name,address,telephone,brand,country from Source_hotel")
	result=mycursor.fetchall()
	for row in result:
		hotel_id,name,address,telephone,brand,country=row
		telephone=str(telephone) 
		mycursor.execute("select sk_hotel_id,name,address,telephone,brand,country from Dim_table_hotel2 where hotel_id="+str(hotel_id)+" and flag='1'")
		old_result=mycursor.fetchone()
		try:
			#print old_result
			sk,old_name,old_address,old_telephone,old_brand,old_country=old_result
			print old_brand,brand
			if old_brand!=brand:
				#type 2
				now = datetime.now()
				dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
				mycursor.execute("update Dim_table_hotel2 set end_date='"+dt_string+"' , flag='0' where sk_hotel_id="+str(sk) )
				mydb.commit()
				mycursor.execute("insert into Dim_table_hotel2(hotel_id,name,address,telephone,brand,country,flag) values ("+str(hotel_id)+",'"+name+"','"+address+"','"+telephone+"','"+brand+"','"+country+"','1')")
				mydb.commit()
			else:
				#type 1
				#pass
				
				mycursor.execute("update Dim_table_hotel2 set name='"+name+"' , address='"+address+"' , telephone='"+telephone+"' , country='"+country+"' where sk_hotel_id="+str(sk) )
				mydb.commit()
				
		except Exception as e:
			print e
			#new entry
			print "new entry"
			mycursor.execute("insert into Dim_table_hotel2(hotel_id,name,address,telephone,brand,country,flag) values ("+str(hotel_id)+",'"+name+"','"+address+"','"+telephone+"','"+brand+"','"+country+"','1')")
			mydb.commit()

	mycursor.execute("update Source_hotel set status='inactive'")
	mydb.commit()
	
def select_hotel():
	mycursor.execute("select sk_hotel_id,hotel_id,name,address,telephone,brand,country,start_date,end_date,flag from Dim_table_hotel2")
	result=mycursor.fetchall()
	return result
