import phone_check as pc
import graphlab as gl
import cProfile

def get_phone_history_from_file(phone_numbers, phonebook, datafile, phonebook_loaded=False, datafile_loaded=False):
	if phonebook_loaded:
		pb = phonebook
	else:
		pb = pc.load_phonebook(phonebook)

	# Iterate through datafile
	if datafile_loaded:
		call_data = datafile
	else:
		call_data = gl.SFrame(datafile)

	call_data = call_data.join(phone_numbers, on='caller', how='inner')
	print 'filtered to relevant numbers'

	valid_numbers = call_data.join(pb, on={'caller':'number'}, how='inner')
	valid_numbers = valid_numbers.join(pb, on={'receiver':'number'}, how='inner')
	print 'filter out routers'

	# Include only callers in phone_numbers
	# Include only calleees in phonebook
	# pn = gl.SFrame(phone_numbers)
	# valid_callers = valid_numbers.join(pn, on='caller', how='inner')

	weights = valid_numbers.groupby(['caller', 'receiver'], operations={'weight':gl.aggregate.COUNT()})
	print 'finished1'
	return weights
	# valid_callers = valid_callees[valid_callees.apply(lambda x: x['receiver'] in pb)]
	# print 'filtered'

	# weights.save(datafile+'_filtered')
	
# def get_phone_numbers(filtered_file):
# 	filtered = gl.SFrame(filtered_file)
# 	return filtered


# filtered_file = '../sframe/2010-01-01_sframe_augmented_filtered'
# phonebook_path = '../phonebook_sf_filtered'
# datafile = '../sframe/2012-01-01_sframe'

# get_phone_history_from_file(filtered_file, phonebook, datafile)