from tkinter import *

BGCOLOR = "#444444"
PANELCOLOR = "#333333"
BUTTONCOLOR = "#777777"

TEXTCOLOR = "#ffffff"

class BaseFrame(Frame):
	def __init__(self, parent=None, height=0):
		Frame.__init__(self, parent, bg=BGCOLOR, height=height)
		self.parent = parent
		self.grid(sticky=EW)


class PanelFrame(Frame):
	def __init__(self, parent=None, bg=PANELCOLOR):
		Frame.__init__(self, parent, bg=bg)
		self.parent = parent
		self.grid(sticky=NSEW, pady=2.5, padx=5)
		self.columnconfigure(0, weight=1)


class ScrollFrame(PanelFrame):
	def __init__(self, parent):
		PanelFrame.__init__(self, parent)
		
		self.bind("<Configure>", self.onFrameConfigure)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=0)
		self.rowconfigure(0, weight=1)
		self.canvas = ScrollCanvas(self)
		self.canvas.grid(column=0, row=0, rowspan=100, sticky=NSEW)
		self.canvas.bind("<Configure>", self.frameWidth)
		self.internalPanel = PanelFrame(self.canvas)
		self.internalPanel.grid(column=0, row=0, sticky=NSEW)
		self.internalPanel.columnconfigure(0, weight=1)
		self.internalPanel.rowconfigure(0, weight=1)
		self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
		self.vsb.grid(column=1, row=0, rowspan=10, sticky=NS)
		self.canvas.create_window(0, 0, window=self.internalPanel, anchor=N, tags="internalPanel")
		self.canvas.configure(yscrollcommand=self.vsb.set, bg=PANELCOLOR, highlightthickness=0)
	
	def onFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def frameWidth(self, event):
		self.canvas.itemconfig("internalPanel", width=event.width)
	
	def update(self, *args):
		self.canvas.event_generate("<Configure>", width=self.canvas.winfo_width())
		self.event_generate("<Configure>")
		self.parent.update(args)


class ScrollCanvas(Canvas):
	def __init__(self, parent):
		Canvas.__init__(self, parent, borderwidth=0)
		self.parent = parent
		self.grid(sticky=NSEW)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.bind("<Configure>", self.on_resize)
	
	def on_resize(self,event):
		self.configure(width=event.width)
	
	def update(self, *args):
		self.parent.update(args)


class PanelLabel(Label):
	def __init__(self, parent=None, text=""):
		Label.__init__(self, parent, text=text, bg=PANELCOLOR, fg=TEXTCOLOR)
		self.grid(sticky=NSEW)


class TextInput(PanelFrame):
	def __init__(self, parent, label, var):
		PanelFrame.__init__(self, parent)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.label = PanelLabel(self, text=label)
		self.label.grid(column=0, row=0, sticky=E)
		self.entry = Entry(self, width=10, textvariable=var)
		self.entry.grid(column=1, row=0, sticky=W)


class NumberSlider(PanelFrame):
	def __init__(self, parent, label, low, high, var):
		PanelFrame.__init__(self, parent)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=3)
		self.label = PanelLabel(self, text=label)
		self.label.grid(column=0, row=0, sticky=E)

		self.bind("<Configure>", self.on_resize)

		self.slider = Scale(self,
				from_=low, to=high,
				width=7, length=150, sliderlength=10,
				orient=HORIZONTAL, sliderrelief=FLAT,
				bg=PANELCOLOR, fg=TEXTCOLOR, highlightcolor=BUTTONCOLOR,
				activebackground=PANELCOLOR, troughcolor=BUTTONCOLOR,
				highlightthickness=0,
				variable=var)
		self.slider.grid(column=1, row=0)

	def on_resize(self,event):
		self.slider.configure(length=event.width*0.5)


class OptionButton(Menubutton):
	def __init__(self, parent, label, var, options):
		Menubutton.__init__(self, parent, text=label, borderwidth=0, relief=FLAT, bg=BUTTONCOLOR, fg=TEXTCOLOR, indicatoron=False)
		
		self.menu = Menu(self, tearoff=False)
		self.configure(menu=self.menu)
		for op in options:
			self.menu.add_radiobutton(label=op, variable=var, value=op, indicatoron=False)


class OptionSelector(OptionMenu):
	def __init__(self, parent, var, options):
		OptionMenu.__init__(self, parent, var, *options)
		self.configure(borderwidth=0, highlightthickness=0, relief=FLAT, bg=BUTTONCOLOR, fg=TEXTCOLOR)
		# self.grid(sticky=NSEW)


class SaveButton(Button):
	def __init__(self, parent, command):
		Button.__init__(self, parent, text='Save', command=command,
				width=15,
				relief=FLAT,
				bg=BUTTONCOLOR, fg=TEXTCOLOR)


class DeleteButton(Button):
	def __init__(self, parent, command):
		self.photo = PhotoImage(file="icon/exit_small.png")
		Button.__init__(self, parent, command=command,
				image=self.photo,
				width=10, height=10,
				relief=FLAT,
				bg=BUTTONCOLOR, fg=TEXTCOLOR)
		self.grid(sticky=E)


class CollapseButton(Button):
	def __init__(self, parent):
		Button.__init__(self, parent, text="V", command=command, width=2, bg=BUTTONCOLOR, fg=TEXTCOLOR)