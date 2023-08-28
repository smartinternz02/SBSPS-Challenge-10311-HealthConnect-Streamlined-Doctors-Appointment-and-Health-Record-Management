from flask import Flask,render_template,request,session,flash
import ibm_db
app=Flask(__name__)
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;\
                    PORT=32731;UID=klm67409;PWD=hwg2Nu5G2huw2k5C;security=SSL;sslcertificate=DigiCertGlobalRootCA.crt",' ',' ')
print(conn)
connstate=ibm_db.active(conn)
print(connstate)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/healthdetails")
def heathdetails():
    uname=session['username']
    uemail = session['email']
    sql = "SELECT * FROM RECORD WHERE MAIL=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, uemail)
    ibm_db.execute(stmt)
    acc = ibm_db.fetch_assoc(stmt)
    print(acc)
    if(acc):
        return render_template("health_details.html",name=acc["NAME"],mail=acc["MAIL"],dob=acc["DOB"],age=acc["AGE"],height=acc["HEIGHT"],weight=acc["WEIGHT"],bmi=acc["BMI"],blood_pressure=acc["BP"],sugar=acc["SUGAR"],notes=acc["NOTES"])
    else:
        flash("Your health record is unavailable please update")
        return render_template("record_menu.html")
@app.route("/record_menu")
def record_menu():
    return render_template("record_menu.html")
@app.route("/")
def index():
    return render_template("index.html",msg="Please login before using the service")

@app.route("/iol")
def iol():
    flash(f"Hi {uname} Welcome to Health Connect \n")            
    return render_template("index.html")

@app.route("/appointment",methods=["GET","POST"])
def appointment():
        if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            department = request.form['department']
            date=request.form['date']
            time=request.form['time']
            details = [name,email,department,date,time]
            print(details) 
            sql = "INSERT into APPOINT VALUES (?,?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2, email)
            ibm_db.bind_param(stmt, 3, department)
            ibm_db.bind_param(stmt, 4, date)
            ibm_db.bind_param(stmt, 5, time)
            ibm_db.execute(stmt)
            msg="your appointment has been submitted successfully!"
            flash(msg)
            return render_template("index.html")
        return render_template("appointment.html")
    

@app.route("/record",methods=["GET","POST"])
def record():
    if request.method == "POST":
        name = request.form['patient_name']
        mail=request.form["mail"]
        dob=request.form["dob"]
        age=request.form["age"]
        height=request.form["height"]
        weight=request.form["weight"]
        bmi=request.form["bmi"]
        bp=request.form["blood_pressure"]
        sugar=request.form["sugar"]
        notes=request.form["notes"]
        details = [name,mail,dob,age,height,weight,bmi,bp,sugar,notes]
        print(details)   
        sql = "INSERT into RECORD VALUES (?,?,?,?,?,?,?,?,?,?)"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.bind_param(stmt, 2, mail)
        ibm_db.bind_param(stmt, 3, dob)
        ibm_db.bind_param(stmt, 4, age)
        ibm_db.bind_param(stmt, 5, height)
        ibm_db.bind_param(stmt, 6, weight)
        ibm_db.bind_param(stmt, 7, bmi)
        ibm_db.bind_param(stmt, 8, bp)
        ibm_db.bind_param(stmt, 9, sugar)
        ibm_db.bind_param(stmt, 10, notes)
        
        ibm_db.execute(stmt)
        flash("Your records has been updated successfully!")
        return render_template("record_menu.html")
    return render_template("health_record.html")

@app.route("/login",methods=["GET","POST"])
def login():
    global uemail
    global uname
    if request.method == 'POST':
        email = request.form['email']
        password =  request.form['password']
        details = [email, password]
        print(details)
        sql = "SELECT * FROM REGISTER_HEALTHCONNECT where EMAIL=? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        print(acc)
        if acc: 
            session['email'] = email
            session['username'] = acc['NAME']
            uname=session['username']
            uemail = session['email']
            session["logged_in"]=True
            
            flash(f"Hi {uname} Welcome to Health Connect \n")            
            return render_template("index.html")
        else:
            msg = "Invalid Credentials"
            flash(msg)
            return render_template("login.html")
    return render_template("login.html")
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        details = [name,email,password]
        print(details)
        sql = "SELECT * FROM REGISTER_HEALTHCONNECT where EMAIL=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        # ibm_db.bind_param(stmt, 2, name)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        print(acc)
        if acc:
            msg = "You have been already REGISTERED, please login!"
            flash(msg)
            return render_template("register.html")
        else: 
            sql = "INSERT into REGISTER_HEALTHCONNECT VALUES (?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2, email)
            ibm_db.bind_param(stmt, 3, password)
            ibm_db.execute(stmt)
            msg = "You have Successfully REGISTERED, Please LOGIN" 
            flash(msg)           
            return render_template("register.html")
    return render_template("register.html")
@app.route("/forget")
def forget():
    return render_template("forgot.html")


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)

