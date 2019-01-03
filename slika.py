def slika():
	n = 280
	koordinate = [[0]*n for i in range(n)]
	file = open('a280.txt', 'r')
	for i in range(n):
		koordinate[i] = file.readline().split()
		for j in range(3):
			koordinate[i][j] = float(koordinate[i][j])
	for i in range(n):
		koordinate[i] = koordinate[i][-2:]
	koordinate = np.array(koordinate)

	x, y = koordinate.T
	plt.scatter(x,y)
	plt.show()