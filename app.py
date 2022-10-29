# If you are not good in python
# pls do not edit a damn shit
# 🛍️ 𝚂𝙼𝙰𝚁𝚃𝚂𝙷𝙾𝙿 🛒

from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask.signals import message_flashed
import MySQLdb.cursors
import re
import sqlite3

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ROYCE'
app.config['MYSQL_PASSWORD'] = '@--select*AND-modify#FIND_ONE'
app.config['MYSQL_DB'] = 'shop'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            flash ('Logged in successfully !')
            return render_template('home.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form and 'address' in request.form and 'address' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        name = request.form['name']


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO customers VALUES (NULL, % s, % s, %s, % s, % s, % s )', (username, password, email, phone, address, name))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username = %s', (session['username'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE adminID = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            msg = 'Logged in successfully as an ADMIN !'
            return render_template('adminhome.html', msg=msg)
        else:
            msg = 'Incorrect  ADMIN CREDENTIALS!'
    return render_template('admin_login.html', msg=msg)
@app.route('/adminlogout')
def adminlogout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('admin_login'))

@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')

@app.route('/customers')
def customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM customers")
    data = cur.fetchall()
    cur.close()

    return render_template('customers.html', customers=data )

@app.route('/add_customer', methods = ['POST'])
def add_customer():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        name = request.form['name']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customers (username, password, email, phone, address, name) VALUES (%s, %s, %s, %s, %s, %s)", (username, password, email, phone, address, name))
        mysql.connection.commit()
        return redirect(url_for('customers'))


@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('customers'))

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        name = request.form['name']

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE customers
               SET username=%s, password=%s, email=%s, phone=%s, address=%s, name=%s
               WHERE id=%s
            """, (username, password, email, phone, address, name, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('customers'))


@app.route('/productsmgmt')
def productsmgmt():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM products")
    data = cur.fetchall()
    cur.close()

    return render_template('productsmgmt.html', products=data )


@app.route('/add_product', methods = ['POST'])
def add_product():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        price = request.form['price']
        AdditionalInfo = request.form['AdditionalInfo']



        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name, price,  AdditionalInfo) VALUES (%s, %s, %s)", (name, price, AdditionalInfo))
        mysql.connection.commit()
        return redirect(url_for('productsmgmt'))


@app.route('/update_products',methods=['POST','GET'])
def update_products():

    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        price = request.form['price']
        AdditionalInfo = request.form['AdditionalInfo']


        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE products
               SET name=%s, price=%s, AdditionalInfo=%s
               WHERE id=%s
            """, (name, price, AdditionalInfo, id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('productsmgmt'))



@app.route('/delete_product/<string:id>', methods = ['GET'])
def delete_product(id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('productsmgmt'))

@app.route('/orders')
def orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM orders")
    data = cur.fetchall()
    cur.close()

    return render_template('orders.html', orders=data )

@app.route('/add_order', methods = ['POST'])
def add_order():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        price = request.form['price']
        product_name = request.form['product_name']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orders (name, phone,  address, price, product_name) VALUES (%s, %s, %s,%s, %s)", (name, phone, address, price, product_name))
        mysql.connection.commit()
        return redirect(url_for('orders'))


@app.route('/update_order',methods=['POST','GET'])
def update_order():

    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        price = request.form['price']
        product_name = request.form['product_name']

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE orders
               SET name=%s, phone=%s, address=%s, price=%s, product_name=%s
               WHERE id=%s
            """, (name, phone, address, price, product_name, id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('orders'))



@app.route('/delete_order/<string:id>', methods = ['GET'])
def delete_order(id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('orders'))

@app.route('/carts')
def carts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM orders")
    data = cur.fetchall()
    cur.close()

    return render_template('cart.html', carts=data )

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'phone' in request.form and 'address' in request.form and 'price' in request.form and 'product_name' in request.form :
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        price = request.form['price']
        product_name = request.form['product_name']


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO orders (name, phone,  address, price, product_name) VALUES (%s, %s, %s,%s, %s)", (name, phone, address, price, product_name))
        mysql.connection.commit()
        msg ='You have successfully ordered !'
        return redirect(url_for('carts'))
    else:
          msg =  'please fill in the following details details !'
    return render_template('cart.html', msg=msg)

@app.route('/vieworders')
def vieworders():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM orders WHERE phone = %s', (session['username'],))
        account = cursor.fetchone()
        return render_template('vieworder.html', account=account)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

# If you are not good in python
# pls do not edit a damn shit
# 🛍️ 𝚂𝙼𝙰𝚁𝚃𝚂𝙷𝙾𝙿 🛒
