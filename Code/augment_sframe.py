#!/usr/bin/env python
import sys
import graphlab as gl
from datetime import date
from datetime import timedelta

tower_file = "../tower_locations.tsv"
towermap_file = "../tower_map.txt"
# calls_sframe_file = "../sframe/2010-01-01_sframe"

def augment(path_to_sframe, tower_map=False):
	# import graphlab as gl
	# load sframe
	sf = gl.SFrame(path_to_sframe)
	print "loaded sframe"

	# get locations
	if not tower_map:
		tower_map = load_tower_locations(tower_file, towermap_file)

	caller_x = sf.apply(lambda x: tower_map.get(x['caller_tower'], (None,None))[0])
	caller_y = sf.apply(lambda x: tower_map.get(x['caller_tower'], (None,None))[1])
	receiver_x = sf.apply(lambda x: tower_map.get(x['receiver_tower'], (None,None))[0])
	receiver_y = sf.apply(lambda x: tower_map.get(x['receiver_tower'], (None,None))[1])

	print len(caller_x)
	print len(caller_y)
	print len(receiver_x)
	print len(receiver_y)

	location_sf = gl.SFrame({
								'caller_x':caller_x, 
								'caller_y':caller_y, 
								'receiver_x':receiver_x, 
								'receiver_y':receiver_y})

	print "extracted location data."
	sf.add_columns(location_sf)
	# print "saving sframe to: " + path_to_sframe + "_augmented"
	# sf.save(path_to_sframe + "_augmented")
	print "done."

	return sf
	


def load_tower_locations(filename, towermap_file):

	#TODO: we use -1 for missing data in multiple places. 
	# we need to make sure that this does not break anything

	##  load tower_map
	# tower_map: dict{tower_id, int_id}
	tower_map = {}
	fmap = open(towermap_file)
	while True:
		l = fmap.readline().strip()

		if not l:
			break

		tokens = l.split(" ")
		tower_map[tokens[0]] = int(tokens[1])


	f = open(filename)
	f.readline()

	# dict{int_id, (x,y)}
	location_map = {}
	while True:
		l = f.readline().strip()

		if not l:
			break

		tokens = l.split("\t")
		int_id = tower_map.get(tokens[0], -1)
		
		latitude = float(tokens[1]) if (tokens[1] != "#N/A") else None
		longitude = float(tokens[2]) if (tokens[1] != "#N/A") else None
		
		# store only determined locations
		if latitude and longitude:
			location_map[int_id] = (latitude, longitude)

		# if (int_id == -1):
		# 	location_map[int_id] = (None, None)		

		
	del location_map[-1]			
	return location_map

a = load_tower_locations(tower_file, towermap_file)
# print len(a.keys())
# print a[a.keys()[1]]

sf = gl.SFrame('~/UAP/sframe/2012-04-16_sf')
sf = augment(sf, a)
print ('saving')
sf.save('~/UAP/sframe_augmented/2012-04-16_sf_augmented')

def change_many_to_sframe(tower_map):
	total_range = (date(2012, 10, 7) - date(2012, 4, 10)).days
	dates = [date(2012, 4, 10)+timedelta(i) for i in range(total_range+1)]
	dates = [d.isoformat()+'_sf' for d in dates]
	for d in dates:
		print d
		try:
			sf = gl.SFrame('~/UAP/sframe/'+d)
		except (IOError, RuntimeError):
			continue
		sf = augment(sf, tower_map)
		print 'saving '+d
		sf.save('~/UAP/sframe_augmented/'+d+'_augmented')

# change_many_to_sframe(a)

# sf = augment(calls_sframe_file)

# print "saving sframe to: " + calls_sframe_file + "_augmented"
# sf.save(calls_sframe_file + "_augmented")
	

# if __name__=="__main__":
# 	calls_sframe_file = sys.argv[1]
# 	sf = augment(calls_sframe_file)	

