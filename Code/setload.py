f = open('../phonebook_filtered.csv')

s = set([])

for line in f:
	number = line.split(',')[0]
	s.add(number)

print len(s)

in_total = 0
for i in range(9000000000, 9900000000):
	if i in s:
		in_total += 1

print in_total