from flask import Flask, redirect, url_for, render_template
from flask import request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/report')
def report():
    return render_template('report.html')


@app.route('/filedreport', methods = ['POST', 'GET'])
def filedreport():
    if request.method == "POST":
        try:
            item_name = request.form['item_name']
            item_lost_loc = request.form['item_lost_loc']
            item_desc = request.form['item_desc']
            item_lost_date = request.form['item_lost_date']
            item_lost_time = request.form['item_lost_time']
            name = request.form['name']
            contact_num = request.form['contact_num']
            email = request.form['email']

            conn = sqlite3.connect("lostandfound.db")

            conn.execute("INSERT INTO report(item_name, item_lost_loc, item_desc, item_lost_date, item_lost_time, name, contact_num, email) VALUES (?,?,?,?,?,?,?,?)", (item_name, item_lost_loc, item_desc, item_lost_date, item_lost_time, name, contact_num, email))
            conn.commit()
            msg="Reported!"

        except:
            conn.rollback()
            msg = "Sorry, there was an error with reporting. Try again later"

        conn.close()
        return render_template("reported.html", msg=msg)
        


@app.route('/search')   
def search():
    con = sqlite3.connect("lostandfound.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM item")

    rows = cur.fetchall()
    con.close()
  
    return render_template("search.html",rows=rows)



@app.route('/adminlanding')
def adminlanding():
    return render_template('adminlanding.html')



@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/admintest')
def admintest():
    return render_template('admintest.html')

@app.route('/publishfind')
def publishfind():
    return render_template('publishfind.html')
 
@app.route('/publishedfind', methods = ['POST', 'GET'])
def publishedfind():
    if request.method == "POST":
        try:
            item_name = request.form['item_name']
            item_description  = request.form['item_description']
            found_date = request.form['found_date']
            found_location = request.form['found_location']
    

            conn = sqlite3.connect("lostandfound.db")

            conn.execute("INSERT INTO item(item_name, item_description, found_date, found_location) VALUES (?,?,?,?)", (item_name, item_description, found_date, found_location))
            conn.commit()
            msg="Published Find!"

        except:
            conn.rollback()
            msg = "Sorry, there was an error with publishing. Try again later"

        conn.close()
        return render_template("published.html", msg=msg)


#@app.route('/reportitem', methods = ['POST','GET'])
#def reportitem(): 
@app.route('/reporteditems')
def reporteditems():
    con = sqlite3.connect("lostandfound.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM report")

    rows = cur.fetchall()
    con.close()
   
    return render_template('reporteditems.html', rows=rows)

if __name__ == '__main__':
    app.run()
