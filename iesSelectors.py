import random
from ies import iesData


def full360(ies, ops):
	for op in ops:
		for angle in ies.angles:
			for point in angle.points:
				op.apply(point, {'progression': point.vertAngle / 180})


def angleRange(ies, startAngle, range, ops):
	for op in ops:
		for horAngle in ies.angles:
			for idx, point in enumerate(horAngle.points):
				if point.vertAngle >= startAngle and point.vertAngle <= startAngle + range:
					op.apply(point, {'progression': (point.vertAngle - startAngle) / range})
