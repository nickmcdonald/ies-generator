import random

MODE_CYLINDER = 0
MODE_DOME = 1

def generateCylindrical(lumens, vertRes, horRes, radius, topConeAngle, topConeReflAngle,
		bottomConeAngle, bottomConeReflAngle, reflectivity, shadeAbsorb, shadeNoise, nonShadeNoise):

	out = "IESNA91\n"
	out += "TILT=NONE\n"
	out += "1 {0} 1 {1} {2} 1 2 {3} {3} {3}\n1.0 1.0 0.0\n".format(lumens, vertRes+1, horRes, radius)

	x = 0.00
	n = 0
	while x < 179.999:
		out += "{0:.2f} ".format(x)
		x += 180/vertRes
		if n == 9:
			out += "\n"
			n = 0
		else:
			n = n + 1
	out += "180\n"

	y = 0
	while y < 359.999:
		x = 0.00
		n = 0
		while x < 180.001:
			if x < bottomConeAngle:
				if nonShadeNoise > 0:
					out += "{0:.2f} ".format(random.randrange(int(lumens*(1-nonShadeNoise)), lumens))
				else:
					out += "{0:.2f} ".format(lumens)
			elif x < bottomConeReflAngle:
				if shadeNoise > 0:
					out += "{0:.2f} ".format(random.randrange(int(lumens*(1-shadeNoise)), lumens)*(1-shadeAbsorb) + (lumens/2*reflectivity))
				else:
					out += "{0:.2f} ".format(lumens*(1-shadeAbsorb) + (lumens/2*reflectivity))
			elif x < 180 - topConeReflAngle:
				if shadeNoise > 0:
					out += "{0:.2f} ".format(random.randrange(int(lumens*(1-shadeNoise)), lumens)*(1-shadeAbsorb))
				else:
					out += "{0:.2f} ".format(lumens*(1-shadeAbsorb))
			elif x < 180 - topConeAngle:
				if shadeNoise > 0:
					out += "{0:.2f} ".format(random.randrange(int(lumens*(1-shadeNoise)), lumens)*(1-shadeAbsorb) + (lumens/2*reflectivity))
				else:
					out += "{0:.2f} ".format(lumens*(1-shadeAbsorb) + (lumens/2*reflectivity))
			else:
				if nonShadeNoise > 0:
					out += "{0:.2f} ".format(random.randrange(int(lumens*(1-nonShadeNoise)), lumens))
				else:
					out += "{0:.2f} ".format(lumens)
			x += 180/vertRes
			if n == 9:
				out += "\n"
				n = 0
			else:
				n = n + 1
		y += 360/horRes

	return out
