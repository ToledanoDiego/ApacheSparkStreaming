from pyspark import SparkContext 
sc = SparkContext( 'local', 'pyspark') 

#given age_group function
def age_group(age):
	if age < 10 : 
		return '0-10'
	elif age < 20: 
		return '10-20'
	elif age < 30:
		return '20-30' 
	elif age < 40:
		return '30-40' 
	elif age < 50:
		return '40-50' 
	elif age < 60:
		return '50-60' 
	elif age < 70:
		return '60-70' 
	elif age < 80:
		return '70-80' 
	else :
		return '80+'

#given parse_with_age_group function
def parse_with_age_group(data):
	userid,age,gender,occupation,zip = data.split("|")
	return userid, age_group(int(age)),gender,occupation,zip,int(age)

#separate lines according to groups
fs=sc.textFile('file:///home/cloudera/Desktop/Coursework2/u.user')
data_with_age_group=fs.map(parse_with_age_group)

#get the lines where age is between 40 and 50
data_with_age_40_50=data_with_age_group.filter(lambda x: '40-50' in x)

#get the lines where age is between 50 and 60
data_with_age_50_60=data_with_age_group.filter(lambda x: '50-60' in x)

#get the occupations where age is between 40 and 50
tmp=data_with_age_40_50.map(lambda x: x[3]).collect()

x = {}
c = []

#count the number of each occupation
for i in tmp:
    x[i] = x.get(i, 0) + 1

#sort the couting
b=sorted(x.items(), key=lambda kv: kv[1])

#data cleaning
for i in b:
	c.append(i[0])

#get the 10 most frequent occupations
top10_40_50 = c[-10:len(c)]

#get the occupations where age is between 50 and 60
tmp=data_with_age_50_60.map(lambda x: x[3]).collect()

x = {}
c = []

#count the number of each occupation
for i in tmp:
    x[i] = x.get(i, 0) + 1

#sort the couting
b=sorted(x.items(), key=lambda kv: kv[1])

#data cleaning
for i in b:
	c.append(i[0])

#get the 10 most frequent occupations
top10_50_60 = c[-10:len(c)]

#get the intersection of the two frequent lists
top10_40_50 = sc.parallelize(top10_40_50)
top10_50_60 = sc.parallelize(top10_50_60)
sol=top10_40_50.intersection(top10_50_60)

#output
print(sol.collect())
