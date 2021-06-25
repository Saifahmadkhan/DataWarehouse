import pyodbc
from tkinter import *
#import tkMessageBox as tmsg
import random
from PIL import Image ,ImageTk

con=pyodbc.connect('Driver={SQL SERVER};''Server=LAPTOP-DGTV8FKG;''Database=Minor_deadline1;' 'Trusted_Connection=yes;')
cursor = con.cursor()




def first_page():
	def f1(root):
		root.destroy()
		second_page()
	root=Tk()
	root.configure(background="slategray4",pady=20)
	root.geometry("1400x1300")
	x=StringVar();x.set("SELECT HOTEL FOR BUSINESS TRIP")
	lab=Label(root,text=x.get(),font=('Courier new',30,'bold'),fg="Maroon")
	lab.pack(side=TOP)
	load=Image.open("front")
	resize=load.resize((800,520),Image.ANTIALIAS)
	render=ImageTk.PhotoImage(resize)
	i=Label(root,image=render)
	i.place(x=280,y=60)
	b_hr_regis=Button(root,text="Go To Decisions",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="black",width=50,height=3,command=lambda:f1(root)).place(x=500,y=620)
	#cgpa=StringVar();cgpa.set('saif')
	#Entry(root,textvar=cgpa,bd=5,width=55).place(x=1190,y=150)
	root.mainloop()

def second_page():
	global cursor;
	cursor.execute("SELECT * FROM decision")
	rows = cursor.fetchall()
	tt=rows[0][1]
	root=Tk()
	root.geometry("1400x1300")
	root.configure(background='slategray4',pady=20)
	root.title("DECISION")
	#lab=Label(root,text="DECISION",height=3,width=20,font=('Courier new',30,'bold'),fg="Maroon").place(x=400,y=100)
	#lab.pack()
	load=Image.open("des.jpg")
	resize=load.resize((800,520),Image.ANTIALIAS)
	render=ImageTk.PhotoImage(resize)
	i=Label(root,image=render)
	i.image=render
	i.place(x=280,y=30)

	mybutton= Button(root,text=tt,width=40,height=3,font=('Courier new',10,'bold'),command=lambda:Options_Available(root),fg="cyan",bg="black").place(x=500,y=600)
	

	#mybutton.pack()
	root.mainloop()
	
	

	
