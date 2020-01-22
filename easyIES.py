from tkinter import *
import copy
from preview import *
from layer import *
from ies import *
from util import *


DEFAULT_LUMENS = 500
DEFAULT_VRES = 50
DEFAULT_HRES = 1


class EasyIESApplication(Tk):

	def __init__(self):
		Tk.__init__(self)

		self.title("Easy IES")
		self.geometry('900x600')

		self.configure(bg=BGCOLOR)

		self.ies = None

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.uiPanel = PanelFrame(self)
		self.uiPanel.grid(column=0, row=0)

		self.lumens = IntVar()
		self.lumens.set(DEFAULT_LUMENS)
		self.lumens.trace_add('write', self.update)
		self.lumensTI = TextInput(self.uiPanel, "Intensity (Lumens)", self.lumens)
		self.lumensTI.grid(column=0, row=0, pady=5)

		self.vRes = IntVar()
		self.vRes.set(DEFAULT_VRES)
		self.vRes.trace_add('write', self.update)
		self.vResTI = TextInput(self.uiPanel, "Resolution", self.vRes)
		self.vResTI.grid(column=0, row=1, pady=5)

		self.clamp = BooleanVar()
		self.clamp.set(True)
		CheckboxInput(self.uiPanel, "Clamp Intensity", self.clamp).grid(column=0, row=3, pady=5)

		ExportButton(self.uiPanel, self.expIES).grid(column=0,row=4, pady=5)

		self.baseIesType = StringVar()
		self.baseIesType.set(BASEIESTYPES[2])
		self.baseIesType.trace_add('write', self.selectIesBase)
		IesBaseButton(self.uiPanel, self.baseIesType, BASEIESTYPES).grid(column=0,row=5, pady=5)

		self.preview = PreviewRender(self)
		self.preview.grid(column=0, row=1, rowspan=10)

		self.layersPanel = LayersPanel(self)
		self.layersPanel.grid(column=1, row=0, rowspan=100, sticky=NSEW)

		self.baseIes = None
		self.ies = self.baseIes

		self.layersPanel.update()

	def update(self, *args):
		self.setIesBase()
		self.ies = copy.deepcopy(self.baseIes)

		for layer in self.layersPanel.layers:
			layer.apply(self.ies)

		self.preview.renderIESPreview(self.ies)

	def expIES(self):
		exportIES(self.ies, self.clamp.get())

	def selectIesBase(self, *args):
		self.setIesBase(selecting=True)
		self.update()

	def setIesBase(self, selecting=False):
		t = self.baseIesType.get()
		if selecting:
			self.lumens.set(DEFAULT_LUMENS)
			self.vRes.set(DEFAULT_VRES)

		if t == "0% Intensity":
			self.baseIes = IesData(
				self.lumens.get(),
				self.vRes.get(),
				1,0)
			self.lumensTI.setEnabled(True)
			self.vResTI.setEnabled(True)
		elif t == "50% Intensity":
			self.baseIes = IesData(
				self.lumens.get(),
				self.vRes.get(),
				1,0.5)
			self.lumensTI.setEnabled(True)
			self.vResTI.setEnabled(True)
		elif t == "100% Intensity":
			self.baseIes = IesData(
				self.lumens.get(),
				self.vRes.get(),
				1,1)
			self.lumensTI.setEnabled(True)
			self.vResTI.setEnabled(True)
		# elif t == "Import" and selecting:
		# 	self.baseIes = importIES()
		# 	self.lumens.set(self.baseIes.lumens)
		# 	self.vRes.set(self.baseIes.vRes)
		# 	self.lumensTI.setEnabled(False)
		# 	self.vResTI.setEnabled(False)


app = EasyIESApplication()
app.mainloop()
