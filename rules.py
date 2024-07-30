def classify(x,cl):
	x=x.lower()
	if cl=='spam' and ('shop' in x or 'buy' in x or 'shop' in x or 'sale' in x or '% off' in x):
		return 'promotion'
	elif cl=='discount':
		return 'promotion'
	elif cl=='shipping':
		return 'invoice'
	else:
		return cl

		
