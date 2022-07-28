from re import S
from telnetlib import STATUS
from this import d
from click import password_option
from flask import redirect
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os
import psycopg2
app = Flask(__name__)
DATABASE_URL = 'postgres://mhaezgysmzajom:54bdabe172ddbafee73bb9f9655955b60e5e318bfafb50979cbb2450c2c18c35@ec2-34-198-186-145.compute-1.amazonaws.com:5432/d8s5vcff8toasv'
           

@app.route('/', methods=['GET', 'POST']) #base root
def home_page():    
    # return redirect('/adminlogin')
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
            if(data[0][4]==password):
                # print("data[0][6]",data[0][6])
                if(data[0][6] == "admin"):
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    conn
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM roomdata;')
                    task = cur.fetchall()  
                    cur.close()
                    conn.close()
                    print(task)    
                    return render_template('home.html' ,name = data[0][1],tasks=task[::-1])
                elif(data[0][6] == "user"):
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    cur = conn.cursor()
                    sql="SELECT rid FROM roomaccess where name= %s"
                    adr = (str(data[0][1]),)
                    cur.execute(sql,adr)
                    task = cur.fetchall()  
                    string = "SELECT * FROM roomdata where rid ='"
                    if(len(task)==1):
                        string += task[0]
                        string += "'"
                    elif(len(task) > 1):
                        for i in range(len(task)-1):
                            string += task[i][0]
                            string += "'"
                            string += " or rid = '"
                        string += task[len(task)-1][0]
                        string += "'"
                    print(string)
                    cur.execute(string)
                    task = cur.fetchall()  
                    cur.close()
                    conn.close()
        
                    return render_template('user.html' ,name = data[0][1],tasks=task[::-1])
            else:
                return render_template('login.html')
        except:
            return render_template('login.html')

@app.route('/validemail', methods=['POST','GET'])   #login
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


@app.route('/signUpSubmit', methods=['POST'])
def signUpSubmit():
    try:
        if request.method == "POST":    
            name = request.form.get("ck")  
            if(str(name) == "chek"):
                add = request.form.get("fname")
                full_name = request.form.get("lname")
                emailaddr = request.form.get("email")
                passwordt = request.form.get("password")
                user = request.form.get("usertype")
                mphone = request.form.get("phone")
                if(add == "s@hil" or add == "bhus@n"):
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    conn
                    cur = conn.cursor()
                    cur.execute('INSERT INTO logindata (name, email,phone, password, addkey,logintype)'
                                'VALUES (%s, %s, %s, %s, %s, %s)',
                                (full_name,emailaddr,mphone,passwordt,add,user))
                    conn.commit()
                    cur.close()
                    conn.close() 
                    return render_template('home.html')
                else:
                    return render_template('signup.html')
            else:
                return render_template('signup.html')
    except:
        print("step3")
        return render_template('signup.html')

@app.route("/ne")
def secret():
    return render_template("signup.html")

@app.route("/home")
def home():
    return redirect('/adminlogin')
    
@app.route('/accessasign', methods=['POST','GET'])   #login
def accessasign():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn
    cur = conn.cursor()
    cur.execute('SELECT name FROM logindata where logintype = %s;',("user",))
    name = cur.fetchall()
    cur.execute('SELECT rid FROM roomdata;')
    rid = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('accessasign.html',name=name,rid=rid)

@app.route('/accessasignsub', methods=['POST','GET'])   #login
def accessasignsub():
    name =    request.form.get("name")
    rid =  request.form.get("rid")
    hour = request.form.get("hour")
    print(name,rid,hour)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn
    cur = conn.cursor()
    cur.execute('INSERT INTO roomaccess (name, rid,hour)'
                'VALUES (%s, %s,%s)',
                (name,rid,hour))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/accesslist')

