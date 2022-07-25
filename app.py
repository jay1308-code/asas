from re import S
from telnetlib import STATUS
from this import d
from click import password_option
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os
import psycopg2
app = Flask(__name__)
DATABASE_URL ='postgres://hzbckwzoqtmlqe:a0f34997b0c650328b4187f36564e47527d06b787f84733fb05555f4e9a9c15d@ec2-52-204-157-26.compute-1.amazonaws.com:5432/d7j9i3rbgtinuj'
           

# class motordata(db.Model):
#     id =     db.Column(db.Integer,primary_key=True)
#     date =   db.Column(db.String(1000))
#     time =   db.Column(db.String(1000))
#     status = db.Column(db.String(1000))
#     onby =   db.Column(db.String(1000))
# class acstatus(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     ac = db.Column(db.String(1000))
#     status = db.Column(db.String(1000))
# class alaram(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     motor = db.Column(db.String(1000))
#     status = db.Column(db.String(1000))
#     shour = db.Column(db.String(1000))
#     smin = db.Column(db.String(1000))
#     szone = db.Column(db.String(1000))
#     ehour = db.Column(db.String(1000))
#     emin = db.Column(db.String(1000))
#     ezone = db.Column(db.String(1000))
# class Logindata(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(1000))
#     email = db.Column(db.String(1000))
#     passsword = db.Column(db.String(1000))
#     addkey = db.Column(db.String(1000))

@app.route('/', methods=['GET', 'POST']) 
def home_page():    
    # changedata("lawbore",1,"sahil")
    return render_template('login.html')

@app.route('/LoginSubmit', methods=['POST'])
def logInSubmit():
    if request.method == "POST":      
        emailid = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("ck")
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            conn
            cur = conn.cursor()
            sql = 'SELECT * FROM logindata WHERE email = %s;'
            cur.execute(sql,(emailid,))
            data = cur.fetchall()
            cur.close()
            conn.close()
            # print(len(data))
            # print("Step1")
            if(data[0][5] == "admin"):
                if(data[0][3]==password):
                    return render_template('home.html' ,name = data[0][1])
                else:
                    return render_template('login.html')    
            else:
                return render_template('user.html',name = data[0][1])                    
                # print("Step2")

        except:
            return render_template('login.html')
    
