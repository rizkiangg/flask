from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from config.db_config import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

mysql = init_db(app)

@app.route('/')
def home():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users')
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('error_page'))  # Redirect to an error page or handle it appropriately

    return render_template('index.html', users=data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'name' not in request.form or 'email' not in request.form or 'password' not in request.form:
            flash('All form fields are required!', 'danger')
            return redirect(url_for('register'))

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()

        if user:
            flash('Email already exists!', 'danger')
            return redirect(url_for('register'))
        else:
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            mysql.connection.commit()
            cur.close()

            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'email' not in request.form or 'password' not in request.form:
            flash('Email and password are required!', 'danger')
            return redirect(url_for('login'))

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):  # Verifikasi password
            session['loggedin'] = True
            session['id'] = user[0]
            session['name'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/error')
def error_page():
    return "An error occurred while fetching data."

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)