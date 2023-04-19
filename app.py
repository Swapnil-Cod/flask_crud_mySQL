from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask_api'
 
mysql = MySQL(app)

@app.route("/",methods=['GET'])
def show():
    if request.method =="GET":
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('select * from std_data')
        std = cur.fetchall()
        return render_template("index.html", Std=std )

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method=="POST":
        cur = mysql.connection.cursor()
        sname = request.form.get('name')
        sphone = request.form.get('phone')
        ssalary = request.form.get('salary')
        cur.execute('insert into std_data (std_name,std_phoneNo,std_address) values(%s,%s,%s)',(sname, sphone, ssalary))
        mysql.connection.commit()
        return redirect('/')
    return render_template('add.html')

@app.route("/update/<int:id>/",methods=['GET','POST'])
def update(id):
    if request.method=="GET":
        cu = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cu.execute('select * from std_data WHERE std_id=%s', [id])
        data = cu.fetchone()
        return render_template('update.html', Data=data)
    if request.method=="POST":
        cur = mysql.connection.cursor()
        sname = request.form.get('name')
        sphone = request.form.get('phone')
        saddress = request.form.get('address')
        cur.execute('UPDATE std_data SET std_name=%s,std_phoneNo=%s,std_address=%s WHERE std_id=%s', [sname, sphone, saddress, id])
        mysql.connection.commit()
        return redirect('/')

@app.route("/delete/<int:id>/",methods=['GET','POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from std_data where std_id=%s',[id])
    mysql.connection.commit()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)


