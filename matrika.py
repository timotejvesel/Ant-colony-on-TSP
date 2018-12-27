import numpy

def explicit_full(file, dimenzija):
	sez = []
	with open(file) as f:
		sez=[float(y) for x in f for y in x.split()]
	sez1 = numpy.array(sez)
	dim = dimenzija
	oblika = (dim, dim)
	razdalja = sez1.reshape(oblika)
	return razdalja
