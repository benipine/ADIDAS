import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

time_list = open('number', 'r').read().split('\n')
class_list = open('class', 'r').read().split('\n')

################################################

counter = 0
date_list = []
date_count = []


for i in range(len(time_list)-1):
	
	if i == 0:
		date_list.append(time_list[i][0:8])
		date_count.append(1)
		
	elif time_list[i-1][0:8] == time_list[i][0:8]:
		date_count[counter] += 1
		
	else:
		date_list.append(time_list[i][0:8])
		date_count.append(1)
		counter += 1
	
		
print(date_list, date_count)

################################################

counter = 0
type_list = []
type_count = []

for i in range(len(class_list)-1):
	
	if class_list[i] in type_list:
		for k in range(len(type_list)):
			if class_list[i] == type_list[k]:
				type_count[k] += 1
				break
			
	else:
		type_list.append(class_list[i])
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
