import graphlab as gl

def convert_phonebook_to_sframe(phonebook):

	sf = gl.SFrame.read_csv(phonebook, header=False)
	sf.rename({
			'X1': 'number',
			'X2': 'type',
			'X3': 'location',
			'X4': 't1',
			'X5': 't2'
		})
	return sf

sf = convert_phonebook_to_sframe('../phonebook')
sf.save('../phonebook_sf')