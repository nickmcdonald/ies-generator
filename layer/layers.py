from util import *
from .operations import *


class Layer(PanelFrame):

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

		self.titleLabel = PanelLabel(self.topBar, text="Layer")
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
		self.parent.parent.parent.removeLayer(self)
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
			elif s == "Mask":
				mod = Mask(self.details)

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


class VerticalRange(Layer):

	def __init__(self, parent):
		Layer.__init__(self, parent)

		self.titleLabel["text"] = "Angle Range"

		self.vAngle = DoubleVar()
		self.vAngle.set(45)
		self.vAngle.trace_add('write', self.update)
		NumberSlider(self.details, "Angle", 0, 180, self.vAngle).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

		self.vRange = DoubleVar()
		self.vRange.set(90)
		self.vRange.trace_add('write', self.update)
		NumberSlider(self.details, "Range", 0, 180, self.vRange).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

	def apply(self, ies):
		if self.visibility.get() == True:
			vAngle = self.vAngle.get()
			vRange = self.vRange.get()
			for op in self.operations:
				for angle in ies.angles:
					for point in angle.points:
						if point.vAngle >= vAngle and point.vAngle <= vAngle + vRange:
							op.apply(point, mix=self.mix.get(), progression=(point.vAngle - vAngle)/vRange)


class HorizontalRange(Layer):

	def __init__(self, parent):
		Layer.__init__(self, parent)

		self.titleLabel["text"] = "Horizontal Range"

		self.hAngle = DoubleVar()
		self.hAngle.set(45)
		self.hAngle.trace_add('write', self.update)
		NumberSlider(self.details, "Angle", 0, 360, self.hAngle).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

		self.hRange = DoubleVar()
		self.hRange.set(90)
		self.hRange.trace_add('write', self.update)
		NumberSlider(self.details, "Range", 0, 360, self.hRange).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

	def apply(self, ies):
		if self.visibility.get() == True:
			hAngle = self.hAngle.get()
			hRange = self.hRange.get()
			for op in self.operations:
				for angle in ies.angles:
					for point in angle.points:
						if point.hAngle >= hAngle and point.hAngle <= hAngle + hRange:
							op.apply(point, mix=self.mix.get(), progression=(point.hAngle - hAngle)/hRange)


class VHRange(Layer):

	def __init__(self, parent):
		Layer.__init__(self, parent)

		self.titleLabel["text"] = "Vertical Horizontal Range"

		self.vAngle = DoubleVar()
		self.vAngle.set(45)
		self.vAngle.trace_add('write', self.update)
		NumberSlider(self.details, "Vertical Angle", 0, 180, self.vAngle).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

		self.vRange = DoubleVar()
		self.vRange.set(90)
		self.vRange.trace_add('write', self.update)
		NumberSlider(self.details, "Vertical Range", 0, 180, self.vRange).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

		self.hAngle = DoubleVar()
		self.hAngle.set(45)
		self.hAngle.trace_add('write', self.update)
		NumberSlider(self.details, "Horizontal Angle", 0, 360, self.hAngle).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

		self.hRange = DoubleVar()
		self.hRange.set(90)
		self.hRange.trace_add('write', self.update)
		NumberSlider(self.details, "Horizontal Range", 0, 360, self.hRange).grid(column=0,row=self.rowCounter)
		self.rowCounter += 1

	def apply(self, ies):
		if self.visibility.get() == True:
			vAngle = self.vAngle.get()
			vRange = self.vRange.get()
			hAngle = self.hAngle.get()
			hRange = self.hRange.get()
			for op in self.operations:
				for angle in ies.angles:
					for point in angle.points:
						if point.hAngle >= hAngle and point.hAngle <= hAngle + hRange:
							if point.vAngle >= vAngle and point.vAngle <= vAngle + vRange:
								hProgress = (point.hAngle - hAngle)/hRange
								if hProgress > 0.5:
									hProgress = 1 - hProgress
								vProgress = (point.vAngle - vAngle)/vRange
								if vProgress > 0.5:
									vProgress = 1 - vProgress
								op.apply(point, mix=self.mix.get(), progression=(hProgress + vProgress)/2)


class Full360(Layer):

	def __init__(self, parent):
		Layer.__init__(self, parent)

		self.titleLabel["text"] = "Full 360"

	def apply(self, ies):
		if self.visibility.get() == True:
			for op in self.operations:
				for angle in ies.angles:
					for point in angle.points:
						op.apply(point, mix=self.mix.get(), progression=point.vAngle/180)
