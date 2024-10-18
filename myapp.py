from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from config.db_config import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

mysql = init_db(app)

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

    return render_template('login.html')

@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html', name=session['name'])
    else:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)