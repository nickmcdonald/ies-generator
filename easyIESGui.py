from tkinter import *
from tkinter import filedialog
from iesGenerator import *
from preview import previewRender

class EasyIESApplication:

	def __init__(self):
	
		self.window = Tk()
		self.window.title("Easy IES")

		self.lumens = IntVar()
		self.vertRes = IntVar()
		self.horRes = IntVar()
		self.radius = IntVar()
		self.topConeAngle = DoubleVar()
		self.topConeReflAngle = DoubleVar()
		self.bottomConeAngle = DoubleVar()
		self.bottomConeReflAngle = DoubleVar()
		self.reflectivity = DoubleVar()
		self.shadeAbsorb = DoubleVar()
		self.shadeNoise = DoubleVar()
		self.nonShadeNoise = DoubleVar()

		self.lumens.set(850)
		self.vertRes.set(50)
		self.horRes.set(1)
		self.radius.set(1)
		self.topConeAngle.set(45.0)
		self.topConeReflAngle.set(55)
		self.bottomConeAngle.set(50)
		self.bottomConeReflAngle.set(60)
		self.reflectivity.set(0.2)
		self.shadeAbsorb.set(0.5)
		self.shadeNoise.set(0.05)
		self.nonShadeNoise.set(0.01)

		self.lumens.trace_add("write", self.update)
		self.vertRes.trace_add("write", self.update)
		self.horRes.trace_add("write", self.update)
		self.radius.trace_add("write", self.update)
		self.topConeAngle.trace_add("write", self.update)
		self.topConeReflAngle.trace_add("write", self.update)
		self.bottomConeAngle.trace_add("write", self.update)
		self.bottomConeReflAngle.trace_add("write", self.update)
		self.reflectivity.trace_add("write", self.update)
		self.shadeAbsorb.trace_add("write", self.update)
		self.shadeNoise.trace_add("write", self.update)
		self.nonShadeNoise.trace_add("write", self.update)

		self.preview = previewRender(self.window, 200,200)
		self.ies = None

		self.initUI(MODE_CYLINDER)
		self.update()
		self.window.mainloop()


	def update(self, *args):
		self.ies = generateCylindrical(
			self.lumens.get(),
			self.vertRes.get(),
			self.horRes.get(),
			self.radius.get(),
			self.topConeAngle.get(),
			self.topConeReflAngle.get(),
			self.bottomConeAngle.get(),
			self.bottomConeReflAngle.get(),
			self.reflectivity.get(),
			self.shadeAbsorb.get(),
			self.shadeNoise.get(),
			self.nonShadeNoise.get())

		self.preview.renderIESPreview(self.ies)

	def save(self):
		filename = filedialog.asksaveasfilename(title = "Select file",filetypes = (("ies files","*.ies"),("all files","*.*")))
		if filename and len(filename) > 0:
			if filename.endswith(".ies"):
				f = open(filename, 'w+')
			else:
				f = open(filename + ".ies", 'w+')
			print(self.ies.getIESOutput(), file=f)


	def initUI(self, mode):

		if mode == MODE_CYLINDER:

			self.window.geometry('320x500')

			lumensLbl = Label(self.window, text="Intensity (Lumens) ")
			lumensLbl.grid(column=0, row=0)
			lumensEnt = Entry(self.window, width=15, textvariable=self.lumens)
			lumensEnt.grid(column=1, row=0)

			vertResLbl = Label(self.window, text="Vertical Resolution ")
			vertResLbl.grid(column=0, row=1)
			vertResEnt = Entry(self.window, width=15, textvariable=self.vertRes)
			vertResEnt.grid(column=1, row=1)

			# horResLbl = Label(window, text="Horizontal Resolution ")
			# horResLbl.grid(column=0, row=2)
			# horResEnt = Entry(window, width=15)
			# horResEnt.grid(column=1, row=2)
			# horResEnt.insert(0, '1')

			topConeAngleLbl = Label(self.window, text="Shade Top Angle ")
			topConeAngleLbl.grid(column=0, row=3)
			topConeAngleEnt = Entry(self.window, width=15, textvariable=self.topConeAngle)
			topConeAngleEnt.grid(column=1, row=3)

			topConeReflAngleLbl = Label(self.window, text="Shade Top Reflection Angle ")
			topConeReflAngleLbl.grid(column=0, row=4)
			topConeReflAngleEnt = Entry(self.window, width=15, textvariable=self.topConeReflAngle)
			topConeReflAngleEnt.grid(column=1, row=4)

			bottomConeAngleLbl = Label(self.window, text="Shade Bottom Angle ")
			bottomConeAngleLbl.grid(column=0, row=5)
			bottomConeAngleEnt = Entry(self.window, width=15, textvariable=self.bottomConeAngle)
			bottomConeAngleEnt.grid(column=1, row=5)

			bottomConeReflAngleLbl = Label(self.window, text="Shade Bottom Reflection Angle ")
			bottomConeReflAngleLbl.grid(column=0, row=6)
			bottomConeReflAngleEnt = Entry(self.window, width=15, textvariable=self.bottomConeReflAngle)
			bottomConeReflAngleEnt.grid(column=1, row=6)

			reflectivityLbl = Label(self.window, text="Shade Reflection Intensity ")
			reflectivityLbl.grid(column=0, row=7)
			reflectivityEnt = Entry(self.window, width=15, textvariable=self.reflectivity)
			reflectivityEnt.grid(column=1, row=7)

			shadeAbsorbLbl = Label(self.window, text="Shade Absorbsion (0-1) ")
			shadeAbsorbLbl.grid(column=0, row=8)
			shadeAbsorbEnt = Entry(self.window, width=15, textvariable=self.shadeAbsorb)
			shadeAbsorbEnt.grid(column=1, row=8)

			shadeNoiseLbl = Label(self.window, text="Shade Noise (0-1) ")
			shadeNoiseLbl.grid(column=0, row=9)
			shadeNoiseEnt = Entry(self.window, width=15, textvariable=self.shadeNoise)
			shadeNoiseEnt.grid(column=1, row=9)

			nonShadeNoiseLbl = Label(self.window, text="Non-Shade Noise (0-1) ")
			nonShadeNoiseLbl.grid(column=0, row=10)
			nonShadeNoiseEnt = Entry(self.window, width=15, textvariable=self.nonShadeNoise)
			nonShadeNoiseEnt.grid(column=1, row=10)

			saveBtn = Button(self.window,text='Save', command=self.save)
			saveBtn.grid(column=1,row=11)

EasyIESApplication()