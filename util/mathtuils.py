import math
import random
from data.menuitems import *

def interpolate(a, b, x, method):
	if method == "Linear":
		return linearInterpolate(a, b, x)
	elif method == "Smooth":
		return smoothInterpolate(a, b, x)
	elif method == "Sharp":
		return sharpInterpolate(a, b, x)
	elif method == "Root":
		return rootInterpolate(a, b, x)

def linearInterpolate(a, b, x):
	return a * (1 - x) + b * x

def smoothInterpolate(a, b, x):
	ft = x * math.pi
	f = (1 - math.cos(ft)) / 2
	return a * (1 - f) + b * f

def sharpInterpolate(a, b, x):
	return (b - a) * x ** 2 + a

def rootInterpolate(a, b, x):
	return (b - a) * math.sqrt(x) + a

def getNoiseProfile(scale, intensity, seed=1):
	s = seed
	points = []
	for i in range(0, int(scale)):
		random.seed(s)
		if intensity > 0:
			points.append(1-(random.randrange(0,int(intensity*100),1)/100))
		else:
			points.append(1)
		s += 1

	points[0] = 1
	points[len(points)-1] = 1
	return points

def noise(profile, x, method):
	for idx, point in enumerate(profile):
		x1 = idx / len(profile)
		x2 = (idx+1) / len(profile)
		if x1 <= x and x <= x2:
			if idx+1 < len(profile):
				return interpolate(point, profile[idx+1], (x-x1)/(x2-x1), method)
			else:
				return interpolate(point, profile[idx], (x-x1)/(x2-x1), method)
	return 1