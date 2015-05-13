import graphlab as gl
import phone_check as pc
import phone_history as ph
from datetime import *


def aggregate_call_data(list_of_dates, path_to_data_folder, phone_numbers):
	sframe_paths = [path_to_data_folder + x + '_sf_augmented' for x in list_of_dates]
	sframes = []
	for f in sframe_paths:
		try:
			sf = gl.SFrame(f)
			sframes.append(sf)
		except IOError:
			continue
	pb = pc.load_phonebook('~/UAP/phonebook_sf_filtered')
	# Get list of SFrames with weights from list of dates
	print 'here'
	call_history_sframes = [ph.get_phone_history_from_file(phone_numbers, pb, sf, True, True) for sf in sframes]
	print 'sframes filtered'
	sf1 = call_history_sframes[0]
	print type(sf1)
	for i in range(1,len(call_history_sframes)):
		sf2 = call_history_sframes[i]
		sf1 = sf1.append(sf2)
	sf1 = sf1.groupby(['caller', 'receiver'], gl.aggregate.SUM('weight'))
	return sf1

# Takes SFrame of calls made within first hour of strike, gets first
# person called per caller
# returns sframe mapping callers to first_called
def get_first_called_sf(sframe):
	first_called = sframe.groupby('caller', gl.aggregate.ARGMIN('start_time', 'receiver'))
	current_headers = first_called.column_names()
	first_called = first_called.rename({'caller':'caller', current_headers[1]:'receiver'})
	num_rows = first_called.num_rows()
	first_called.add_column(gl.SArray(data=[1 for x in range(num_rows)], dtype=int), 'first')
	return first_called


def percentage(list_binary):
	number_first = sum(list_binary)
	total = len(list_binary)
	return float(number_first)/total

#	aggregate_data -- sframe of aggregated call data mapping caller number
# 		and receiver number with edgeweight over certain time period
#	first_called_sframe -- sframe of call data mapping for first called receiver
#		number for each caller within certain radius and time of strike.  Should
#		be in format caller | receiver | first, where first is binary (1/0)	
def check_aggregate(aggregate_data, first_called_sframe):
	combined = aggregate_data.join(first_called_sframe, ['caller', 'receiver'], 'left')
	num_calls = sum(combined['Sum of weight'])
	greatest_weight_receiver = combined.groupby('caller', gl.aggregate.ARGMAX('Sum of weight', 'receiver'))
	headers = greatest_weight_receiver.column_names()
	greatest_weight_receiver.rename({headers[0]:'caller', headers[1]:'receiver'})
	only_greatest_weight = combined.join(greatest_weight_receiver, ['caller','receiver'], 'inner')

	combined.save('../combined/'+strike_date.isoformat()+'_3mi')
	
	greater_than_five = only_greatest_weight[only_greatest_weight['Sum of weight'] > 5]
	greater_than_five_first = greater_than_five.apply(lambda x: 0 if x['first']==None else x['first'])
	gt5p = percentage(greater_than_five_first)
	num_filt_callers = len(greater_than_five_first)

	first_array = only_greatest_weight.apply(lambda x: 0 if x['first']==None else x['first'])
	fap = percentage(first_array)
	num_callers = len(first_array)

	return (num_calls,gt5p,num_filt_callers,fap,num_callers)



path_to_data_folder = '~/UAP/sframe_augmented/'
f = '~/UAP/sframe_augmented/2012-04-16_sf_augmented_filtered'
print f
filtered_phone_numbers = gl.SFrame(f)

first_called = get_first_called_sf(filtered_phone_numbers)
strike_date = date(2012,4,16)
total_days = 30
list_of_dates = [(strike_date-timedelta(i)).isoformat() for i in range(total_days)]

aggregate_data = aggregate_call_data(list_of_dates, path_to_data_folder, first_called)
percentage = check_aggregate(aggregate_data, first_called)
print percentage