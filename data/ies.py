class iesData:

	def __init__(self, lumens, vertRes, horRes):
		self.lumens = lumens
		self.vertRes = vertRes
		self.horRes = horRes
		self.angles = []
		
		y = 0
		while y < 359.999:
			self.angles.append(iesAngle(y, vertRes, 1))
			y += 360/horRes

	def getIESOutput(self, clamp):
		out = "IESNA91\n"
		out += "TILT=NONE\n"
		out += "1 {0} 1 {1} {2} 1 2 1 1 1\n1.0 1.0 0.0\n".format(self.lumens, self.vertRes+1, self.horRes)

		n = 0
		for point in self.angles[0].points:
			out += "{0:.2f} ".format(point.vertAngle)
			if n == 9:
				out += "\n"
				n = 0
			else:
				n = n + 1
		out += "\n\n"

		for angle in self.angles:
			n = 0
			for point in angle.points:
				i = point.intensity
				if clamp and i > 1:
					i = 1
				out += "{0:.2f} ".format(self.lumens * i)
				if n == 9:
					out += "\n"
					n = 0
				else:
					n = n + 1
			out += "\n\n"

		return out


class iesAngle:

	def __init__(self, angle, vertRes, intensity):
		self.angle = angle
		self.vertRes = vertRes
		self.points = []
		x = 0.00
		while x < 180.001:
			self.points.append(iesPoint(angle, x, intensity))
			x += 180/vertRes
		
		self.points[len(self.points)-1].vertAngle = 180
	
	def updateAngle(self, angle):
		self.angle = angle
		for point in self.points:
			point.horAngle = angle


class iesPoint:

	def __init__(self, horAngle, vertAngle, intensity):
		self.horAngle = horAngle
		self.vertAngle = vertAngle
		self.intensity = intensity