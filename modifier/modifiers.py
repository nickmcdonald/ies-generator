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
		self.details = PanelFrame(self)
		self.details.grid(column=0,row=1)
		self.details.columnconfigure(0, weight=1)

		CollapseButton(self.topBar, self.details).grid(column=0,row=0)
		self.topBar.columnconfigure(0, weight=0)

		self.titleLabel = PanelLabel(self.topBar, text="Modifier")
		self.titleLabel.grid(column=1,row=0, sticky=W)
		self.topBar.columnconfigure(1, weight=1)

		self.selection = StringVar()
		self.selection.set("Add Operation")
		self.selection.trace_add('write', self.addOperation)
		OptionButton(self.topBar, "Add Operation", self.selection, OPERATIONS).grid(column=2,row=0)
		self.topBar.columnconfigure(2, weight=1)
		self.operations = []

		self.mix = StringVar()
		self.mix.set(MIXMETHODS[0])
		self.mix.trace_add('write', self.update)
		OptionSelector(self.topBar, self.mix, MIXMETHODS).grid(column=3,row=0)
		self.topBar.columnconfigure(3, weight=1)

		self.visibility = BooleanVar()
		self.visibility.set(True)
		VisibilityButton(self.topBar, self.visibility).grid(column=4,row=0)
		self.topBar.columnconfigure(4, weight=0)

		DeleteButton(self.topBar, self.deleteSelf).grid(column=5,row=0)
		self.topBar.columnconfigure(5, weight=0)

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
				mod = AdjustIntensity(self.details)
			elif s == "Interpolate":
				mod = Interpolate(self.details)
			elif s == "Simple Curve":
				mod = SimpleCurve(self.details)
			elif s == "Noise":
				mod = Noise(self.details)
			
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
		if self.visibility.get() == True:
			angle = self.angle.get()
			range = self.range.get()
			for op in self.operations:
				for horAngle in ies.angles:
					for idx, point in enumerate(horAngle.points):
						if point.vertAngle >= angle and point.vertAngle <= angle + range:
							op.apply(point, mix=self.mix.get(), progression=(point.vertAngle - angle)/range)


class Full360Modifier(Modifier):

	def __init__(self, parent):
		Modifier.__init__(self, parent)

		self.titleLabel["text"] = "Full 360"

	def apply(self, ies):
		if self.visibility.get() == True:
			for op in self.operations:
				for angle in ies.angles:
					for point in angle.points:
						op.apply(point, mix=self.mix.get(), progression=point.vertAngle/180)
