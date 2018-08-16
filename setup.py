from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\nickm\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\nickm\AppData\Local\Programs\Python\Python36\tcl\tk8.6'

base = None

executables = [Executable("easyIESGui.py", base=base)]

packages = ["idna","tkinter","easyIESGui","iesGenerator","random"]
options = {
	'build_exe': {
		'packages':packages,
		"include_files": ["lib/tcl86t.dll", "lib/tk86t.dll"]
	},
}

setup(
	name = "<EasyIES>",
	options = options,
	version = "1.0",
	description = 'A program for generating IES files',
	executables = executables
)