@app.route('/addroomsubmit', methods=['POST'])   #login
def addroomsubmit():
    rid =    request.form.get("rid")
    espid =  request.form.get("espid")
    # name = request.form.get("ck")
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn
    cur = conn.cursor()
    cur.execute('INSERT INTO roomdata (rid, espid, ac1, lock1, ac2, lock2)'
                'VALUES (%s, %s,%s, %s, %s, %s)',
                (rid, espid,0, 0,0,0))
    cur.execute('INSERT INTO roomstatus (rid, espid, ac1, ac2)'
                'VALUES (%s, %s,%s, %s)',
                (rid, espid,0, 0))    
    conn.commit()
    cur.close()
    conn.close()
    print(rid , espid)
    # adminlogin()
    return redirect('/adminlogin')

@app.route('/addroom', methods=['POST','GET'])   #login
def addroom():
    return render_template('addroom.html')



@app.route("/cheakbox", methods=['POST','GET'])
def cheakbox():
    swa = (request.json['sw'])
    stat = (request.json['data'])
    nam = (request.json['name'])
    x = swa.split("_")
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    s = "UPDATE roomdata SET "
    ql = "=%s WHERE id = %s"
    sql = s + str(x[1]) + ql 
    adr = (int(stat),int(x[0]),)
    cur.execute(sql, adr)
    cur.execute('SELECT rid FROM roomdata where id = %s;',(int(x[0]),))
    temp = cur.fetchall()
    if(int(stat)==1):
        te = str(temp[0][0])+" "+str(x[1])+" is on"
    else:
        te = str(temp[0][0])+" "+str(x[1])+" is off"
    cur.execute('INSERT INTO logs (log, method)'    
                'VALUES (%s, %s)',
                (te, nam,))

    if(str(x[1])=="ac1" or str(x[1])=="ac2"):
        s = "UPDATE roomstatus SET "
        ql = "=%s WHERE rid = %s"
        sql = s + str(x[1]) + ql 
        print(str(temp[0][0]))
        adr = (int(stat),str(temp[0][0]),)
        cur.execute(sql,adr)
    conn.commit()
    cur.close()
    conn.close()
    return "ok"


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
    
@app.route('/logs', methods=['GET', 'POST']) 
def logs():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT * FROM logs;')
    data = cur.fetchall()
    # cur.execute('SELECT status FROM motordata;')
    # data1 = cur.fetchall()
    # cur.execute('SELECT onby FROM motordata;')
    # data2 = cur.fetchall()
    # cur.execute('SELECT time FROM motordata;')
    # data3 = cur.fetchall()
    # cur.execute('SELECT date FROM motordata;')
    # data4 = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('log.html',data = data[::-1])


@app.route('/adminlogin')
def adminlogin():
    # name = request.args.get('name')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT * FROM roomdata;')
    task = cur.fetchall()  
    cur.close()
    conn.close()
    return render_template('home.html' , tasks=task[::-1])

@app.route('/adminlogi')
def adminlogi():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT name FROM logindata;')
    namelist = cur.fetchall()  
    cur.close()
    conn.close()
    return render_template('access.html' , chooesname = "Chooes name", namelist=namelist[::-1])

@app.route('/accesslist', methods=['POST','GET'])
def accesslist():
    name = request.form.get('fullname')
    print("name",name)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT name FROM logindata where logintype = %s;',("user",))
    namelist = cur.fetchall()
    cur.execute('SELECT * FROM roomaccess where name = %s;',(name,))
    data = cur.fetchall()
    print(data)
    conn.commit()
    cur.close()
    conn.close()
    return render_template('access.html' , namelist = namelist[::-1] , chooesname = name , tasks=data[::-1])

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
        name = str(request.args.get('name'))
        now = datetime.now()
        date = str(now.strftime("%b %d, %Y"))
        time = str(now.strftime("%I:%M:%S %p"))
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        print("name",name)
        sql = "SELECT status FROM motorstatus WHERE name = %s"
        var = (name, )
        cur.execute(sql,var)
        data = (cur.fetchall())
        print("data",data)
        data = data[0][0]
        sql = "UPDATE ping SET date = %s ,time = %s WHERE name = %s"
        adr = (date,time,name, )
        cur.execute(sql,adr)
        conn.commit()
        cur.close()
        conn.close()
        # data = "aa"
    except:
        data = "pass"
    return str(data)

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
    app.run(host='0.0.0.0', port=80)
        
