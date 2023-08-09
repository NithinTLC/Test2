from flask import Flask, render_template, request, redirect, url_for,session
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Nithin#7786',
    database='employee_management'
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'password':
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        return render_template('prac.html',  employees=employees)
    else:
        return redirect(url_for('index', error='Invalid credentials'))


@app.route('/admin')
def admin():
    if 'admin' in session:
        # Fetch employee records from the database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        # Render the admin panel template with the fetched employee records
        return render_template('dashboard.html', username=session['admin'], employees=employees)
    else:
        return redirect('/login')

@app.route('/newacc')
def create():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        db.commit()
        return redirect(url_for('success'))
    return render_template('signup.html')

@app.route('/success', methods=['GET'])
def success():
    return "<h1>Login Success</h1>"

if __name__ == '__main__':
    app.run(debug=True)
