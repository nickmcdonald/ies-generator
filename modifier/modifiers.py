from data.menuitems import *
from util.uiGeneric import *
from modifier.operations import *


class Modifier(PanelFrame):

	def __init__(self, parent):
		PanelFrame.__init__(self, parent)
		self.parent = parent
		
		self.columnconfigure(0, weight=1)

		self.topBar = PanelFrame(self)
		self.topBar.grid(column=0,row=0)
		self.topBar.columnconfigure(0, weight=1)
		self.topBar.columnconfigure(1, weight=1)
		self.topBar.columnconfigure(2, weight=1)
		self.topBar.columnconfigure(3, weight=1)
		self.details = PanelFrame(self)
		self.details.grid(column=0,row=1)
		self.details.columnconfigure(0, weight=1)
		self.titleLabel = PanelLabel(self.topBar, text="Modifier")
		self.titleLabel.grid(column=0,row=0,sticky=W)

		self.operations = []

		self.selection = StringVar()
		self.selection.set("Add Operation")
		self.selection.trace_add('write', self.addOperation)
		OptionButton(self.topBar, "Add Operation", self.selection, OPERATIONS).grid(column=1,row=0)

		self.method = StringVar()
		self.method.set(MIXMETHODS[0])
		self.method.trace_add('write', self.update)
		OptionSelector(self.topBar, self.method,MIXMETHODS).grid(column=2,row=0)

		DeleteButton(self.topBar, self.deleteSelf).grid(column=3,row=0,padx=20)
		PanelLabel(self).grid(column=0,row=100)

		self.rowCounter = 1

		self.update()
	
	def deleteSelf(self, *args):
		self.parent.parent.parent.removeModifier(self)
		self.destroy()

	def addOperation(self, *args):
		s = self.selection.get()
		if s != "Add Operation":
			if s == "Adjust Intensity":
				mod = AdjustIntensity(self)
			elif s == "Interpolate":
				mod = Interpolate(self)
			elif s == "Simple Curve":
				mod = SimpleCurve(self)
			elif s == "Noise":
				mod = Noise(self)
			
			mod.grid(column=0,row=self.rowCounter)
			self.operations.append(mod)
			self.rowCounter += 1

		self.update()
	
	def removeOperation(self, op):
		self.operations.remove(op)
		self.update()

	def apply(self, ies):
		pass

	def update(self, *args):
		self.parent.parent.update(args)


class AngleRangeModifier(Modifier):

	def __init__(self, parent):
		Modifier.__init__(self, parent)

		self.titleLabel["text"] = "Angle Range"

		self.angle = DoubleVar()
		self.angle.set(45)
		self.angle.trace_add('write', self.update)
		NumberSlider(self.details, "Angle", 0, 180, self.angle).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

		self.range = DoubleVar()
		self.range.set(90)
		self.range.trace_add('write', self.update)
		NumberSlider(self.details, "Range", 0, 180, self.range).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

	def apply(self, ies):
		angle = self.angle.get()
		range = self.range.get()
		for op in self.operations:
			for horAngle in ies.angles:
				for idx, point in enumerate(horAngle.points):
					if point.vertAngle >= angle and point.vertAngle <= angle + range:
						op.apply(point, {'progression': (point.vertAngle - angle) / range})


class Full360Modifier(Modifier):

	def __init__(self, parent):
		Modifier.__init__(self, parent)

		self.titleLabel["text"] = "Full 360"

	def apply(self, ies):
		for op in self.operations:
			for angle in ies.angles:
				for point in angle.points:
					op.apply(point, {'progression': point.vertAngle / 180})
