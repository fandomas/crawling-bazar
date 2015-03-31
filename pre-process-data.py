import matplotlib.pyplot as plt

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



teles=eval(open('file_teles_stract.txt').read())


cates=[]
x=[]
y=[]

for i in teles.items():
	for j in i[1][0]:
		cates.append(j[0])

new_cates=[]
for i in cates:
	temp=""
	
	for j in list(reversed(range(len(i)))):
		
		if is_number(i[j])==True:
			temp=i[:len(temp)-1]
		else:
			new_cates.append(temp)
			
			break

from nltk.probability import FreqDist

sixn=FreqDist(new_cates)

for i in range(len( sixn.items() )):
	x.append(i)

for i in sixn.items():
	y.append(i[1])


#plt.figure(1, figsize=(18,18), dpi=100)
labels = (sixn.keys()[:10])
fracts = y[:10]

plt.pie(fracts, explode=None, labels=labels,
        autopct='%1.2f%%')
plt.show()
