from tkinter import *
from ies import *
from .layers import *
from util import *
import math


class LayersPanel(ScrollFrame):

	def __init__(self, parent):
		ScrollFrame.__init__(self, parent)
		self.parent = parent

		self.columnconfigure(0, weight=1)

		self.layers = []

		self.rowCounter = 3

		self.selection = StringVar()
		self.selection.set("Add Layer")
		self.selection.trace_add('write', self.addLayer)
		PanelLabel(self.internalPanel).grid(column=0, row=0)
		OptionButton(self.internalPanel, "Add Layer", self.selection, LAYERS).grid(column=0, row=1, sticky=N)
		PanelLabel(self.internalPanel).grid(column=0, row=2)

	def addLayer(self, *args):
		s = self.selection.get()
		if s != "Add Layer":
			if s == "Full 360":
				mod = Full360(self.internalPanel)
			elif s == "Angle Range":
				mod = VerticalRange(self.internalPanel)

			mod.grid(column=0,row=self.rowCounter, sticky=EW)
			self.layers.append(mod)
			self.rowCounter += 1

		self.update()

	def removeLayer(self, layer):
		self.layers.remove(layer)
		self.update()
