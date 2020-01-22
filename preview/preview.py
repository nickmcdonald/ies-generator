from tkinter import Canvas
from ies import *
from util import *
import math


class PreviewRender(PanelFrame):

	def __init__(self, parent, width=500, height=500):
		PanelFrame.__init__(self, parent)
		self.canvas = Canvas(self, width=width, height=height, bg=PANELCOLOR, highlightthickness=0)
		self.canvas.grid(column=0, row=1)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.width = width
		self.height = height
		self.ies = None
		self.clear()

		self.hAngle = IntVar()
		self.hAngle.set(0)
		self.hAngle.trace_add('write', self.update)
		# self.slider = NumberSlider(self, "View Angle", 0, 360, self.hAngle).grid(column=0,row=0)

	def renderIESPreview(self, ies=None):
		self.canvas.delete('all')
		if ies != None:
			self.ies = ies

		a = self.hAngle.get()
		oa = a + 180
		if oa > 360:
			oa -= 360

		a1 = closest(a, self.ies.angles)
		a2 = closest(oa, self.ies.angles)

		for idx, point in enumerate(a1.points):
			color = fractionToGrey(point.intensity)
			try:
				nextAngle = a1.points[idx+1].vAngle
			except:
				nextAngle = 180
			self.canvas.create_polygon([
					self.width/2, self.height/2,
					self.width/2 + self.width/2 * math.sin(math.radians(point.vAngle)), self.height/2 + self.height/2 * math.cos(math.radians(point.vAngle)),
					self.width/2 + self.width/2 * math.sin(math.radians(nextAngle)), self.height/2 + self.height/2 * math.cos(math.radians(nextAngle))
			], outline=color, fill=color, width=0)
			idx += 1

		for idx, point in enumerate(a2.points):
			color = fractionToGrey(point.intensity)
			try:
				nextAngle = a2.points[idx+1].vAngle
			except:
				nextAngle = 180
			self.canvas.create_polygon([
					self.width/2, self.height/2,
					self.width/2 + -self.width/2 * math.sin(math.radians(point.vAngle)), self.height/2 + self.height/2 * math.cos(math.radians(point.vAngle)),
					self.width/2 + -self.width/2 * math.sin(math.radians(nextAngle)), self.height/2 + self.height/2 * math.cos(math.radians(nextAngle))
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

	def update(self, *args):
		self.renderIESPreview()

	def clear(self):
		self.canvas.delete('all')


def closest(angle, angles):
	c = angles[0]
	for a in angles:
		if abs (angle - a.hAngle) < abs (angle - c.hAngle):
			c = a
	return c


def fractionToGrey(x):
	if x < 1:
		return "#{:02x}{:02x}{:02x}".format(int(x*255),int(x*255),int(x*255))
	else:
		return "#{:02x}{:02x}{:02x}".format(int(255),int(255),int(255))
