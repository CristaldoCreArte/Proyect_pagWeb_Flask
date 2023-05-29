from flask import Flask, render_template,request,redirect,url_for,session,flash
from Form.forms import User
from dotenv import load_dotenv
import os
import sqlite3
from Form.forms import User



def create_consult_table():
    conexion = sqlite3.connect('consult.db')
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consult (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            fullname TEXT NOT NULL,
            numberPhone INTEGER NOT NULL,
            email TEXT NOT NULL,
            consult TEXT NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()

create_consult_table()


def create_users_register():
    conexion = sqlite3.connect('users.db')
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()


create_users_register()


def check_email_exists(email):
    conexion = sqlite3.connect('users.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT email FROM users WHERE email=?", (email,))
    result = cursor.fetchone()
    conexion.close()

email = 'example@example.com'
check_email_exists(email)


app = Flask (__name__)
app.secret_key = '@@@POLOC2G3JDdsfew91j'
database_url = os.environ.get('DATABASE_URL')



@app.route('/')
def home():
    return render_template("form.html")

@app.route('/login', methods=['POST','GET'])
def login():

    if request.method == 'POST' and 'email' in request.form and 'password':
        email = request.form['email']
        password = request.form['password']
        conexion = sqlite3.connect('users.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT email,password FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conexion.close()
        if user:
            session['id'] = user['id']
            return render_template('home.html')
        else:
            flash('Las credenciales no coinciden')
            return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = User()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if check_email_exists(email):
            flash('El correo electrónico ya está en uso.')
            return redirect(url_for('home'))
        else:
            # Insertar el usuario en la base de datos
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            conn.close()

            flash('Registro exitoso. ¡Bienvenido!')
            return redirect(url_for('home'))

    return render_template('form.html', form=form)
    # if request.method == 'POST':
    #     user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'])
    #     conexion = sqlite3.connect('users.db')
    #     cursor = conexion.cursor()
    #     cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (str(user.username), str(user.email), str(user.password)))
    #     sql = cursor.fetchone()
    #     conexion.commit()
    #     conexion.close()
    #     if check_email_exists(email):
    #         flash('El Email esta en uso')
    #         return redirect(url_for('home'))
    #     else:
    #         return render_template('home.html')


@app.route('/consult', methods=['POST'])
def consult():
    if request.method == 'POST':
        fullname = request.form['fullname']
        numberPhone = request.form['numberPhone']
        email = request.form['email']
        consult= request.form['consult']

        with sqlite3.connect('consult.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO consult (fullname, numberPhone, email, consult) VALUES (?, ?, ?, ?)", (fullname,numberPhone, email, consult))
            conexion.commit()
            return render_template('home.html')
    return render_template('home.html')


# @app.route('/homer')
# def homer():
#     if 'user' in session:
#         return render_template('home.html')
#     else:
#         return "No tiene una cuenta registrada"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    create_users_register()
    create_consult_table()
    check_email_exists(email)
    app.run(debug=True)


