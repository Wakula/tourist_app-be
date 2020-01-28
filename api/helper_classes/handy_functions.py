def try_except(exp1, exp2, *args):
	'''Will return result of expression that was successfull, or False in other case.
	exp1(*args) or exp2(*args) or False'''
	try:
		return exp1(*args)
	except:
		try:
			return exp2(*args)
		except:
			return False