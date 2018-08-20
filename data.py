class IesData:

	def __init__(self, lumens, vertRes, horRes, points):
		self.lumens = lumens
		self.vertRes = vertRes
		self.horRes = horRes
		self.points = points

	def getIESOutput(self):
		out = "IESNA91\n"
		out += "TILT=NONE\n"
		out += "1 {0} 1 {1} {2} 1 2 1 1 1\n1.0 1.0 0.0\n".format(self.lumens, self.vertRes+1, self.horRes)

		x = 0.00
		n = 0
		while x < 179.999:
			out += "{0:.2f} ".format(x)
			x += 180/self.vertRes
			if n == 9:
				out += "\n"
				n = 0
			else:
				n = n + 1
		out += "180\n"

		for x in self.points:
			out += "{0:.2f} ".format(x)
			if n == 9:
				out += "\n"
				n = 0
			else:
				n = n + 1
		
		return out