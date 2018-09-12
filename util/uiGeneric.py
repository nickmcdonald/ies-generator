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


class CheckboxInput(PanelFrame):
	def __init__(self, parent, label, var):
		PanelFrame.__init__(self, parent)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.label = PanelLabel(self, text=label)
		self.label.grid(column=0, row=0, sticky=E)

		self.cbox = Checkbutton(self, textvariable=var, 
				bg=PANELCOLOR, activebackground=PANELCOLOR,
				fg=PANELCOLOR, activeforeground=PANELCOLOR,
				selectcolor=BUTTONCOLOR,
				text=''
		)

		self.cbox.grid(column=1, row=0, sticky=W)


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
		Menubutton.__init__(self, parent, text=label, borderwidth=0, relief=FLAT,
		activebackground=BUTTONCOLOR, bg=BUTTONCOLOR,
		activeforeground=TEXTCOLOR, fg=TEXTCOLOR,
		indicatoron=False)
		
		self.menu = Menu(self, tearoff=False)
		self.configure(menu=self.menu)
		for op in options:
			self.menu.add_radiobutton(label=op, variable=var, value=op, indicatoron=False)


class OptionSelector(OptionMenu):
	def __init__(self, parent, var, options):
		OptionMenu.__init__(self, parent, var, *options)
		self.configure(borderwidth=0,
				highlightthickness=0, relief=FLAT,
				activebackground=BUTTONCOLOR, bg=BUTTONCOLOR,
				activeforeground=TEXTCOLOR, fg=TEXTCOLOR)


class BaseButton(Button):
	def __init__(self, parent, command, text="", image=None, width=10, height=10, bg=BUTTONCOLOR):
		Button.__init__(self, parent, command=command,
				text=text, image=image,
				width=width,
				height=height,
				relief=FLAT,
				activebackground=bg, bg=bg, 
				activeforeground=TEXTCOLOR, fg=TEXTCOLOR)


class ExportButton(BaseButton):
	def __init__(self, parent, command):
		BaseButton.__init__(self, parent, text='Export', command=command, width=15, height=1)


class DeleteButton(BaseButton):
	def __init__(self, parent, command):
		self.deleteImage = PhotoImage(file="icon/exit_small.png")
		BaseButton.__init__(self, parent, command=command, image=self.deleteImage)


class CollapseButton(BaseButton):
	def __init__(self, parent, collapseFrame):
		self.collapsedImage = PhotoImage(file="icon/collapsed_small.png")
		self.expandedImage = PhotoImage(file="icon/expanded_small.png")
		BaseButton.__init__(self, parent, command=self.toggle,
				image=self.expandedImage, bg=PANELCOLOR)

		self.collapseFrame = collapseFrame
		self.collapseFrameRow = int(collapseFrame.grid_info()['row'])
		self.collapseFrameColumn = int(collapseFrame.grid_info()['column'])
		self.collapsed = False
	
	def toggle(self):
		if self.collapsed:
			self.collapseFrame.grid(column=self.collapseFrameColumn,row=self.collapseFrameRow)
			self.configure(image=self.expandedImage)
		else:
			self.collapseFrame.grid_remove()
			self.configure(image=self.collapsedImage)
		self.collapsed = not self.collapsed

class VisibilityButton(BaseButton):
	def __init__(self, parent, var):
		self.visibleImage = PhotoImage(file="icon/visible_small.png")
		self.notVisibleImage = PhotoImage(file="icon/notvisible_small.png")
		self.parent = parent
		self.var = var
		BaseButton.__init__(self, parent, command=self.toggle,
				image=self.visibleImage)

		self.visible = True
	
	def toggle(self):
		self.visible = not self.visible
		if self.visible:
			self.configure(image=self.visibleImage)
			self.var.set(True)
		else:
			self.configure(image=self.notVisibleImage)
			self.var.set(False)
		
		self.parent.parent.update()