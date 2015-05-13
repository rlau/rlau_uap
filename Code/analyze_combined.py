import graphlab as gl

def percentage(list_binary):
	number_first = sum(list_binary)
	total = len(list_binary)
	return float(number_first)/total

def get_first_from_sframe(sframe):
	gwr = get_gwr(sframe)
	ogw = sframe.join(gwr, ['caller', 'receiver'], 'inner')
	fa = ogw.apply(lambda x: 0 if x['first'] == None else x['first'])
	num = sum(fa)
	tot = len(fa)
	return num, tot


def get_gwr(sframe):
	gwr = sframe.groupby('caller', gl.aggregate.ARGMAX('Sum of weight', 'receiver'))
	headers = gwr.column_names()
	gwr = gwr.rename({headers[0]:'caller', headers[1]:'receiver'})
	return gwr

def first(d,c,r):
	return (d[c] == r)

def get_nth_called(sf_path, n):
	sf = gl.SFrame(sf_path)
	num, tot= get_first_from_sframe(sf)
	dist = [num]
	for i in range(1, n):
		d = {}
		gwr = get_gwr(sf)
		for j in range(gwr.num_rows()):
			d[gwr[j]['caller']] = gwr[j]['receiver']
		next_sf = sf[sf.apply(lambda x: not first(d, x['caller'], x['receiver']))]
		dist.append(get_first_from_sframe(next_sf)[0])
		sf = next_sf
	rest = tot - sum(dist)
	dist.append(rest)
	return [x/float(tot) for x in dist]

print '3mi 4/16'
print get_nth_called('~/UAP/combined/2012-04-16_3mi', 8)
print '10mi 4/16'
print get_nth_called('~/UAP/combined/2012-04-16', 8)
print '3mi 6/13 strike 1'
print get_nth_called('~/UAP/combined/2012-06-13', 8)
print '10mi 6/13 strike 1'
print get_nth_called('~/UAP/combined/2012-06-13_10mi', 8)
print '10mi 6/13 strike 2'
print get_nth_called('~/UAP/combined/2012-06-13_10mi_2', 8)
print '3mi 4/10'
print get_nth_called('~/UAP/combined/2012-04-10_3mi', 8)
print '10mi 4/10'
print get_nth_called('~/UAP/combined/2012-04-10_10mi', 8)


