import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import sqlite3
import sys

if len(sys.argv)!=3:
    print("need arguments (start and end date)")
    sys.exit()
    
start_date = sys.argv[1]
end_date = str(int(sys.argv[2])+1)

conn = sqlite3.connect("adidas.db")
cur = conn.cursor()
cur.execute("SELECT * FROM detection_data WHERE date BETWEEN ? AND ?",(start_date+'000000',end_date+'000000'))
rows= cur.fetchall()
conn.close()

#time_list = open('number', 'r').read().split('\n')
#class_list = open('class', 'r').read().split('\n')

################################################

counter = 0
date_list = []
date_count = []


for i in range(len(rows)):
    
	if i == 0:
		date_list.append(rows[i][1][0:8])
		date_count.append(1)
		
	elif rows[i-1][1][0:8] == rows[i][1][0:8]:
		date_count[counter] += 1
		
	else:
		date_list.append(rows[i][1][0:8])
		date_count.append(1)
		counter += 1
	
		
print(date_list, date_count)

################################################

counter = 0
type_list = []
type_count = []

for i in range(len(rows)):
	
	if rows[i][2] in type_list:
		for k in range(len(type_list)):
			if rows[i][2] == type_list[k]:
				type_count[k] += 1
				break
			
	else:
		type_list.append(rows[i][2])
		type_count.append(1)
		
print(type_list, type_count)

################################################

plt.pie(type_count)
plt.legend(type_list)

################################################

plt.savefig('type.jpg')
ax = plt.figure().gca()
ax.yaxis.get_major_locator().set_params(integer=True)

plt.plot(date_list, date_count)
plt.grid(True)
plt.savefig('date.jpg')