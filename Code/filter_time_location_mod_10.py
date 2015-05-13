#!/usr/bin/env python

# Use this file



import sys, math
from datetime import *
import graphlab as gl
import graphlab.aggregate as agg
import phone_check as pb


# calls_sframe_file = "../sframe/2010-01-01_sframe_augmented"
# good_attacks = [('2010-01-01', 13.22024043, 45.3018921)]


def filter_by_location(x, attack_location, radius):
	caller_x = x['caller_x']
	caller_y = x['caller_y']
	return distance((caller_x,caller_y), attack_location) < radius

def time_from_stamp(t):
	return datetime.fromtimestamp(int(t))

# def time_filter(x, attack_time, delta):
# 	start_time = datetime.fromtimestamp(float(x['start_time']))
# 	return (start_time > attack_time - delta) and (start_time < attack_time + timedelta(hours=1))

def time_filter(x, attack_time, delta=1):
	start_time = datetime.fromtimestamp(int(x['start_time']))
	return ((start_time > attack_time)&(start_time < attack_time + timedelta(hours=delta)))

def distance(p1, p2): # in mi
	d = distance_on_unit_sphere(p1[0],p1[1],p2[0],p2[1])
	# convert to km  (for miles multiply by 3960) (for km multiply by 6373)  
	return d*3960

def distance_on_unit_sphere(lat1, long1, lat2, long2):
 	## From: http://www.johndcook.com/blog/python_longitude_latitude/

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
	phi1 = (90.0 - lat1)*degrees_to_radians
	phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
	theta1 = long1*degrees_to_radians
	theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
	arc = math.acos(cos)
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
	return arc


# sf = gl.SFrame(calls_sframe_file)

# attack_time = datetime.strptime(good_attacks[0][0], "%Y-%m-%d")
# attack_location = (good_attacks[0][1], good_attacks[0][2])
# sf = sf[sf['caller_x'] and sf['caller_y']]

# # filter records outside radius
# sf = sf[sf.apply(lambda x:  filter_by_location(x, attack_location, radius=3))]

# sf.save(calls_sframe_file + "_filtered")
bp = '/home/rlau/UAP/sframe_augmented/'
end = '_sf_augmented'
phonebook = pb.load_phonebook('~/UAP/phonebook_sf_filtered')
# strikes = [('2012-04-16',1334607000,14.33870029,47.4367981),]
# strikes = [('2012-06-13',1339573500,14.32492434,47.43690185),]
# strikes = [('2012-06-13',1339573500,14.35219955,47.35110092)]
strikes = [('2012-04-10',1334091540,13.22024043,45.3018921)]

for strike in strikes:
	day_of_strike_sframe, time_of_strike = strike[0:2]
	attack_location = (strike[2], strike[3])

	fp = bp+day_of_strike_sframe+end

	
	sf = gl.SFrame(fp)
	sf = sf[sf['caller_x'] and sf['caller_y']]
	print 'filter 1'
	attack_time = time_from_stamp(time_of_strike)

	sf = sf[sf.apply(lambda x: time_filter(x, attack_time, 1))]
	print 'filter 2'
	sf = sf[sf.apply(lambda x: filter_by_location(x, attack_location, radius=3))]
	print 'filter 3'
	sf = sf.join(phonebook, on={'caller':'number'}, how='inner')
	print 'filter 4'
	sf = sf.join(phonebook, on={'receiver':'number'}, how='inner')
	print 'filter 5'
	sf.save(fp+'_filtered_3mi')


# if __name__=="__main__":
#     calls_sframe_file = sys.argv[1]
# 	sf = gl.SFrame(calls_sframe_file)

# 	# attack time
# 	attack_time = datetime.strptime(good_attacks[0][0], "%Y-%m-%d")
# 	attack_location = (good_attacks[0][1], good_attacks[0][2])

# 	# filter by time 
# 	# sf = sf[sf.apply(lambda x: time_filter(x, attack_time, delta = timedelta(days=30)))]

# 	# remove records with no caller tower
# 	sf = sf[sf['caller_x'] and sf['caller_y']]

# 	# filter records outside radius
# 	sf = sf[sf.apply(lambda x: 	filter_by_location(x, attack_location, radius=3))]

# 	sf.save(calls_sframe_file + "_filtered")
