import sqlite3

conn = sqlite3.connect('store_schema.sql')

conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		email TEXT,
		firstName TEXT,
		lastName TEXT
		)''')

conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		description TEXT,
		image TEXT,
		stock INTEGER,
		categoryId INTEGER,
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')       
conn.execute('''CREATE TABLE cart
		(userId INTEGER,
		productId INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''') 
conn.execute('''CREATE TABLE Order
		(userId INTEGER,
		productId INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')
conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')

conn.execute("INSERT INTO categories VALUES(1, 'Premer league')")
conn.execute("INSERT INTO categories VALUES(2, 'La Liga')")
conn.execute("INSERT INTO categories VALUES(3, 'Bundesliga')")
conn.execute("INSERT INTO categories VALUES(4, 'French League 1')")

conn.execute("INSERT INTO products VALUES(1, 'Arsenal Home Shirt', 50.0, 'Home shirt/kit for Arsenal Football Club', 'Arsenal_Home_Shirt.jpg', 11, 1)");
conn.execute("INSERT INTO products VALUES(2, 'Barcelona Home Shirt', 70.0, 'Home shirt/kit of Barcelona Football Club', 'BarcaHome.jpg', 12, 2)");
conn.execute("INSERT INTO products VALUES(3, 'Bayern Home Shirt', 60.0, 'Home shirt/kit of Bayern Munich Football Club', 'BayernHome.jpeg', 32, 3)");
conn.execute("INSERT INTO products VALUES(4, 'Borussia Dortmund Home Shirt', 40.0, 'Home shirt/kit of Borussia Dortmund Football Club', 'BVB.jpg', 32, 3)");
conn.execute("INSERT INTO products VALUES(5, 'Chealsea Home Shirt', 60.0, 'Home shirt/kit of Chealsea Football Club', 'Chelsea_Home_Shirt.jpg', 42, 1)");
conn.execute("INSERT INTO products VALUES(6, 'Liverpool Home Shirt', 60.0, 'Home shirt/kit of Liverpool Football Club', 'liverpool.jpeg', 52, 1)");
conn.execute("INSERT INTO products VALUES(7, 'Real Madrid Home Shirt', 80.0, 'Home shirt/kit of Real Madrid Football Club', 'MadridHome.jpg', 62, 2)");
conn.execute("INSERT INTO products VALUES(8, 'Manchester United Home Shirt', 80.0, 'Home shirt/kit of Manchester United Football Club', 'ManUtd_Home_Shirt.jpg', 72, 1)");
conn.execute("INSERT INTO products VALUES(9, 'PSG Home Shirt', 70.0, 'Home shirt/kit of PSG Football Club', 'PSG.jpg', 82, 4)");
conn.execute("INSERT INTO products VALUES(10, 'Tottenham Hotspur Home Shirt', 50.0, 'Home shirt/kit of Tottenham Hotspur Football Club', 'Tottenham.jpg', 92, 1)");


#testing for grader
conn.execute("INSERT INTO users VALUES(6, 'testpass', 'testuser', 'testuser', 'testuser')");


conn.commit()

conn.close()        