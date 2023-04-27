from flask import Flask
from flask import render_template,request
import sqlite3

app = Flask(__name__)
app.config['email']=""
@app.route("/")
def home():
    app.config['email']=""
    return render_template('home.html')
@app.route("/login",methods = ['POST', 'GET'])
def login():
    if request.method=='POST':
        con=sqlite3.connect('database.db')
        try:
            cur = con.cursor()
            email = request.form['email'].lower()
            password = request.form['password']
            cur.execute("""SELECT email,password FROM user WHERE email=? and password=?""",(email,password))
            rows = cur.fetchone()
            if(rows):
                app.config['email']=email
                return render_template('afterlogin.html',rows=rows)
            else:
                return render_template('login.html',msg="e")
        except:
            print("Hi")
            return render_template('login.html',msg="e")
        finally:
            con.close()
    if request.method=='GET':
        return render_template('login.html',msg="")
@app.route("/mycart",methods = ['POST', 'GET'])
def mycart():
    con=sqlite3.connect('database.db')
    if request.method=='GET':
        cur = con.cursor()
        cur.execute("""SELECT * FROM cart WHERE email=?""",(app.config['email'],))
        rows = cur.fetchall()
        return render_template('mycart.html',rows=rows)
@app.route("/addcart",methods = ['POST', 'GET'])
def addcart():
    con=sqlite3.connect('database.db')
    try:
        if request.method=='POST':
            if(app.config['email']):
                title = request.form['booktitle']
                url  =request.form['url']
                cur = con.cursor()
                cur.execute("INSERT INTO cart (email ,cardname,url) VALUES (?,?,?)",(app.config['email'],title,url))
                cur.execute("SELECT * FROM books")
                rows = cur.fetchall()
                msg=[rows,f"The {title} has been successfully added to your cart.","text-success"]
                con.commit()
                return render_template('booksal.html',rows=msg)
            else:
                return render_template('login.html',msg="")
    except Exception as E:
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        msg=[rows,f"{title} has been already added to your cart.","text-danger"]
        return render_template('booksal.html',rows=msg)
    finally:
        con.close()
 
@app.route("/signup",methods = ['POST', 'GET'])
def signup():
    con=sqlite3.connect('database.db')
    try:
        if request.method=='POST':
            user_name = request.form['sun']
            email = request.form['semail'].lower()
            password = request.form['spassword']
            cur = con.cursor()
            cur.execute("INSERT INTO user (username , email , password) VALUES (?,?,?)",(user_name,email,password))
            con.commit()
            return render_template('signup.html',msg="s")
    except Exception as E:
        return render_template('signup.html',msg="e")
    finally:
        con.close()
        

    if request.method=='GET':
        return render_template('signup.html',msg="")
@app.route('/deletebook',methods = ['POST', 'GET'])
def deletebook():
    con=sqlite3.connect('database.db')
    if request.method=='POST':
        title = request.form['ctitle']
        url  =request.form['curl']
        cur = con.cursor()
        cur.execute("DELETE FROM cart WHERE email = ? AND cardname = ? AND url = ?", (app.config['email'], title, url))
        con.commit()
        cur.execute("""SELECT * FROM cart WHERE email=?""",(app.config['email'],))
        rows = cur.fetchall()
        return render_template('mycart.html',rows=rows)


@app.route('/about')
def about():
    return render_template('aboutus.html')
@app.route('/afterlogin')
def afterlogin():
    return render_template('afterlogin.html')
@app.route("/book")
def book():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM books")

    rows = cur.fetchall()
    con.close()
    if(app.config['email']):
        return render_template('booksal.html',rows=[rows,'',''])
    else:
        return render_template('books.html',rows=rows)
@app.route("/checkout")
def checkout():
    con=sqlite3.connect('database.db')
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cart WHERE email = ? ", (app.config['email'],))
        con.commit()
        return render_template('checkout.html')
    except:
        return render_template('checkout.html')
    finally:
        con.close()
if __name__ == '__main__':
   app.run(debug = True)