@app.route('/validemail', methods=['POST'])   #login
def validemail():
    if (request.method == 'POST'):
        name = (request.json['name'])
        print(name)
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        conn
        cur = conn.cursor()
        sql = 'SELECT * FROM logindata WHERE email = %s;'
        cur.execute(sql,(name,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        if(len(data) >= 1):
            return "valid"
        else:
            return "not valid"

@app.route('/cheakUserName', methods=['POST'])  #signup
def CheakUserName():
    if (request.method == 'POST'):
        name = (request.json['name'])
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        conn
        cur = conn.cursor()
        sql = 'SELECT * FROM logindata WHERE email = %s;'
        cur.execute(sql,(name,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        if(len(data) == 1):
            return "email exist"
        else:
            return "chek"

@app.route("/ne")
def secret():
    return render_template("signup.html")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/signUpSubmit', methods=['POST'])
def signUpSubmit():
    if request.method == "POST":
        try:    
            name = request.form.get("ck")  
            if(str(name) == "chek"):
                add = request.form.get("fname")
                full_name = request.form.get("lname")
                emailaddr = request.form.get("email")
                passwordt = request.form.get("password")
                user = request.form.get("usertype")
                if(add == "s@hil" or add == "bhus@n"):
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    conn
                    cur = conn.cursor()
                    cur.execute('INSERT INTO logindata (name, email, password, addkey,logintype)'
                                'VALUES (%s, %s, %s, %s, %s)',
                                (full_name,emailaddr,passwordt,add,user))
                    conn.commit()
                    cur.close()
                    conn.close() 
                    return render_template('home.html')
        except:
            print("step3")
            return render_template('signup.html')

@app.route('/logininfo', methods=['GET', 'POST']) 
def data_page():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT name FROM logindata;')
    data = cur.fetchall()
    cur.execute('SELECT email FROM logindata;')
    data1 = cur.fetchall()
    cur.execute('SELECT password FROM logindata;')
    data2 = cur.fetchall()
    cur.execute('SELECT logintype FROM logindata;')
    data3 = cur.fetchall()   
    cur.close()
    conn.close()
    return render_template('logindata.html',data = data[::-1] , data1 = data1[::-1],status = data2[::-1],onby=data3[::-1])
    
@app.route('/motorinfo', methods=['GET', 'POST']) 
def ssa():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT name FROM motordata;')
    data = cur.fetchall()
    cur.execute('SELECT status FROM motordata;')
    data1 = cur.fetchall()
    cur.execute('SELECT onby FROM motordata;')
    data2 = cur.fetchall()
    cur.execute('SELECT time FROM motordata;')
    data3 = cur.fetchall()
    cur.execute('SELECT date FROM motordata;')
    data4 = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('datapage.html',date = data4[::-1],data = data[::-1] , data1 = data1[::-1],status = data2[::-1],onby=data3[::-1])

def changedata(name,status,onby):
    print("change data")
    now = datetime.now()
    date = str(now.strftime("%b %d, %Y"))
    time = str(now.strftime("%I:%M:%S %p"))
    DATABASE_URL ='postgres://hzbckwzoqtmlqe:a0f34997b0c650328b4187f36564e47527d06b787f84733fb05555f4e9a9c15d@ec2-52-204-157-26.compute-1.amazonaws.com:5432/d7j9i3rbgtinuj'
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    sql = "UPDATE motorstatus SET status = %s WHERE name = %s"
    adr = (status,name,)
    cur.execute(sql,adr)
    cur.execute('INSERT INTO motordata (name, status, onby,date,time)'
                'VALUES (%s, %s, %s,%s, %s)',
                (name, status, onby,date,time))
    # cur.execute('SELECT * FROM motorstatus;')
    # data = cur.fetchall()
    # print(".......................")
    # print(data)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/switch', methods=['POST'])
def aaa():
    sw = (request.json['sw'])
    stat = (request.json['data'])
    print(sw)
    print(stat)
    try:
        name = (request.json['name'])
    except:
        name = "Eror"
    if(sw==1):
        changedata("lawbore",stat,name)
    elif(sw==2):
        changedata("sprinkles",stat,name)
    elif(sw==3):
        changedata("lawborealaram",stat,name)
    elif(sw==4):
        changedata("sprinklesalaram",stat,name)
    else:
        acno = "as"
    return "ok"


# @app.route('/update', methods=['POST'])
# def update():
#     roomno = (request.json['rno']) 
#     humi = (request.json['humi'])
#     te = (request.json['temp'])
#     t = dbms(rid = roomno , humidity = humi ,temp=te)
#     db.session.add(t)
#     db.session.commit()
#     return "Updateed"

@app.route('/temp', methods=['POST'])
def temp():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute('SELECT * FROM alaram;')
        data = cur.fetchall()
        # print(data)
        conn.commit()
        cur.close()
        conn.close()
        if(0 == 0 ):
            b = "Alarm is OFF and motor1 start at " + str(data[0][2]) +" and turn off at "+ str(data[0][3])   
        else:
            b = "Alarm is ON motor1 start at " + + str(data[0][2]) +" and turn off at "+ str(data[0][3])   
    except:
        # pass
        b = "emty"
    return b

@app.route('/temp1', methods=['POST'])
def temp1():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute('SELECT * FROM alaram;')
        data = cur.fetchall()
        print(data)
        conn.commit()
        cur.close()
        conn.close()
        if(0 == 0):
            b = "Alarm is OFF and motor1 start at " + str(data[0][2]) +" and turn off at "+ str(data[0][3])   
        else:
            b = "Alarm is ON motor1 start at " + + str(data[0][2]) +" and turn off at "+ str(data[0][3])   
    except:
        # pass
        b = "emty"
    return b



# @app.route('/espupdate', methods=['GET','POST'])
# def espupdate():
#     try:
#         a = request.args.get('a')
#         b = request.args.get('b')
#         c = request.args.get('c')
#         t = dbms(rid = a , humidity = b ,temp=c)
#         # db.session.add(t)
#         # db.session.commit()
#         return str(a)+str(b)
#     except:
#         return "pass"

@app.route('/espac', methods=['GET','POST'])
def espac():
    try:  
        now = datetime.now()
        date = str(now.strftime("%b %d, %Y"))
        time = str(now.strftime("%I:%M:%S %p"))
        DATABASE_URL ='postgres://hzbckwzoqtmlqe:a0f34997b0c650328b4187f36564e47527d06b787f84733fb05555f4e9a9c15d@ec2-52-204-157-26.compute-1.amazonaws.com:5432/d7j9i3rbgtinuj'
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute('SELECT * FROM motorstatus;')
        data = cur.fetchall()
        sql = "UPDATE ping SET date = %s ,time = %s WHERE name = %s"
        adr = (date,time,"lawbore", )
        cur.execute(sql,adr)
        conn.commit()
        cur.close()
        conn.close()
        b = data[0][2]
        c = 0
        d = 0
        e = 0
    except:
        b = 5
        c = 5
        d = 5
        e = 5
    return str(b) + str(c)+ str(d)+ str(e) 

@app.route('/sched', methods=['GET','POST'])
def sched():
    try:
        #print("comi")
        name = (request.json['motor'])
        starttime = (request.json['shour']) + ":" + (request.json['smin']) +" " +(request.json['szone'])
        endtime = (request.json['ehour'])+ ":" + (request.json['emin']) +" " +(request.json['ezone'])
        # print(name)
        # print(starttime)
        # print(endtime)
        # DATABASE_URL ='postgres://hzbckwzoqtmlqe:a0f34997b0c650328b4187f36564e47527d06b787f84733fb05555f4e9a9c15d@ec2-52-204-157-26.compute-1.amazonaws.com:5432/d7j9i3rbgtinuj'
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        sql = "UPDATE alaram SET stime = %s , etime = %s WHERE name = %s"
        adr = (starttime,endtime,name )
        cur.execute(sql,adr)
        conn.commit()
        cur.close()
        conn.close()
    except:
        print("pass")
        pass
    return "ok"

@app.route('/swpos', methods=['GET','POST'])
def swpos():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        sql = "SELECT status FROM motorstatus where name = %s ;"
        adr = ("lawbore", )
        cur.execute(sql,adr)
        data = cur.fetchall()
        sql = "SELECT status FROM motorstatus where name = %s ;"
        adr = ("sprinkles", )
        cur.execute(sql,adr)
        data1 = cur.fetchall()
        print(data[0][0])
        cur.close()
        conn.close()
        s = str(data[0][0]) + str(data1[0][0])
        # print(s)/
        return s
    except:
        print("pass")
        return "22"

@app.route('/online', methods=['GET','POST'])
def online():
    try:
        DATABASE_URL ='postgres://hzbckwzoqtmlqe:a0f34997b0c650328b4187f36564e47527d06b787f84733fb05555f4e9a9c15d@ec2-52-204-157-26.compute-1.amazonaws.com:5432/d7j9i3rbgtinuj'
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute('SELECT * FROM ping;')
        data = cur.fetchall()
        # print(data)
        conn.commit()
        cur.close()
        conn.close()
        lhour = int(int(data[0][3][0:2]))
        lmin = int(int(data[0][3][3:5]))
        now = datetime.now()
        # nowdate = now.strftime("%b %d, %Y")
        nowhour = int(now.strftime("%I"))
        nowmin = int(now.strftime("%M"))
        if(nowhour == lhour):
            if(nowmin-lmin < 2 ):
                return "online"
            else:
                return "ofline"
        else:
            return "offline"        
    except:
        return "data is not come"
    


if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    # db.switch.drop()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=82)
        
