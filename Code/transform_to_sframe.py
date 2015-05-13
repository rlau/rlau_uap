#!/usr/bin/env python
import sys
import graphlab as gl
from datetime import date
from datetime import timedelta

# path_to_files = "../2010-01-01"
# destination = "../sframe/2010-01-01_sframe"

def transform(path_to_files):
	# load into sframe
	sf = path_to_files

	# rename columns
	sf.rename({
				'X1': 'prepaid',
				'X2':'call_text',
				'X3':'start_time',
				'X4':'end_time',
				'X5':'caller',
				'X6':'caller_tower',
				'X7':'receiver',
				'X8':'receiver_tower',
			   })
	return sf

# sf = transform(path_to_files)
# sf.save(destination)

def save_as_sframe(path_to_files, destination):
	sf = gl.SFrame.read_csv(path_to_files, header=False)
	sf = transform(sf)
	sf.save(destination)
	
def change_many_to_sframe():
	total_range = (date(2012, 10, 7) - date(2012, 3, 20)).days
	dates = [date(2012, 3, 20)+timedelta(i) for i in range(total_range+1)]
	dates = [d.isoformat() for d in dates]
	for d in dates:
		try:
			sf = gl.SFrame.read_csv('/data2/Bruno_full_dataset_decompressed/'+d, header=False)
		except (IOError, RuntimeError):
			continue
		sf = transform(sf)
		sf.save('~/UAP/sframe/'+d+'_sf')


if __name__=="__main__":
	# path_to_files = sys.argv[1]
	# destination = sys.argv[2]

	# sf = transform(path_to_files)
	# sf.save(destination)

	sf = gl.SFrame.read_csv('/data2/Bruno_full_dataset_decompressed/2012-04-16', header=False)
	sf = transform(sf)
	sf.save('~/UAP/sframe/2012-04-16_sf')

	# change_many_to_sframe()



