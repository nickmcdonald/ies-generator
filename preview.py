from tkinter import Canvas
from data import IesData
import math

class previewRender:

	def __init__(self, window, width, height):
		self.canvas = Canvas(window, width=width, height=height)
		self.canvas.grid(column=0, row=12)
		self.width = width
		self.height = height

	def renderIESPreview(self, ies):
		self.canvas.delete("all")
		resAngle = 180 / ies.vertRes
		idx = 0
		for intensity in ies.points:
			color = percentToGrey(intensity / ies.lumens)
			self.canvas.create_polygon([
					self.width/2, self.height/2,
					self.width/2 + 100 * math.sin(math.radians(idx * resAngle)), self.height/2 + 100 * math.cos(math.radians(idx * resAngle)),
					self.width/2 + 100 * math.sin(math.radians((idx+1) * resAngle)), self.height/2 + 100 * math.cos(math.radians((idx+1) * resAngle))
			], outline=color, fill=color, width=0)
			self.canvas.create_polygon([
					self.width/2, self.height/2,
					self.width/2 + -100 * math.sin(math.radians(idx * resAngle)), self.height/2 + 100 * math.cos(math.radians(idx * resAngle)),
					self.width/2 + -100 * math.sin(math.radians((idx+1) * resAngle)), self.height/2 + 100 * math.cos(math.radians((idx+1) * resAngle))
			], outline=color, fill=color, width=0)
			idx += 1

def percentToGrey(x):
	return "#{:02x}{:02x}{:02x}".format(int(x*255),int(x*255),int(x*255))