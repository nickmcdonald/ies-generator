from tkinter import Canvas
from ies import iesData
from uiGeneric import *
import math


class PreviewRender(PanelFrame):

	def __init__(self, parent, width=500, height=500):
		PanelFrame.__init__(self, parent)
		self.canvas = Canvas(self, width=width, height=height, bg=PANELCOLOR, highlightthickness=0)
		self.canvas.grid(column=0, row=0)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.width = width
		self.height = height
		self.ies = None
		self.clear()

	def renderIESPreview(self, ies=None):
		self.canvas.delete('all')
		if ies != None:
			self.ies = ies
		resAngle = 180 / self.ies.vertRes
		idx = 0
		for point in self.ies.angles[0].points:
			color = fractionToGrey(point.intensity / self.ies.lumens)
			self.canvas.create_polygon([
					self.width/2, self.height/2,
					self.width/2 + self.width/2 * math.sin(math.radians(idx * resAngle)), self.height/2 + self.height/2 * math.cos(math.radians(idx * resAngle)),
					self.width/2 + self.width/2 * math.sin(math.radians((idx+1) * resAngle)), self.height/2 + self.height/2 * math.cos(math.radians((idx+1) * resAngle))
			], outline=color, fill=color, width=0)
			self.canvas.create_polygon([
					self.width/2, self.height/2,
					self.width/2 + -self.width/2 * math.sin(math.radians(idx * resAngle)), self.height/2 + self.height/2 * math.cos(math.radians(idx * resAngle)),
					self.width/2 + -self.width/2 * math.sin(math.radians((idx+1) * resAngle)), self.height/2 + self.height/2 * math.cos(math.radians((idx+1) * resAngle))
			], outline=color, fill=color, width=0)
			idx += 1
			
		self.bind("<Configure>", self.on_resize)
	
	def on_resize(self,event):
		windowx = self.parent.winfo_width() / 2
		windowy = self.parent.winfo_height() / 2
		if windowx < windowy:
			size = windowx
			scale = float(windowx)/self.width
		else:
			size = windowy
			scale = float(windowy)/self.height
		
		self.width = size
		self.height = size

		self.canvas.config(width=size, height=size)
		self.canvas.scale("all",0,0,scale,scale)

		self.renderIESPreview()
	
	def clear(self):
		self.canvas.delete('all')


def fractionToGrey(x):
	if x < 1:
		return "#{:02x}{:02x}{:02x}".format(int(x*255),int(x*255),int(x*255))
	else:
		return "#{:02x}{:02x}{:02x}".format(int(255),int(255),int(255))