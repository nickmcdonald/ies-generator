from tkinter import *
import math
from ies import iesPoint
from uiGeneric import *

class Operation(PanelFrame):

	def __init__(self, parent):
		PanelFrame.__init__(self, parent)
		self.parent = parent
		
		self.topBar = PanelFrame(self)
		self.topBar.grid(column=0,row=0)
		self.topBar.columnconfigure(0, weight=1)
		self.topBar.columnconfigure(1, weight=1)
		self.topBar.columnconfigure(2, weight=1)
		self.details = PanelFrame(self)
		self.details.grid(column=0,row=1)
		self.titleLabel = PanelLabel(self.topBar, text="Operation")
		self.titleLabel.grid(column=0, row=0, sticky=E)

		DeleteButton(self.topBar, command=self.deleteSelf).grid(column=2, row=0, sticky=W)
		
		self.update()

	def apply(self, point, options={}):
		pass

	def deleteSelf(self, *args):
		self.parent.removeOperation(self)
		self.destroy()

	def update(self, *args):
		self.parent.update(args)


class AdjustIntensity(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Adjust Intensity"

		self.intensity = DoubleVar()
		self.intensity.set(80)
		self.intensity.trace_add("write", self.update)

		NumberSlider(self.details, "Intensity %", 0, 200, self.intensity).grid(column=0,row=0)

		self.update()

	def apply(self, point, options={}):
		point.intensity = point.intensity * (self.intensity.get()/100)


class Interpolate(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Interpolate"

		self.startIntensity = DoubleVar()
		self.startIntensity.set(80)
		self.startIntensity.trace_add("write", self.update)

		NumberSlider(self.details, "Top Intensity %", 0, 200, self.startIntensity).grid(column=0,row=0)

		self.EndIntensity = DoubleVar()
		self.EndIntensity.set(80)
		self.EndIntensity.trace_add("write", self.update)

		NumberSlider(self.details, "Bottom Intensity %", 0, 200, self.EndIntensity).grid(column=0,row=1)

		self.update()

	def apply(self, point, options={}):
		y0 = self.EndIntensity.get() / 100
		y1 = self.startIntensity.get() / 100
		x = options['progression']
		y = y0 * (1-x) + y1 * x
		point.intensity = point.intensity * y


class SimpleCurve(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Interpolate"

		self.startIntensity = DoubleVar()
		self.startIntensity.set(80)
		self.startIntensity.trace_add("write", self.update)

		NumberSlider(self.details, "Top Intensity %", 0, 200, self.startIntensity).grid(column=0,row=0)

		self.midIntensity = DoubleVar()
		self.midIntensity.set(80)
		self.midIntensity.trace_add("write", self.update)

		NumberSlider(self.details, "Middle Intensity %", 0, 200, self.midIntensity).grid(column=0,row=1)

		self.endIntensity = DoubleVar()
		self.endIntensity.set(80)
		self.endIntensity.trace_add("write", self.update)

		NumberSlider(self.details, "Bottom Intensity %", 0, 200, self.endIntensity).grid(column=0,row=2)

		self.update()

	def apply(self, point, options={}):
		y0 = self.endIntensity.get() / 100
		y1 = self.midIntensity.get() / 100
		y2 = self.startIntensity.get() / 100
		if options['progression'] < 0.5:
			x = options['progression']
			y = y0 * (1-x) + y1 * x
		else:
			x = options['progression']
			y = y1 * (1-x) + y2 * x

		point.intensity = point.intensity * y
