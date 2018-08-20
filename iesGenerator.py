import random
from data import IesData

MODE_CYLINDER = 0
MODE_DOME = 1

def generateCylindrical(lumens, vertRes, horRes, radius, topConeAngle, topConeReflAngle,
		bottomConeAngle, bottomConeReflAngle, reflectivity, shadeAbsorb, shadeNoise, nonShadeNoise):

	points = []

	y = 0
	while y < 359.999:
		x = 0.00
		while x < 180.001:
			if x < bottomConeAngle:
				if nonShadeNoise > 0:
					points.append(random.randrange(int(lumens*(1-nonShadeNoise)), lumens))
				else:
					points.append(lumens)
			elif x < bottomConeReflAngle:
				if shadeNoise > 0:
					points.append(random.randrange(int(lumens*(1-shadeNoise)), lumens)*(1-shadeAbsorb) + (lumens/2*reflectivity))
				else:
					points.append(lumens*(1-shadeAbsorb) + (lumens/2*reflectivity))
			elif x < 180 - topConeReflAngle:
				if shadeNoise > 0:
					points.append(random.randrange(int(lumens*(1-shadeNoise)), lumens)*(1-shadeAbsorb))
				else:
					points.append(lumens*(1-shadeAbsorb))
			elif x < 180 - topConeAngle:
				if shadeNoise > 0:
					points.append(random.randrange(int(lumens*(1-shadeNoise)), lumens)*(1-shadeAbsorb) + (lumens/2*reflectivity))
				else:
					points.append(lumens*(1-shadeAbsorb) + (lumens/2*reflectivity))
			else:
				if nonShadeNoise > 0:
					points.append(random.randrange(int(lumens*(1-nonShadeNoise)), lumens))
				else:
					points.append(lumens)
			x += 180/vertRes
		y += 360/horRes
	d = IesData(lumens, vertRes, horRes, points)
	return d
