from flask import Flask,render_template,request,session,flash
import ibm_db
app=Flask(__name__)
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;\
                    PORT=32731;UID=klm67409;PWD=hwg2Nu5G2huw2k5C;security=SSL;sslcertificate=DigiCertGlobalRootCA.crt",' ',' ')
print(conn)
connstate=ibm_db.active(conn)
print(connstate)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/")
def index():
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
        return render_template("index.html")
    return render_template("appointment.html")
@app.route("/record",methods=["GET","POST"])
def record():
    if request.method == "POST":
        name = request.form['patient_name']
        dob=request.form["dob"]
        age=request.form["age"]
        height=request.form["height"]
        weight=request.form["weight"]
        bmi=request.form["bmi"]
        bp=request.form["blood_pressure"]
        sugar=request.form["sugar"]
        notes=request.form["notes"]
        details = [name,dob,age,height,weight,bmi,bp,sugar,notes]
        print(details)
         
        sql = "INSERT into RECORD VALUES (?,?,?,?,?,?,?,?,?)"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.bind_param(stmt, 2, dob)
        ibm_db.bind_param(stmt, 3, age)
        ibm_db.bind_param(stmt, 4, height)
        ibm_db.bind_param(stmt, 5, weight)
        ibm_db.bind_param(stmt, 6, bmi)
        ibm_db.bind_param(stmt, 7, bp)
        ibm_db.bind_param(stmt, 8, sugar)
        ibm_db.bind_param(stmt, 9, notes)
        ibm_db.execute(stmt)
        return render_template("index.html")
    return render_template("health_record.html")

@app.route("/login",methods=["GET","POST"])
def login():
    global uemail
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
            uemail = session['email']            
            return render_template("index.html")
        else:
            msg = "Invalid Credentials"
            return render_template("login.html", message=msg)
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
            
            return render_template("register.html",message=msg)
        else: 
            sql = "INSERT into REGISTER_HEALTHCONNECT VALUES (?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2, email)
            ibm_db.bind_param(stmt, 3, password)
            ibm_db.execute(stmt)
            msg = "You have Successfully REGISTERED, Please LOGIN"            
            return render_template("register.html", message = msg)
    return render_template("register.html")
@app.route("/forget")
def forget():
    return render_template("forgot.html")


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)

