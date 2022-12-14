import sqlite3
import sys

if len(sys.argv)<2:
	print("need an argument (delete->0 (id), viewall->1, making DB file ->2)")
	sys.exit()

conn = sqlite3.connect("adidas.db")

cur = conn.cursor()

if sys.argv[1]=='0':
	cur.execute("DELETE FROM detection_data WHERE id = ?",(int(sys.argv[2]),))
	conn.commit()
elif sys.argv[1]=='1':
	cur.execute("SELECT * FROM detection_data")
	rows= cur.fetchall()
	for row in rows:
		print(row)
elif sys.argv[1]=='2':
	conn.execute('CREATE TABLE detection_data(id INTEGER, date TEXT, category TEXT, detail TEXT)')
else:
	print("wrong argument!")
	sys.exit()
	
conn.close()
