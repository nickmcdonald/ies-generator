from tkinter import *
from tkinter import filedialog
from preview import *
from modifier.modifierpanel import *
from util.uiGeneric import *

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
		self.lumens.set(850)
		self.lumens.trace_add('write', self.update)
		TextInput(self.uiPanel, "Intensity (Lumens)", self.lumens).grid(column=0, row=0, pady=5)

		self.vertRes = IntVar()
		self.vertRes.set(50)
		self.vertRes.trace_add('write', self.update)
		TextInput(self.uiPanel, "Vertical Resolution", self.vertRes).grid(column=0, row=1, pady=5)

		self.horRes = IntVar()
		self.horRes.set(1)
		self.horRes.trace_add('write', self.update)
		# TextInput(self.uiPanel, "Horizontal Resolution", self.horRes).grid(column=0, row=2, pady=5)

		self.clamp = BooleanVar()
		self.clamp.set(True)
		CheckboxInput(self.uiPanel, "Clamp Intensity", self.clamp).grid(column=0, row=3, pady=5)
		
		ExportButton(self.uiPanel, self.export).grid(column=0,row=4, pady=5)

		self.preview = PreviewRender(self)
		self.preview.grid(column=0, row=1, rowspan=10)

		self.modifiersPanel = ModifiersPanel(self)
		self.modifiersPanel.grid(column=1, row=0, rowspan=100, sticky=NSEW)

		self.modifiersPanel.update()

	def update(self, *args):
		self.ies = iesData(
			self.lumens.get(),
			self.vertRes.get(),
			self.horRes.get())

		for modifier in self.modifiersPanel.modifiers:
			modifier.apply(self.ies)

		self.preview.renderIESPreview(self.ies)

	def export(self):
		filename = filedialog.asksaveasfilename(title = "Select file",filetypes = (("ies files","*.ies"),("all files","*.*")))
		if filename and len(filename) > 0:
			if filename.endswith(".ies"):
				f = open(filename, 'w+')
			else:
				f = open(filename + ".ies", 'w+')
			print(self.ies.getIESOutput(self.clamp.get()), file=f)


app = EasyIESApplication()
app.mainloop()