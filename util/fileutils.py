from tkinter import filedialog
from data.ies import *
import os
import sys

def resourcePath(rel):
	try:
		basePath = sys._MEIPASS
	except Exception:
		basePath = os.path.abspath(".")
	return os.path.join(basePath, rel)

def exportIES(ies, clamp):
		filename = filedialog.asksaveasfilename(title="Select Export Location", filetypes=(("ies files","*.ies"),("all files","*.*")))
		if filename and len(filename) > 0:
			if filename.endswith(".ies"):
				f = open(filename, 'w+')
			else:
				f = open(filename + ".ies", 'w+')
			print(ies.getIESOutput(clamp), file=f)

def importIES():
	filename = filedialog.askopenfilename(title="Select IES file", filetypes=(("ies files","*.ies"),("all files","*.*")))
	if filename and len(filename) > 0:
		f = open(filename, 'r+')
		return readIESData(f)