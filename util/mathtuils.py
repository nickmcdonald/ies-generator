import math
import random
from util import *

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

def getNoise1DProfile(scale, intensity, seed=1):
	s = seed
	points = []
	for i in range(0, scale):
		random.seed(s)
		if intensity > 0:
			points.append(1-(random.randrange(0,intensity*100,1)/100))
		else:
			points.append(1)
		s += 1

	points[0] = 1
	points[len(points)-1] = 1
	return points

def noise1D(profile, x, method):
	for idx, point in enumerate(profile):
		x1 = idx / len(profile)
		x2 = (idx+1) / len(profile)
		if x1 <= x and x <= x2:
			if idx+1 < len(profile):
				return interpolate(point, profile[idx+1], (x-x1)/(x2-x1), method)
			else:
				return interpolate(point, profile[idx], (x-x1)/(x2-x1), method)
	return 1

def getNoise2DProfile(xScale, yScale, intensity, seed=1):
	s = seed
	points = [[]]
	for x in range(0, xScale):
		for y in range(0, yScale):
			random.seed(s)
			if intensity > 0:
				points[x].append(1-(random.randrange(0,intensity*100,1)/100))
			else:
				points[x].append(0)
			s += 1
		points[x][0] = 1
		points[x][len(points[x])-1] = 1
	return points

def noise2D(profile, x, y, method):
	for ix in range(0, len(profile)):
		for iy in range(0, len(profile[ix])):
			x1 = ix / len(profile)
			x2 = (ix+1) / len(profile)
			y1 = iy / len(profile[ix])
			y2 = (iy+1) / len(profile[ix])
			if x1 <= x and x <= x2 and y1 <= y and y <= y2:
				if ix+1 < len(profile) or iy+1 < len(profile[ix]):
					i1 = interpolate(profile[ix][iy], profile[ix+1][iy], (x-x1)/(x2-x1), method)
					i2 = interpolate(profile[ix][iy+1], profile[ix+1][iy+1], (x-x1)/(x2-x1), method)
					return interpolate(i1, i2, (y-y1)/(y2-y1), method)
				else:
					return 1
	return 1