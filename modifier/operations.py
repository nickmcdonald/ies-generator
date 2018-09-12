from tkinter import *
import math
from data.ies import *
from data.menuitems import *
from util.uiGeneric import *
from util.mathtuils import *


class Operation(PanelFrame):

	def __init__(self, parent):
		PanelFrame.__init__(self, parent)
		self.parent = parent
		
		self.topBar = PanelFrame(self)
		self.topBar.grid(column=0,row=0)
		self.topBar.columnconfigure(0, weight=1)
		self.topBar.columnconfigure(1, weight=1)
		self.topBar.columnconfigure(2, weight=1)
		self.topBar.columnconfigure(3, weight=1)
		self.topBar.columnconfigure(4, weight=1)
		self.details = PanelFrame(self)
		self.details.grid(column=0,row=1)

		CollapseButton(self.topBar, self.details).grid(column=0, row=0, sticky=E)
		self.titleLabel = PanelLabel(self.topBar, text="Operation")
		self.titleLabel.grid(column=1, row=0, sticky=W)

		self.visibility = BooleanVar()
		self.visibility.set(True)
		VisibilityButton(self.topBar, self.visibility).grid(column=3,row=0, sticky=E)

		DeleteButton(self.topBar, command=self.deleteSelf).grid(column=4, row=0, sticky=W)
		
		self.update()

	def mix(self, point, value, mix):
		if mix == "Multiply":
			point.intensity *= value
		elif mix == "Override":
			point.intensity = value
		elif mix == "Divide":
			if value != 0:
				point.intensity /= value
			else:
				point.intensity = 1
		elif mix == "Add":
			point.intensity += value
		elif mix == "Subtract":
			point.intensity -= value
		elif mix == "Min":
			point.intensity = min(point.intensity, value)
		elif mix == "Max":
			point.intensity = max(point.intensity, value)
		if point.intensity < 0:
			point.intensity = 0

	def deleteSelf(self, *args):
		self.parent.parent.removeOperation(self)
		self.destroy()

	def update(self, *args):
		self.parent.parent.update(args)


class AdjustIntensity(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Adjust Intensity"

		self.intensity = DoubleVar()
		self.intensity.set(80)
		self.intensity.trace_add('write', self.update)
		NumberSlider(self.details, "Intensity %", 0, 200, self.intensity).grid(column=0,row=0)

		self.update()

	def apply(self, point, mix=MIXMETHODS[0], progression=0):
		if self.visibility.get() == True:
			self.mix(point, self.intensity.get()/100, mix)


class Interpolate(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Interpolate"

		self.method = StringVar()
		self.method.set(INTERPMETHODS[0])
		self.method.trace_add('write', self.update)
		OptionSelector(self.topBar, self.method,INTERPMETHODS).grid(column=2,row=0)

		self.startIntensity = DoubleVar()
		self.startIntensity.set(80)
		self.startIntensity.trace_add('write', self.update)
		NumberSlider(self.details, "Top Intensity %", 0, 200, self.startIntensity).grid(column=0,row=1)

		self.endIntensity = DoubleVar()
		self.endIntensity.set(80)
		self.endIntensity.trace_add('write', self.update)
		NumberSlider(self.details, "Bottom Intensity %", 0, 200, self.endIntensity).grid(column=0,row=2)

		self.update()

	def apply(self, point, mix=MIXMETHODS[0], progression=0):
		if self.visibility.get() == True:
			a = self.endIntensity.get() / 100
			b = self.startIntensity.get() / 100
			y = interpolate(a, b, progression, self.method.get())
			self.mix(point, y, mix)


class SimpleCurve(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Simple Curve"

		self.method = StringVar()
		self.method.set(INTERPMETHODS[0])
		self.method.trace_add('write', self.update)
		OptionSelector(self.topBar, self.method, INTERPMETHODS).grid(column=2,row=0)

		self.startIntensity = DoubleVar()
		self.startIntensity.set(100)
		self.startIntensity.trace_add('write', self.update)
		NumberSlider(self.details, "Top Intensity %", 0, 200, self.startIntensity).grid(column=0,row=1)

		self.midIntensity = DoubleVar()
		self.midIntensity.set(70)
		self.midIntensity.trace_add('write', self.update)
		NumberSlider(self.details, "Middle Intensity %", 0, 200, self.midIntensity).grid(column=0,row=2)

		self.endIntensity = DoubleVar()
		self.endIntensity.set(100)
		self.endIntensity.trace_add('write', self.update)
		NumberSlider(self.details, "Bottom Intensity %", 0, 200, self.endIntensity).grid(column=0,row=3)

		self.update()

	def apply(self, point, mix=MIXMETHODS[0], progression=0):
		if self.visibility.get() == True:
			a = self.endIntensity.get() / 100
			b = self.midIntensity.get() / 100
			c = self.startIntensity.get() / 100
			y = 1
			if progression < 0.5:
				y = interpolate(a, b, progression*2, self.method.get())
			else:
				y = interpolate(c, b, (1-progression)*2, self.method.get())
			self.mix(point, y, mix)


class Noise(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Noise"

		self.method = StringVar()
		self.method.set(INTERPMETHODS[0])
		self.method.trace_add('write', self.update)
		OptionSelector(self.topBar, self.method, INTERPMETHODS).grid(column=2,row=0)

		self.scale = DoubleVar()
		self.scale.set(10)
		self.scale.trace_add('write', self.update)
		NumberSlider(self.details, "Noise Scale", 0, 50, self.scale).grid(column=0,row=1)

		self.intensity = DoubleVar()
		self.intensity.set(50)
		self.intensity.trace_add('write', self.update)
		NumberSlider(self.details, "Noise Intensity %", 0, 100, self.intensity).grid(column=0,row=2)

		self.update()

	def apply(self, point, mix=MIXMETHODS[0], progression=0):
		if self.visibility.get() == True:
			profile = getNoiseProfile(self.scale.get(), self.intensity.get()/100, seed=self.scale.get() + self.intensity.get())
			y = noise(profile, progression, self.method.get())
			self.mix(point, y, mix)
