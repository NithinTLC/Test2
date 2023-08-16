from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
db = mysql.connector.connect(
    host='mysql',
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

    query = "SELECT * FROM credentials WHERE username = %s"
    params = (username,)
    cursor.execute(query, params)
    result = cursor.fetchone()

    if result and result[2] == password:
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        return render_template('dashboard.html', employees=employees)
    else:
        return 'Invalid username or password'

@app.route('/admin',methods=['GET','POST'])
def admin():
    if 'admin' in session:
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        return render_template('dashboard.html', employees=employees)
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
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        db.commit()
        return redirect(url_for('success'))
    return render_template('signup.html')

@app.route('/success', methods=['GET'])
def success():
    return "<h1>Sign up Success</h1>"

# @app.route('/search', methods=['POST'])
# def search():
#     search_value = request.form['search']
#     cursor.execute("SELECT * FROM employees WHERE first_name LIKE %s", ('%' + search_value + '%',))
#     employees = cursor.fetchall()
#     return render_template('dashboard.html', employees=employees)
@app.route('/search', methods=['POST'])
def search():
    search_value = request.form['search']
    query = "SELECT * FROM employees WHERE first_name LIKE %s"
    params = ('%' + search_value + '%',)

    if search_value:
        query += " OR skills LIKE %s OR qualifications LIKE %s"
        params += ('%' + search_value + '%', '%' + search_value + '%')

    cursor.execute(query, params)
    employees = cursor.fetchall()
    return render_template('dashboard.html', employees=employees)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = int(request.form['age'])
        experience = int(request.form['experience'])
        salary = int(request.form['salary'])
        skills = request.form['skills']
        qualifications = request.form['qualifications']
        cursor.execute(
            "INSERT INTO employees (first_name, last_name, age, experience, salary, skills, qualifications) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (first_name, last_name, age, experience, salary, skills, qualifications))
        db.commit()
    return  "<h1>added successfully</h1>"

@app.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    if request.method == 'GET':
        cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
        employee = cursor.fetchone()
        return render_template('edit.html', employee=employee)
    elif request.method == 'POST':
        # Handle the form submission and update the employee
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = int(request.form['age'])
        experience = int(request.form['experience'])
        salary = float(request.form['salary'])
        skills = request.form['skills']
        qualifications = request.form['qualifications']
        cursor.execute(
            "UPDATE employees SET first_name = %s, last_name = %s, age = %s, experience = %s, salary = %s, skills = %s, qualifications = %s WHERE id = %s",
            (first_name, last_name, age, experience, salary, skills, qualifications, employee_id))
        db.commit()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        return render_template('dashboard.html', employees=employees)
        # return "<h1>updated!!</h/>"
        # return render_template('dashboard.html')
    else:
        # Handle other HTTP methods (e.g., PUT, DELETE) if needed
        return "Method not supported"

@app.route('/refreshdb')
def refreshdb():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('dashboard.html', employees=employees)

@app.route('/delete/<int:employee_id>')
def delete(employee_id):
    cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
    db.commit()
    return "<h1>Deleted</h/>"

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to a different page
    return redirect(url_for('index'))

@app.route('/go_back')
def go_back():
    previous_page = request.referrer
    return redirect(previous_page or '/')
if __name__ == '__main__':
    app.run(debug=True)
