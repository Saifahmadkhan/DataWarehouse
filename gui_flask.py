from flask import Flask,render_template,request
import ast
import etl
app = Flask(__name__)
##################################
@app.route("/upload/hotel")
def upload_hotel():		## for extracting data for hotel dimension
	return render_template('hotel_upload.html')
	
@app.route("/uploader/hotel", methods = ['GET', 'POST'])
def uploader_hotel():
	if request.method == 'POST':
	    f = request.files['file']
	    #f.save(secure_filename(f.filename))
	    etl.csvtodb_hotel(f.read())
	    return 'file uploaded successfully'

@app.route('/extraction/hotel')
def extract_hotel():
	etl.extract_hotel()
	return "Extraction successful"

@app.route('/view/hotel')
def view_hotel():
	table=etl.select_hotel()	
	return render_template('hotel_view.html', len1=len(table), len2=len(table[0]), table=table)

##################################
@app.route("/")
def home():
	return render_template('home.html')
@app.route("/extract")
def extract():				## for extracting data for timestamp dimension
	etl.extract()
	return "extraction successful"

@app.route('/upload')
def file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   	if request.method == 'POST':
	    f = request.files['file']
	    #f.save(secure_filename(f.filename))
	    etl.csvtodb(f.read())
	    return 'file uploaded successfully'
    
@app.route("/dimension", methods=["GET","POST"])
def dimension():
	return render_template('dimension.html')

@app.route("/fact",methods=["GET","POST"])
def fact():
	return render_template('fact1.html')

@app.route("/view",methods=["GET","POST"])
def view():
	return render_template('fact11.html')
	

@app.route("/processing/dim",methods=["GET","POST"])
def get_new_record():						##get new record for changing dimension
	if request.method=="POST":
		dimension_table=request.form["dim"]					##'Dim_table_timestamp'
		s=request.form['dim_attr'].strip('{}'); s=s.split(',')[0];pk=int(s.split(':')[1])
		dimension_attr=	ast.literal_eval(request.form["dim_attr"])					##{'date_id':1,'date':'01.02.2019','day':'mon','month':'jan','year':'2019'}
		#return dimension_table,dimension_attr,pk
		sk=etl.select(dimension_table,pk)
		if sk!=None:
			etl.update(dimension_table,sk)
		etl.insert(dimension_table+" (date_id,date,day,month,year,end_date,flag)",dimension_attr,pk)
		table=etl.get_data(2)
		return render_template('view.html', table_name=dimension_table, table=table, len1=len(table), len2=len(table[0]), id=2)
    
@app.route("/processing/fact1",methods=["GET","POST"])
def get_new_record1():						##get new record for changing dimension
	if request.method=="POST":
		fact_table=request.form["fact"]					##'Dim_table_timestamp'
		dim_list=etl.find_dim(fact_table)
		return render_template('fact2.html', length=len(dim_list), fact=fact_table, dim_list=dim_list)

@app.route("/processing/fact2",methods=["GET","POST"])
def get_new_record2():
	if request.method=="POST":
		dim_sk=[];ct=0
		while 1:
			try:
				dim_sk.append(request.form["dim"+str(ct)]);ct+=1
			except:
				break
		fact_attr=request.form["fact_attr"]
		etl.put_data(dim_sk,fact_attr)
		table=etl.get_data(0)
		return render_template('view.html', table_name='Fact_table_Make_Booking', table=table, len1=len(table), len2=len(table[0]), id=0)

@app.route("/processing/fact11",methods=["GET","POST"])
def view_record():
	if request.method=="POST":
		fact_table=request.form['fact']
		if 'Fact' in fact_table:
			table=etl.get_data(0);id=0
		elif 'hotel' in fact_table:
			table=etl.get_data(1);id=1
		else:
			table=etl.get_data(2);id=2
		return render_template('view.html', table_name=fact_table, table=table, len1=len(table), len2=len(table[0]), id=id)	
		

if __name__ == "__main__":
    app.run(debug=True)
