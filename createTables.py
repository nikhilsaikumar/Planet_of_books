import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

conn.execute('CREATE TABLE books (imgURL TEXT, bookname TEXT,author TEXT,genre TEXT)')

print("Created table successfully!")

conn.close()
