# python mkgraph.py START_DAY END_DAY

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


################################################

counter = 0
date_list = []
date_count = []
drone_count = []


for i in range(len(rows)):
    
    if i == 0:
        date_list.append(rows[i][1][0:8])
        date_count.append(1)
        if(rows[i][2]=='drone' or rows[i][2]=='airplane'):
            drone_count.append(1)
        else:
            drone_count.append(0)
        
    elif rows[i-1][1][0:8] == rows[i][1][0:8]:
        date_count[counter] += 1
        if(rows[i][2]=='drone' or rows[i][2]=='airplane'):
            drone_count[counter]+=1
            
    else:
        date_list.append(rows[i][1][0:8])
        date_count.append(1)
        counter += 1
        if(rows[i][2]=='drone' or rows[i][2]=='airplane'):
            drone_count.append(1)
        else:
            drone_count.append(0)

print(date_list, date_count)

################################################

ratio_of_day = []
for i in range(counter):
    ratio_of_day.append(int((drone_count[i] / date_count[i])*100))

print(ratio_of_day)

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
plt.savefig('type.jpg')

################################################

ax = plt.figure().gca()
ax.yaxis.get_major_locator().set_params(integer=True)

plt.plot(date_list, date_count)
plt.grid(True)

if len(date_list) <= 7:
	date_size = 9
    
elif len(date_list) <= 14:
	date_size = 4
    
plt.xticks(date_list, date_list, size = date_size)
plt.savefig('date.jpg')