def Options_Available(r):
	r.destroy()

	global cursor;
	def objective():
		def f2(root):
			obj=add_obj.get();att=add_att.get(); obv=edit_obv.get();
			att_list=att.split(',');typei=edit_type.get(); parent=edit_parent.get()
			
			if obj=='' or obj=='add new object name' or obv=='' or obv=='add new objective' or att=='' or att=='enter attribute name of object':
				print ("hello")
				print (obj); print (obv);print (att)
				return
			if typei=='' or typei=='objective type' or parent=='' or parent=='parent objective id':
				print ("hell")
				return

			####
			#put objective in objective table and (decision_objective). put object in object_table
			####
			cursor.execute('select * from object')
			rows=cursor.fetchall()
			obj_row=len(rows)+1
			
			
			cursor.execute("insert into object(object_id,name,action_id) values (?,?,?)",obj_row,obj,1)
			con.commit()
			cursor.execute('select * from objective')
			rows1=cursor.fetchall()			
			obv_row=len(rows1)+1		
			cursor.execute("insert into objective values (?,?,?,?,?)",obv_row,typei,obv,obj_row,parent)
			con.commit()
			cursor.execute("select * from attribute")
			rows=cursor.fetchall()
			iii=len(rows)+1
			for i in range(0,len(att_list)):
				try:
					cursor.execute("insert into attribute(attribute_id,name,value,object_id) values (?,?,?,?)",iii,att_list[i],'',obj_row)
					con.commit()
				except:
					break
				
				iii+=1	
			cursor.execute("insert into decision_objective(decision_id,objective_id) values (?,?)",1,obv_row)
			con.commit()
			print(obj);print(att_list);print(obv);
			root.destroy()
			objective()

		def f11(event,root):
			idxs=listbox2.curselection()
			if len(idxs)==1:
				idx=idxs[0]
				obj_id=all_objects[idx][0]
				root.destroy()
				object_description(obj_id)
		root = Tk()
		root.geometry("1400x1300")
		root.configure(background="slategray4",pady=20)
		x=StringVar();x.set("OBJECTIVES")
		lab=Label(root,text=x.get(),font=('Courier new',30,'bold'),fg="Maroon")
		lab.pack(side=TOP)
		#############
		#fetch all objectives from objective table. Get object_id separately for querying into object table afterwards
		cursor.execute("select * from objective")
		rows=cursor.fetchall()
		all_objectives=[]; object_ids=[]; all_objects=[]
		for row in rows:
			all_objectives.append([row[0],row[1],row[2],row[4]])
			object_ids.append(row[3])
		#######################
		#############
		#fetch object by using object_id
		for i in range(len(object_ids)):
			cursor.execute('SELECT * FROM object where object_id=?',object_ids[i])
			rows=cursor.fetchall()
			for row in rows:
				all_objects.append([row[0],row[1]])
		#############	
		lab=Label(root,text="Objectives",font=('Courier new',20,'bold'),fg="Maroon"); lab.place(x=180,y=50)
		lab=Label(root,text="Id",font=('Courier new',10,'bold'),fg="Maroon"); lab.place(x=90,y=130)
		lab=Label(root,text="Type",font=('Courier new',10,'bold'),fg="Maroon"); lab.place(x=130,y=130)
		lab=Label(root,text="Name",font=('Courier new',10,'bold'),fg="Maroon"); lab.place(x=180,y=130)
		lab=Label(root,text="Parent id",font=('Courier new',10,'bold'),fg="Maroon"); lab.place(x=240,y=130)

		
		listbox1 = Listbox(root,bg="light grey",font=("Times",15),selectbackground="white",height=20,width=35)
		scrollbar1 = Scrollbar(root, orient=VERTICAL, command=listbox1.yview)
		scrollbar1.place(x=430,y=180,height=464,width=15)
		listbox1.configure(yscrollcommand=scrollbar1.set)
		#listbox1.bind('<<ListboxSelect>>',lambda event:f11(event,root))
		listbox1.place(x=80,y=180)
		for i in range(len(all_objectives)):
			listbox1.insert(i,str(all_objectives[i][0])+"    "+str(all_objectives[i][1])+"    "+str(all_objectives[i][2])+"   "+str(all_objectives[i][3]))
		####
		lab=Label(root,text="Objects",font=('Courier new',20,'bold'),fg="Maroon"); lab.place(x=1000,y=50);
		#lab=Label(root,text="Id",font=('Courier new',10,'bold'),fg="Maroon"); lab.place(x=905,y=130)
		lab=Label(root,text="Id",font=('Courier new',10,'bold'),fg="Maroon"); lab.place(x=905,y=130)
		lab=Label(root,text="Name",font=('Courier new',10,'bold'),fg="Maroon"); lab.place(x=950,y=130)
		
		listbox2 = Listbox(root,bg="light grey",font=("Times",15),selectbackground="white",height=20,width=35)
		scrollbar2 = Scrollbar(root, orient=VERTICAL, command=listbox2.yview)
		scrollbar2.place(x=1250,y=180,height=464,width=15)
		listbox2.configure(yscrollcommand=scrollbar2.set)
		listbox2.place(x=900,y=180)
		listbox2.bind('<<ListboxSelect>>',lambda event:f11(event,root))
		for i in range(len(all_objects)):
			listbox2.insert(i,str(all_objects[i][0])+"    "+str(all_objects[i][1]))
			
		
		new_obv=StringVar(); new_obv.set('add new objective'); obv_type=StringVar(); obv_type.set('objective type'); 
		parent_obv=StringVar(); parent_obv.set('parent objective id');
		new_obj=StringVar(); new_obj.set('add new object name'); att_obj=StringVar(); att_obj.set('enter attribute name of object');
		
		edit_obv=Entry(root,bd=5,width=55); edit_obv.place(x=510,y=230); edit_obv.insert(0,new_obv.get())
		edit_type=Entry(root,bd=5,width=55); edit_type.place(x=510,y=280); edit_type.insert(0,obv_type.get())
		edit_parent=Entry(root,bd=5,width=55); edit_parent.place(x=510,y=330); edit_parent.insert(0,parent_obv.get())
		add_obj=Entry(root,bd=5,width=55); add_obj.place(x=510,y=380); add_obj.insert(0,new_obj.get())
		add_att=Entry(root,bd=5,width=55); add_att.place(x=510,y=430); add_att.insert(0,att_obj.get())
		
		add=Button(root,text="ADD OBJECT",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="black",width=40,height=3,command=lambda:f2(root)).place(x=534,y=500)
		button=Button(root,text="Main Page",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:Options_Available(root))
		button.pack(side=BOTTOM)#hrlogin		
	

		root.mainloop()

	
	
	
	
	
	

	def func_uncertainty(r):
		def f1(event,root):
			idxs=listbox1.curselection()
			if len(idxs)==1:
				idx=idxs[0]
				unc_id=unc_list[idx][0]
				root.destroy()
				print(type(unc_id))
				goto_object_unc(unc_id)

		def f2(root):
			unc_name=edit.get();unc_parent=parent.get()
			if unc_parent=='enter id of parent' or unc_parent=='':
				unc_parent=None
			####
			# insert new unc in table uncertainty and decision_uncertainty
			####
			cursor.execute("SELECT * from uncertainity")
			rows=cursor.fetchall()
			it=len(rows)+1
			#cursor.execute("insert into uncertainity(uncertainity_id,name,parent_uncertainity_id) values(it,unc_name,unc_parent)")
			tt=(it,unc_name,unc_parent)
			cursor.execute("insert into uncertainity(uncertainity_id,name,parent_uncertainity_id) values (?, ?,?)", it,unc_name,unc_parent)
			con.commit()
			cursor.execute("insert into decision_uncertainity(decision_id,uncertainity_id) values (?,?)", 1,it)
			con.commit()
			print (unc_parent,unc_name)
			#root.destroy()
			func_uncertainty(root)
		##get all uncertainty from uncertainty table	
		unc_list=[]
		cursor.execute("SELECT * from uncertainity")
		rows=cursor.fetchall()
		for row in rows:
			unc_list.append([str(row[0]),row[1],str(row[2])])
		###############
		r.destroy()
		root = Tk()
		root.geometry("1400x1300")
		root.configure(background="slategray4",pady=20)
		x=StringVar();x.set("UNCERTAINTIES")
		lab=Label(root,text=x.get(),font=('Courier new',30,'bold'),fg="Maroon")
		lab.pack(side=TOP)
		lab=Label(root,text="Ids       Uncertainties    Parent_ids",font=("Times", 15, "bold")).place(x=200,y=90)
		listbox1 = Listbox(root,bg="light grey",font=("Times",15),selectbackground="white",height=10,width=48)
		scrollbar1 = Scrollbar(root, orient=VERTICAL, command=listbox1.yview)
		scrollbar1.place(x=610,y=120,height=234,width=15)
		listbox1.configure(yscrollcommand=scrollbar1.set)
		listbox1.place(x=130,y=120)
		listbox1.bind('<<ListboxSelect>>',lambda event:f1(event,root))
		for i in range(0,len(unc_list)):
			listbox1.insert(i,str(unc_list[i][0])+"    "+str(unc_list[i][1])+"  "+str(unc_list[i][2]))
		new_unc=StringVar(); new_unc.set('add new uncertainty here'); parent_unc=StringVar(); parent_unc.set('enter id of parent')
		edit=Entry(root,bd=5,width=55); edit.place(x=750,y=120); edit.insert(0,new_unc.get())
		parent=Entry(root,bd=5,width=55); parent.place(x=750,y=220); parent.insert(0,parent_unc.get())
		add_unc=Button(root,text="ADD UNCERTAINTY",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="black",width=40,height=2,command=lambda:f2(root)).place(x=690,y=300)
		button=Button(root,text="Main Page",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:Options_Available(root))
		button.pack(side=BOTTOM)#hrlogin
		root.mainloop()


	def goto_object_unc(unc_id):
		def f11(event,root):
			idxs=listbox1.curselection()
			if len(idxs)==1:
				idx=idxs[0]
				obj_id=all_objects[idx][0]
				root.destroy()
				object_description(obj_id)
		def f22(event,root):	
			idxs=listbox2.curselection()
			if len(idxs)==1:
				idx=idxs[0]
				obj_id=unc_objects[idx][0]
				root.destroy()
				object_description(obj_id)
		def f2(root):
			obj=add_obj.get();att=add_att.get(); id=add_id.get();
			#obj=obj.split('=')
			attname_list=att.split(',')
			
			if obj=='' or obj=='add new object name' or id=='' or id=='add new object id' or att=='' or att=='enter attribute of object':
				return
			####
			#fetch all objects from object table. If id is already present with another object then add that (object_id and unc_id) in 
			#object_uncertainty table. 
			#if id is not present before add object_name in object table, (object_id, unc_id) in object_uncertainty table, attributes to 
			#attribute table.
			####
			cursor.execute('SELECT * FROM object')
			rows=cursor.fetchall()
			flag=0
			for row in rows:
				if row[0]==id:
					flag=1
			if flag==0:
				cursor.execute("insert into object(object_id,name,action_id) values (?,?,?)",id,obj,1)
				con.commit()
				cursor.execute("insert into object_uncertainity(object_id,uncertainity_id) values (?,?)",id,unc_id)
				con.commit()
				
			else:
				cursor.execute("insert into object_uncertainity(object_id,uncertainity_id) values (?,?)",id,unc_id)
				con.commit()
			#att=att.split(',')
			cursor.execute("select * from attribute")
			rows=cursor.fetchall()
			iii=len(rows)+1
			for val in range(0,len(attname_list)):
				try:
					cursor.execute("insert into attribute(attribute_id,name,value,object_id) values (?,?,?,?)",iii,attname_list[val],'',id)
					con.commit()
				except:
					break
				iii+=1			
			#print (obj,att_list,id)
			root.destroy()
			goto_object_unc(unc_id)
		print ("goto_object_unc ",unc_id)
		root = Tk()
		root.geometry("1400x1300")
		root.configure(background="slategray4",pady=20)
		x=StringVar();x.set("Uncertainty Objects")
		lab=Label(root,text=x.get(),font=('Courier new',30,'bold'),fg="Maroon")
		lab.pack(side=TOP)
		################
		#fetch all objects in object table
		cursor.execute("SELECT * FROM object")
		rows=cursor.fetchall()
		
		all_objects=[]
		#all_objects.append(["1","s"])
		print(rows)
		for row in (rows):
			#print(row[0])
		
			all_objects.append([row[0],row[1]])
		################
		lab=Label(root,text="Already id",font=("Times", 15, "bold")).place(x=300,y=90)
		listbox1 = Listbox(root,bg="light grey",font=("Times",15),selectbackground="white",height=10,width=48)
		scrollbar1 = Scrollbar(root, orient=VERTICAL, command=listbox1.yview)
		scrollbar1.place(x=610,y=120,height=233,width=15)
		listbox1.configure(yscrollcommand=scrollbar1.set)
		listbox1.bind('<<ListboxSelect>>',lambda event:f11(event,root))
		listbox1.place(x=130,y=120)
		for i in range(0,len(all_objects)):
			listbox1.insert(i,str(all_objects[i][0])+"    "+str(all_objects[i][1]))
		

		#################
		
		#fetch all objects that belong to unc_id;
		#get all object_ids from object_uncertainty;
		#use object_ids to get all object_names from object tabl.
		print(unc_id) 
		cursor.execute('SELECT object_id from object_uncertainity where uncertainity_id=?',unc_id)
		#SELECT uncertainity_id FROM object_uncertainity
		rows=cursor.fetchall()
		print("sameena")
		print(rows)
		unc_objects=[]
		
		for i in rows:
			cursor.execute('SELECT name from object where object_id=?',i[0])
			r=cursor.fetchall()
			unc_objects.append([str(i[0]),r[0][0]])
		#################
		lab=Label(root,text="Your id",font=("Times", 15, "bold")).place(x=980,y=90)
		listbox2 = Listbox(root,bg="light grey",font=("Times",15),selectbackground="white",height=10,width=20)
		scrollbar2 = Scrollbar(root, orient=VERTICAL, command=listbox2.yview)
		scrollbar2.place(x=1100,y=120,height=233,width=15)
		listbox2.configure(yscrollcommand=scrollbar2.set)
		listbox2.place(x=900,y=120)
		listbox2.bind('<<ListboxSelect>>',lambda event:f22(event,root))
		for i in range(0,len(unc_objects)):
			listbox2.insert(i,str(unc_objects[i][0])+"    "+str(unc_objects[i][1]))
		

		new_id=StringVar(); new_id.set('add new object id');
		new_obj=StringVar(); new_obj.set('add new object name'); att_obj=StringVar(); att_obj.set('enter attribute name of object')
		add_id=Entry(root,bd=5,width=55); add_id.place(x=550,y=400); add_id.insert(0,new_id.get())
		add_obj=Entry(root,bd=5,width=55); add_obj.place(x=550,y=450); add_obj.insert(0,new_obj.get())
		add_att=Entry(root,bd=5,width=55); add_att.place(x=550,y=500); add_att.insert(0,att_obj.get())
		
		add=Button(root,text="ADD OBJECT",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="black",width=40,height=2,command=lambda:f2(root)).place(x=570,y=620)
		button=Button(root,text="Main Page",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:Options_Available(root))
		button.pack(side=BOTTOM)#hrlogin
		root.mainloop()


	def object_description(object_ids):
		print(object_ids,"object")
		cursor.execute('select name from object where object_id=?',object_ids)
		rows=cursor.fetchall()
		print(rows)
		obj_name=""
		for row in rows:
			obj_name=row[0]
		cursor.execute('select attribute_id,name from attribute where object_id=?',object_ids)
		rows=cursor.fetchall()
		att_id=""
		att_name=""
		for row in rows:
			print(row)
			if att_id!="":
				att_id+=(","+str(row[0]))
				att_name+=(","+str(row[1]))
			else:
				att_id+=str(row[0])
				att_name+=str(row[1])
			
		print (att_id)
		print(att_name)
		root=Tk()
		root.configure(background="slategray4",pady=20)
		#nm=StringVar();em=StringVar();ph=StringVar();add=StringVar();pas=StringVar();qua=StringVar()
		root.geometry("1300x1300")
		root.title("Description")
		lab=Label(root,text="Description Of Object",font=('Courier new',30,'bold'),fg="Maroon")
		lab.pack(side=TOP)
		
		lab=Label(root,text="Object Name:",font=("Times", 20, "bold")).place(x=100,y=100)
		Quali =Entry(root,bd=5,width=55);Quali.place(x=400,y=100);Quali.insert(0,obj_name)
		lab=Label(root,text="Attribute ids:",font=("Times", 20, "bold")).place(x=100,y=200)
		Quali =Entry(root,bd=5,width=55);Quali.place(x=400,y=200);Quali.insert(0,att_id)
		lab=Label(root,text="Attributes Name:",font=("Times", 20, "bold")).place(x=100,y=300)
		Quali =Entry(root,bd=5,width=55);Quali.place(x=400,y=300);Quali.insert(0,att_name)
		button=Button(root,text="Main Page",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:Options_Available(root)).place(x=550,y=500) #hrlogin		
		root.mainloop()
		
	
		
	
	
	def func_action(r):
		def action_submit(r,action_value):
			n=action_value.get()
			#print()
			root.destroy()
			cursor.execute("SELECT * FROM action")
			rows = cursor.fetchall()
			if len(rows)==0:
				cursor.execute("insert into action values(?,?)",1,n)
				con.commit()
			
			action_object()
			
		def action_object():
			objidvalue=0
			def func(*args):
				idxs=listbox1.curselection()
				print(idxs[0])
				
				print(obj_name[idxs[0]])
				print(obj_id[idxs[0]])
				root.destroy()
				object_description(obj_id[idxs[0]]) #jhanvi
		
			def add_action_object(r):
				
				names=Quali2.get()
				names=names.split(',')
				
				print(names)
				print(Quali1.get())
				
				cursor.execute("select * from object")
				rows=cursor.fetchall()
				row1=len(rows)+1
				cursor.execute("select * from attribute")
				rows=cursor.fetchall()
				row2=len(rows)+1
				cursor.execute('insert into object values(?,?,?)',row1,Quali1.get(),1)
				con.commit()
				for i in range(0,len(names)):
					cursor.execute("insert into attribute(attribute_id,name,value,object_id) values (?,?,?,?)",row2,names[i],'',row1)
					con.commit()
					row2+=1
				
				r.destroy()
				action_object()
				
			
			root=Tk()
			root.configure(background="slategray4",pady=20)
			root.geometry("1400x1300")
			root.title("Action_Object")
			lab=Label(root,text="Action Object",font=('Courier new',30,'bold'),fg="Maroon")
			lab.pack(side=TOP)
			value1=""
			value2=""
			lab=Label(root,text="Name:",font=("Times", 20, "bold")).place(x=700,y=100)
			Quali1 =Entry(root,textvariable=value1,bd=5,width=55);Quali1.place(x=870,y=100);
			
			lab=Label(root,text="Atts name:",font=("Times", 20, "bold")).place(x=700,y=200)
			Quali2 =Entry(root,textvariable=value2,bd=5,width=55);Quali2.place(x=870,y=200);
			
			#lab=Label(root,text="Atts values:",font=("Times", 20, "bold")).place(x=700,y=300)
			#Quali3 =Entry(root,textvariable=value2,bd=5,width=55);Quali3.place(x=870,y=300);
			
			button=Button(root,text="Add",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:add_action_object(root)).place(x=800,y=400) #hrlogin		
	
			lab=Label(root,text="Object Name ",font=("Times", 20, "bold")).place(x=135,y=80)
			listbox1 = Listbox(root,bg="light grey",font=("Times",15),selectbackground="white",height=20,width=49)
			scrollbar1 = Scrollbar(root, orient=VERTICAL, command=listbox1.yview)
			scrollbar1.place(x=610,y=120,height=462,width=15)
			listbox1.configure(yscrollcommand=scrollbar1.set)
			listbox1.place(x=130,y=120)
			obj_name=[]
			obj_id=[]
			#obj_name.append("samee");obj_name.append("saif");obj_name.append("jhanvi");
			#obj_id.append(1);obj_id.append(2);obj_id.append(3);
			cursor.execute("SELECT * FROM object where action_id=?",1)
			rows = cursor.fetchall()
			for row in rows:
				obj_name.append(row[1])
				obj_id.append(row[0])
				
				
			
			
			listbox1.bind('<<ListboxSelect>>',func)  #jhanvi
			for i in range(0,len(obj_name)):
				listbox1.insert(i,obj_name[i]+ " " +str(obj_id[i]))
			root.mainloop()
		name=StringVar()
		value="check"
		r.destroy()
		root=Tk()
		root.configure(background="slategray4",pady=20)
		root.geometry("1920x1080")
		root.title("Action")
		cursor.execute("SELECT * FROM action")
		rows = cursor.fetchall()
		if len(rows)==1:
			name.set(rows[0][1])
		else:
			name.set("")
		lab=Label(root,text="Actions",font=('Courier new',30,'bold'),fg="Maroon")
		lab.pack(side=TOP)
		lab=Label(root,text="Name:",font=("Times", 20, "bold")).place(x=100,y=100)
		Quali =Entry(root,bd=5,width=55);Quali.place(x=200,y=100);Quali.insert(0,name.get())
		
		button=Button(root,text="Submit",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:action_submit(root,Quali)).place(x=470,y=550) #hrlogin		
		button=Button(root,text="Main Page",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:Options_Available(root))
		button.pack(side=BOTTOM)#hrlogin
		root.mainloop()
		
		



		
	def func_objective(r):
		r.destroy()
		objective()
	
	
	
	root=Tk()
	root.configure(background="slategray4",pady=20)
	nm=StringVar();em=StringVar();ph=StringVar();add=StringVar();pas=StringVar();qua=StringVar()
	root.geometry("1300x1300")
	root.title("OPTIONS")
	lab=Label(root,text="OPTIONS",font=('Courier new',30,'bold'),fg="Maroon")
	lab.pack(side=TOP)
	
	load=Image.open("im.jpg")
	resize=load.resize((550,250),Image.ANTIALIAS)
	render=ImageTk.PhotoImage(resize)
	i=Label(root,image=render)
	i.image=render
	i.place(x=380,y=80)
	button=Button(root,text="Uncertainties",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:func_uncertainty(root)).place(x=430,y=400) #hrlogin
	button=Button(root,text="Actions",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:func_action(root)).place(x=430,y=450) #hrlogin
	button=Button(root,text="Objectives",bg="DodgerBlue4",fg="white",activebackground="DodgerBlue2",activeforeground="white",width=60,height=2,command= lambda:func_objective(root)).place(x=430,y=500) #hrlogin		
	
	
	root.mainloop()

	
	
first_page()
#Options_Available()
