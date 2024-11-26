from flask import Flask,render_template,request,redirect
import sqlite3

app = Flask(__name__)

def create_connection():
    conn = sqlite3.connect("contact.db")
    return conn

def create_table():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS contact(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,number TEXT)')
    conn.commit()
    conn.close()

@app.route('/admin')
def admin():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contact')
    data = cur.fetchall()
    print(data)
    return render_template('admin.html',users=data)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return redirect('/register')

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method == 'POST':
        name = request.form['inp1']
        num = request.form['inp2'] 
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO contact(name , number)VALUES(?,?)''',(name,num)) 
        conn.commit()
        conn.close()
        print(name,num)
        return redirect('admin')
    return render_template("contact.html")

@app.route("/register", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        number = request.form['number']
        # password = request.form['password']
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO contact(name, number) VALUES(?,?)''', (username, number))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("register.html")

if __name__=="__main__":
    create_connection()
    create_table()
    app.run(debug=True)