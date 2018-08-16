from tkinter import *
from tkinter import filedialog
from iesGenerator import *

def initUI(mode):

	if mode == MODE_CYLINDER:
		window.geometry('300x300')

		lumensLbl = Label(window, text="Intensity (Lumens) ")
		lumensLbl.grid(column=0, row=0)
		lumensEnt = Entry(window, width=15)
		lumensEnt.grid(column=1, row=0)
		lumensEnt.insert(0, '850')

		vertResLbl = Label(window, text="Vertical Resolution ")
		vertResLbl.grid(column=0, row=1)
		vertResEnt = Entry(window, width=15)
		vertResEnt.grid(column=1, row=1)
		vertResEnt.insert(0, '50')

		# horResLbl = Label(window, text="Horizontal Resolution ")
		# horResLbl.grid(column=0, row=2)
		# horResEnt = Entry(window, width=15)
		# horResEnt.grid(column=1, row=2)
		# horResEnt.insert(0, '1')

		topConeAngleLbl = Label(window, text="Shade Top Angle ")
		topConeAngleLbl.grid(column=0, row=3)
		topConeAngleEnt = Entry(window, width=15)
		topConeAngleEnt.grid(column=1, row=3)
		topConeAngleEnt.insert(0, '40')

		topConeReflAngleLbl = Label(window, text="Shade Top Reflection Angle ")
		topConeReflAngleLbl.grid(column=0, row=4)
		topConeReflAngleEnt = Entry(window, width=15)
		topConeReflAngleEnt.grid(column=1, row=4)
		topConeReflAngleEnt.insert(0, '55')

		bottomConeAngleLbl = Label(window, text="Shade Bottom Angle ")
		bottomConeAngleLbl.grid(column=0, row=5)
		bottomConeAngleEnt = Entry(window, width=15)
		bottomConeAngleEnt.grid(column=1, row=5)
		bottomConeAngleEnt.insert(0, '50')

		bottomConeReflAngleLbl = Label(window, text="Shade Bottom Reflection Angle ")
		bottomConeReflAngleLbl.grid(column=0, row=6)
		bottomConeReflAngleEnt = Entry(window, width=15)
		bottomConeReflAngleEnt.grid(column=1, row=6)
		bottomConeReflAngleEnt.insert(0, '60')

		reflectivityLbl = Label(window, text="Shade Reflection Intensity ")
		reflectivityLbl.grid(column=0, row=7)
		reflectivityEnt = Entry(window, width=15)
		reflectivityEnt.grid(column=1, row=7)
		reflectivityEnt.insert(0, '0.2')

		shadeAbsorbLbl = Label(window, text="Shade Absorbsion (0-1) ")
		shadeAbsorbLbl.grid(column=0, row=8)
		shadeAbsorbEnt = Entry(window, width=15)
		shadeAbsorbEnt.grid(column=1, row=8)
		shadeAbsorbEnt.insert(0, '0.5')

		shadeNoiseLbl = Label(window, text="Shade Noise (0-1) ")
		shadeNoiseLbl.grid(column=0, row=9)
		shadeNoiseEnt = Entry(window, width=15)
		shadeNoiseEnt.grid(column=1, row=9)
		shadeNoiseEnt.insert(0, '0.06')

		nonShadeNoiseLbl = Label(window, text="Non-Shade Noise (0-1) ")
		nonShadeNoiseLbl.grid(column=0, row=10)
		nonShadeNoiseEnt = Entry(window, width=15)
		nonShadeNoiseEnt.grid(column=1, row=10)
		nonShadeNoiseEnt.insert(0, '0.01')

		def generate():
			lumens = int(lumensEnt.get())
			vertRes = int(vertResEnt.get())
			horRes = 1  # int(horResEnt.get())
			radius = 1
			topConeAngle = float(topConeAngleEnt.get())
			topConeReflAngle = float(topConeReflAngleEnt.get())
			bottomConeAngle = float(bottomConeAngleEnt.get())
			bottomConeReflAngle = float(bottomConeReflAngleEnt.get())
			reflectivity = float(reflectivityEnt.get())
			shadeAbsorb = float(shadeAbsorbEnt.get())
			shadeNoise = float(shadeNoiseEnt.get())
			nonShadeNoise = float(nonShadeNoiseEnt.get())

			out = generateCylindrical(lumens, vertRes, horRes, radius, topConeAngle, topConeReflAngle, bottomConeAngle, bottomConeReflAngle, reflectivity, shadeAbsorb, shadeNoise, nonShadeNoise)
			writeOutToFile(out)

		genbtn = Button(window,text='Generate', command=generate)
		genbtn.grid(column=1,row=11)


def writeOutToFile(out):
	filename = filedialog.asksaveasfilename(title = "Select file",filetypes = (("ies files","*.ies"),("all files","*.*")))
	if filename and len(filename) > 0:
		if filename.endswith(".ies"):
			f = open(filename, 'w+')
		else:
			f = open(filename + ".ies", 'w+')
		print(out, file=f)

window = Tk()
window.title("Easy IES")

initUI(MODE_CYLINDER)

window.mainloop()
