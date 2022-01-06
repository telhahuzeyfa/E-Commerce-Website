
from flask import Flask, session
from flask import render_template, request, redirect, url_for
import sqlite3, hashlib
# import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret key'
productImages = 'static/productImages'
app.config['productImages'] = productImages

def loginInfo():
    with sqlite3.connect('store_schema.sql') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            numItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = '" + session['email'] + "'")
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM cart WHERE userId = " + str(userId))
            numItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, numItems)

@app.route("/")
def home():
  loggedIn, firstName, numItems = loginInfo()
  with sqlite3.connect('store_schema.sql') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        productData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
  productData = location(productData)   
  return render_template('home.html', 
  productData=productData, loggedIn=loggedIn, 
  firstName=firstName, numItems=numItems, 
  categoryData=categoryData)

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error='')  

@app.route("/registerForm")
def registrationForm():
    return render_template("register.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('home'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)    
@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

def is_valid(email, password):
    con = sqlite3.connect('store_schema.sql')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False     

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        with sqlite3.connect('store_schema.sql') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName) VALUES (?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName))
                con.commit()
                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error"
        con.close()
        return render_template("login.html", error=msg)

def is_valid(email, password):
    con = sqlite3.connect('store_schema.sql')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False       

@app.route("/orderHistory")
def orderHistory():
    if 'email' not in session:
        return redirect(url_for('home'))
    loggedIn, firstName, numItems = loginInfo()
    return render_template("orderHistory.html", loggedIn=loggedIn, firstName=firstName, numItems=numItems)

@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, numItems = loginInfo()
    productId = request.args.get('productId')
    with sqlite3.connect('store_schema.sql') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ' + productId)
        productData = cur.fetchone()
    conn.close()
    return render_template("productDescription.html", data=productData, loggedIn = loggedIn, firstName = firstName, numItems = numItems)

@app.route("/displayCategory")
def displayCategory():
        loggedIn, firstName, numItems = loginInfo()
        categoryId = request.args.get("categoryId")
        with sqlite3.connect('store_schema.sql') as conn:
            cur = conn.cursor()
            cur.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = " + categoryId)
            data = cur.fetchall()
        conn.close()
        categoryName = data[0][4]
        data = location(data)
        return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName, numItems=numItems, categoryName=categoryName)
@app.route("/remove")
def remove():
    with sqlite3.connect('store_schema.sql') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        data = cur.fetchall()
    conn.close()
    return render_template('remove.html', data=data)
@app.route("/removeItem")
def removeItem():
    productId = request.args.get('productId')
    with sqlite3.connect('store_schema.sql') as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM products WHERE productID = ' + productId)
            conn.commit()
            msg = "Item Has Been Deleted"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    print(msg)
    return redirect(url_for('home'))    
@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, numItems = loginInfo()
    email = session['email']
    with sqlite3.connect('store_schema.sql') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, cart WHERE products.productId = cart.productId AND cart.userId = " + str(userId))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, numItems=numItems)
    
@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        with sqlite3.connect('store_schema.sql') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = '" + session['email'] + "'")
            userId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO cart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Item Has Been Added To Your Cart"
            except:
                conn.rollback()
                msg = "Error Occured"
        conn.close()
        return redirect(url_for('home'))

@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    productId = int(request.args.get('productId'))
    with sqlite3.connect('store_schema.sql') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
        userId = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM cart WHERE userId = " + str(userId) + " AND productId = " + str(productId))
            conn.commit()
            msg = "Item Has Been Removed"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    return redirect(url_for('home'))
    
@app.route("/checkout", methods=['GET','POST'])
def payment():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, numItems = loginInfo()
    email = session['email']

    with sqlite3.connect('store_schema.sql') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, cart WHERE products.productId = cart.productId AND cart.userId = " + str(userId))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
        print(row)
    conn.commit()
    return render_template("checkout.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, numItems=numItems)

def location(data):
    loc = []
    i = 0
    while i < len(data):
        cur = []
        for j in range(5):
            if i >= len(data):
                break
            cur.append(data[i])
            i += 1
        loc.append(cur)
    return loc
@app.route("/test", methods=['GET','POST'])
def test():
    return render_template("navigationBar.html");
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
