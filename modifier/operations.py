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
		self.intensity.trace_add('write', self.update)
		NumberSlider(self.details, "Intensity %", 0, 200, self.intensity).grid(column=0,row=0)

		self.update()

	def apply(self, point, options={}):
		point.intensity = point.intensity * (self.intensity.get()/100)


class Interpolate(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Interpolate"

		self.method = StringVar()
		self.method.set(INTERPMETHODS[0])
		self.method.trace_add('write', self.update)
		OptionSelector(self.details, self.method,INTERPMETHODS).grid(column=0,row=0)

		self.startIntensity = DoubleVar()
		self.startIntensity.set(80)
		self.startIntensity.trace_add('write', self.update)
		NumberSlider(self.details, "Top Intensity %", 0, 200, self.startIntensity).grid(column=0,row=1)

		self.endIntensity = DoubleVar()
		self.endIntensity.set(80)
		self.endIntensity.trace_add('write', self.update)
		NumberSlider(self.details, "Bottom Intensity %", 0, 200, self.endIntensity).grid(column=0,row=2)

		self.update()

	def apply(self, point, options={}):
		a = self.endIntensity.get() / 100
		b = self.startIntensity.get() / 100
		y = interpolate(a, b, options['progression'], self.method.get())
		point.intensity = point.intensity * y


class SimpleCurve(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Simple Curve"

		self.method = StringVar()
		self.method.set(INTERPMETHODS[0])
		self.method.trace_add('write', self.update)
		OptionSelector(self.details, self.method, INTERPMETHODS).grid(column=0,row=0)

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

	def apply(self, point, options={}):
		a = self.endIntensity.get() / 100
		b = self.midIntensity.get() / 100
		c = self.startIntensity.get() / 100
		y = 1
		if options['progression'] < 0.5:
			y = interpolate(a, b, options['progression']*2, self.method.get())
		else:
			y = interpolate(c, b, (1-options['progression'])*2, self.method.get())

		point.intensity = point.intensity * y


class Noise(Operation):

	def __init__(self, parent):
		Operation.__init__(self, parent)

		self.titleLabel['text'] = "Noise"

		self.method = StringVar()
		self.method.set(INTERPMETHODS[0])
		self.method.trace_add('write', self.update)
		OptionSelector(self.details, self.method, INTERPMETHODS).grid(column=0,row=0)

		self.scale = DoubleVar()
		self.scale.set(10)
		self.scale.trace_add('write', self.update)
		NumberSlider(self.details, "Noise Scale", 0, 50, self.scale).grid(column=0,row=1)

		self.intensity = DoubleVar()
		self.intensity.set(50)
		self.intensity.trace_add('write', self.update)
		NumberSlider(self.details, "Noise Intensity %", 0, 100, self.intensity).grid(column=0,row=2)

		self.update()

	def apply(self, point, options={}):
		profile = getNoiseProfile(self.scale.get(), self.intensity.get()/100, seed=self.scale.get() + self.intensity.get())
		y = noise(profile, options['progression'], self.method.get())
		point.intensity = point.intensity * y
