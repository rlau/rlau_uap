import graphlab as gl

# phonebook = "../phonebook_sf_filtered"

def load_phonebook(phonebook, csv=False):
	if csv:
		sf = gl.SFrame.read_csv(phonebook, header=False)
		
		# rename for saving to filter
		if phonebook[-4:] == '.csv':
			phonebook = phonebook[:-4]

		# rename columns
		sf.rename({
			'X1': 'number',
			'X2': 'type',
			'X3': 'location',
			'X4': 't1',
			'X5': 't2'
		})

		# Eliminate "RT", -1, "Short"
		sf = sf[(sf['type'] == 'LL') | (sf['type'] == 'Intl') | (sf['type'] == 'Cell')]
		sf.save(phonebook+'filtered')
	
	else:
		# Load existing sframe phonebook
		sf = gl.SFrame(phonebook)
	return sf
