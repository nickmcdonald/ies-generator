import random
from tkinter import *
from tkinter import filedialog

window = Tk()

window.title("IES Generator")

window.geometry('500x600')

mode = "sphere"

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

horResLbl = Label(window, text="Horizontal Resolution ")
horResLbl.grid(column=0, row=2)
horResEnt = Entry(window, width=15)
horResEnt.grid(column=1, row=2)
horResEnt.insert(0, '1')


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
    horRes = int(horResEnt.get())
    radius = 1
    topConeAngle = float(topConeAngleEnt.get())
    topConeReflAngle = float(topConeReflAngleEnt.get())
    bottomConeAngle = float(bottomConeAngleEnt.get())
    bottomConeReflAngle = float(bottomConeReflAngleEnt.get())
    reflectivity = float(reflectivityEnt.get())
    shadeAbsorb = float(shadeAbsorbEnt.get())
    shadeNoise = float(shadeNoiseEnt.get())
    nonShadeNoise = float(nonShadeNoiseEnt.get())
    
    out = "IESNA91\n"
    out += "TILT=NONE\n"
    out += "1 {0} 1 {1} {2} 1 2 {3} {3} {3}\n1.0 1.0 0.0\n".format(lumens, vertRes+1, horRes, radius)

    if mode == "sphere":
            x = 0.00
            n = 0
            while x < 179.999:
                out += "{0:.2f} ".format(x)
                x += 180/vertRes
                if n == 9:
                    out += "\n"
                    n = 0
                else:
                    n = n + 1
            out += "180\n"

            y = 0
            while y < 359.999:
                x = 0.00
                n = 0
                while x < 180.001:
                    if x < bottomConeAngle:
                        if nonShadeNoise > 0:
                            out += "{0:.2f} ".format(random.randrange(int(lumens*(1-nonShadeNoise)), lumens))
                        else:
                            out += "{0:.2f} ".format(lumens)
                    elif x < bottomConeReflAngle:
                        if shadeNoise > 0:
                            out += "{0:.2f} ".format(random.randrange(int(lumens*(1-shadeNoise)), lumens)*(1-shadeAbsorb) + (lumens/2*reflectivity))
                        else:
                            out += "{0:.2f} ".format(lumens*(1-shadeAbsorb) + (lumens/2*reflectivity))
                    elif x < 180 - topConeReflAngle:
                        if shadeNoise > 0:
                            out += "{0:.2f} ".format(random.randrange(int(lumens*(1-shadeNoise)), lumens)*(1-shadeAbsorb))
                        else:
                            out += "{0:.2f} ".format(lumens*(1-shadeAbsorb))
                    elif x < 180 - topConeAngle:
                        if shadeNoise > 0:
                            out += "{0:.2f} ".format(random.randrange(int(lumens*(1-shadeNoise)), lumens)*(1-shadeAbsorb) + (lumens/2*reflectivity))
                        else:
                            out += "{0:.2f} ".format(lumens*(1-shadeAbsorb) + (lumens/2*reflectivity))
                    else:
                        if nonShadeNoise > 0:
                            out += "{0:.2f} ".format(random.randrange(int(lumens*(1-nonShadeNoise)), lumens))
                        else:
                            out += "{0:.2f} ".format(lumens)
                    x += 180/vertRes
                    if n == 9:
                        out += "\n"
                        n = 0
                    else:
                        n = n + 1
                y += 360/horRes

                print(out)

                filename = filedialog.asksaveasfilename(title = "Select file",filetypes = (("ies files","*.ies"),("all files","*.*")))
                if filename.endswith(".ies"):
                    f = open(filename, 'w+')
                else:
                    f = open(filename + ".ies", 'w+')
                print(out, file=f)

genbtn = Button(window,text='Generate', command=generate)
genbtn.grid(column=0,row=11)







window.mainloop()






