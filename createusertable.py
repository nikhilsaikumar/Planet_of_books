import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# conn.execute('CREATE TABLE users (email TEXT, password TEXT)')
conn.execute('CREATE TABLE user (username TEXT, email TEXT PRIMARY KEY,password TEXT)')
# conn.execute('DROP TABLE About_Course')
print("Created table successfully!")

conn.close()
