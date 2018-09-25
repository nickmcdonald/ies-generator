from tkinter import *
import copy
from preview import *
from modifier.modifierpanel import *
from util.uiGeneric import *
from util.fileutils import *


DEFAULT_LUMENS = 850
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
		self.vResTI = TextInput(self.uiPanel, "Vertical Resolution", self.vRes)
		self.vResTI.grid(column=0, row=1, pady=5)

		self.hRes = IntVar()
		self.hRes.set(DEFAULT_HRES)
		self.hRes.trace_add('write', self.update)
		self.hResTI = TextInput(self.uiPanel, "Horizontal Resolution", self.hRes)
		self.hResTI.grid(column=0, row=2, pady=5)

		self.clamp = BooleanVar()
		self.clamp.set(True)
		CheckboxInput(self.uiPanel, "Clamp Intensity", self.clamp).grid(column=0, row=3, pady=5)
		
		ExportButton(self.uiPanel, self.expIES).grid(column=0,row=4, pady=5)

		self.baseIesType = StringVar()
		self.baseIesType.set(BASEIESTYPES[0])
		self.baseIesType.trace_add('write', self.update)
		IesBaseButton(self.uiPanel, self.baseIesType, BASEIESTYPES).grid(column=0,row=5, pady=5)

		self.preview = PreviewRender(self)
		self.preview.grid(column=0, row=1, rowspan=10)

		self.modifiersPanel = ModifiersPanel(self)
		self.modifiersPanel.grid(column=1, row=0, rowspan=100, sticky=NSEW)

		self.baseIes = None
		self.ies = self.baseIes

		self.modifiersPanel.update()

	def update(self, *args):
		self.setIesBase()
		self.ies = copy.deepcopy(self.baseIes)

		for modifier in self.modifiersPanel.modifiers:
			modifier.apply(self.ies)

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
			self.hRes.set(DEFAULT_HRES)

		if t == "0% Intensity":
			self.baseIes = iesData(
				self.lumens.get(),
				self.vRes.get(),
				self.hRes.get(),0)
			self.lumensTI.setEnabled(True)
			self.vResTI.setEnabled(True)
			self.hResTI.setEnabled(True)
		elif t == "50% Intensity":
			self.baseIes = iesData(
				self.lumens.get(),
				self.vRes.get(),
				self.hRes.get(),0.5)
			self.lumensTI.setEnabled(True)
			self.vResTI.setEnabled(True)
			self.hResTI.setEnabled(True)
		elif t == "100% Intensity":
			self.baseIes = iesData(
				self.lumens.get(),
				self.vRes.get(),
				self.hRes.get(),1)
			self.lumensTI.setEnabled(True)
			self.vResTI.setEnabled(True)
			self.hResTI.setEnabled(True)
		elif t == "Import" and importing:
			self.baseIes = importIES()
			self.lumens.set(self.baseIes.lumens)
			self.vRes.set(self.baseIes.vRes)
			self.hRes.set(self.baseIes.hRes)
			self.lumensTI.setEnabled(False)
			self.vResTI.setEnabled(False)
			self.hResTI.setEnabled(False)


app = EasyIESApplication()
app.mainloop()