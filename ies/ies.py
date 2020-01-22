import re

class IesData:

	def __init__(self, lumens, vRes, hRes, val):
		self.lumens = lumens
		self.vRes = vRes
		self.hRes = hRes
		self.angles = []

		y = 0
		while y < 360:
			self.angles.append(IesAngle(y, vRes, val))
			y += 360/hRes

	def getIESOutput(self, clamp):
		out = "IESNA91\n"
		out += "TILT=NONE\n"
		out += "1 {0} 1 {1} {2} 1 2 1 1 1\n1.0 1.0 0.0\n\n".format(self.lumens, len(self.angles[0].points), len(self.angles))

		n = 0
		for point in self.angles[0].points:
			out += "{0:.2f} ".format(point.vAngle)
			if n == 9:
				out += "\n"
				n = 0
			else:
				n = n + 1
		out += "\n\n"

		n = 0
		for angle in self.angles:
			out += "{0:.2f} ".format(angle.hAngle)
			if n == 9:
				out += "\n"
				n = 0
			else:
				n = n + 1
		out += "\n0 \n"

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


class IesAngle:

	def __init__(self, hAngle, vRes, intensity):
		self.hAngle = hAngle
		self.vRes = vRes
		self.points = []
		x = 0.00
		while x <= 180:
			self.points.append(IesPoint(hAngle, x, intensity))
			x += 180/(vRes-1)

		self.points[len(self.points)-1].vAngle = 180

	def updateAngle(self, hAngle):
		self.hAngle = hAngle
		for point in self.points:
			point.hAngle = hAngle


class IesPoint:

	def __init__(self, hAngle, vAngle, intensity):
		self.hAngle = hAngle
		self.vAngle = vAngle
		self.intensity = intensity
		self.mask = 0


def readIESData(inp):

	lines = [line.rstrip('\n') for line in inp]

	version = ""
	details = {}
	settings = ""
	unknownNumbers = ""
	vAngleStartIdx = 0
	hAngleStartIdx = 0
	valsStartIdx = 0
	vAngles = []
	hAngles = []

	for idx, line in enumerate(lines):
		l = line.strip()
		if l.startswith('IES'):
			version = l
		elif line.startswith('['):
			name = l.split(']')[0].replace('[','')
			val = l.split(']')[1]
			details[name] = val
		elif l.startswith("TILT"):
			settings = re.sub(' +', ' ', lines[idx+1]).split(' ')
			unknownNumbers = lines[idx+2]
			vAngleStartIdx = idx + 3

	lumens = int(settings[1])
	factor = float(settings[2])
	vNums = int(settings[3])
	hNums = int(settings[4])
	unit = settings[6]
	# openingSize = tuple(settings[7], settings[8], settings[9])

	ies = IesData(lumens, vNums, hNums, 0)

	vAnglesRead = 0
	for idx in range(vAngleStartIdx, len(lines)):
		vals = lines[idx].split()
		for val in vals:
			vAngles.append(float(val))
			vAnglesRead += 1
		if vAnglesRead >= vNums:
			hAngleStartIdx = idx+1
			break

	hAnglesRead = 0
	for idx in range(hAngleStartIdx, len(lines)):
		vals = lines[idx].split()
		for val in vals:
			hAngles.append(float(val))
			hAnglesRead += 1
		if hAnglesRead >= hNums:
			valsStartIdx = idx+1
			break

	brightest = 0
	valsIdx = 0
	angleIdx = 0
	for idx in range(valsStartIdx, len(lines)):
		vals = lines[idx].split()
		for val in vals:
			if float(val) > brightest:
				brightest = float(val)
			if valsIdx >= vNums:
				valsIdx = 0
				angleIdx +=1
			ies.angles[angleIdx].points[valsIdx].intensity = float(val)
			ies.angles[angleIdx].points[valsIdx].vAngle = vAngles[valsIdx]
			valsIdx += 1

	ies.lumens = brightest
	for angle in ies.angles:
		for point in angle.points:
			point.intensity /= brightest

	return ies
