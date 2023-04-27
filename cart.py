import sqlite3
conn = sqlite3.connect('database.db')
print("Connected to database successfully")

conn.execute('CREATE TABLE cart (email TEXT,cardname TEXT,url TEXT,PRIMARY KEY(email, cardname, url))')

print("Created table successfully!")

conn.close()
