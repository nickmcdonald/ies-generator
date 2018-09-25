from tkinter import *
from ies import *
from .modifiers import *
from util import *
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
		self.selection.trace_add('write', self.addModifier)
		PanelLabel(self.internalPanel).grid(column=0, row=0)
		OptionButton(self.internalPanel, "Add Modifier", self.selection, MODIFIERS).grid(column=0, row=1, sticky=N)
		PanelLabel(self.internalPanel).grid(column=0, row=2)
	
	def addModifier(self, *args):
		s = self.selection.get()
		if s != "Add Modifier":
			if s == "Full 360":
				mod = Full360(self.internalPanel)
			elif s == "Vertical Range":
				mod = VerticalRange(self.internalPanel)
			elif s == "Horizontal Range":
				mod = HorizontalRange(self.internalPanel)
			elif s == "Vertical Horizontal Range":
				mod = VHRange(self.internalPanel)

			mod.grid(column=0,row=self.rowCounter, sticky=EW)
			self.modifiers.append(mod)
			self.rowCounter += 1

		self.update()
	
	def removeModifier(self, modifier):
		self.modifiers.remove(modifier)
		self.update()

