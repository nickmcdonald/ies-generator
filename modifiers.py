from tkinter import *
from ies import iesData
from iesSelectors import *
from operations import *
from uiGeneric import *
import math


class ModifiersPanel(ScrollFrame):

	def __init__(self, parent):
		ScrollFrame.__init__(self, parent)
		self.parent = parent

		self.columnconfigure(0, weight=1)

		self.modifiers = []

		self.rowCounter = 3

		self.selection = StringVar()
		self.selection.set("Add Modifier")
		self.selection.trace_add("write", self.addModifier)

		PanelLabel(self.internalPanel).grid(column=0, row=0)
		OptionSelector(self.internalPanel, "Add Modifier", self.selection,
			["Full 360",
			"Angle Range"]
		).grid(column=0, row=1, sticky=N)
		PanelLabel(self.internalPanel).grid(column=0, row=2)
	
	def addModifier(self, *args):
		s = self.selection.get()
		if s != "Add Modifier":
			if s == "Full 360":
				mod = Full360Modifier(self.internalPanel)
				mod.grid(column=0,row=self.rowCounter, sticky=EW)
				self.modifiers.append(mod)
			elif s == "Angle Range":
				mod = AngleRangeModifier(self.internalPanel)
				mod.grid(column=0,row=self.rowCounter)
				self.modifiers.append(mod)

			self.rowCounter += 1
		self.update()
	
	def removeModifier(self, modifier):
		self.modifiers.remove(modifier)
		self.update()


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
		self.details = PanelFrame(self)
		self.details.grid(column=0,row=1)
		self.details.columnconfigure(0, weight=1)
		self.titleLabel = PanelLabel(self.topBar, text="Modifier")
		self.titleLabel.grid(column=0,row=0,sticky=W)

		self.operations = []
		self.rowCounter = 1

		self.selection = StringVar()
		self.selection.set("Add Operation")
		self.selection.trace_add("write", self.addOperation)

		OptionSelector(self.topBar, "Add Operation", self.selection,
			["Adjust Intensity",
			"Interpolate",
			"Simple Curve"]
		).grid(column=1,row=0)
		DeleteButton(self.topBar, self.deleteSelf).grid(column=2,row=0,padx=20)

		PanelLabel(self).grid(column=0,row=100)

		self.update()
	
	def deleteSelf(self, *args):
		self.parent.parent.parent.removeModifier(self)
		self.destroy()

	def addOperation(self, *args):
		s = self.selection.get()
		if s != "Add Operation":
			if s == "Adjust Intensity":
				mod = AdjustIntensity(self)
				mod.grid(column=0,row=self.rowCounter)
				self.operations.append(mod)
			elif s == "Interpolate":
				mod = Interpolate(self)
				mod.grid(column=0,row=self.rowCounter)
				self.operations.append(mod)
			elif s == "Simple Curve":
				mod = SimpleCurve(self)
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


class Full360Modifier(Modifier):

	def __init__(self, parent):
		Modifier.__init__(self, parent)

		self.titleLabel["text"] = "Full 360"

	def apply(self, ies):
		full360(ies, self.operations)


class AngleRangeModifier(Modifier):

	def __init__(self, parent):
		Modifier.__init__(self, parent)

		self.titleLabel["text"] = "Angle Range"

		self.angle = DoubleVar()
		self.angle.set(45)
		self.angle.trace_add("write", self.update)
		NumberSlider(self.details, "Angle", 0, 180, self.angle).grid(column=0,row=0)

		self.range = DoubleVar()
		self.range.set(45)
		self.range.trace_add("write", self.update)
		NumberSlider(self.details, "Range", 0, 180, self.range).grid(column=0,row=1)

		self.rowCounter = 2

	def apply(self, ies):
		angleRange(ies,
			self.angle.get(),
			self.range.get(),
			self.operations)
