from tkinter import *
from  tkinter import  messagebox
from tkinter import font as tkFont
from tkinter import ttk
from tkinter import filedialog
import os, pyautogui, json, keyboard



class main_handle():
	def __init__(self, root):
		self.root = root
		self.saved = True
		self.currentSaveAs = False
		self.currentOpen = False
		self.fileDir = ""
		self.txtColor = 'black'
		self.txtSize = 16
	

	def initUI(self):

		#scrollbar
		self.yScroll = Scrollbar(self.root)
		self.yScroll.pack(side = 'right', fill = Y)
		#mainEntry textbox
		self.mainEntry = Text(self.root, height = 250, width = 500, bd = 2, wrap = WORD,
					insertontime = 500, insertofftime = 500, font = ('aerial', 16, 'bold'),
					yscrollcommand = self.yScroll.set)
		self.mainEntry.pack()

		self.yScroll.config(command = self.mainEntry.yview)


		#init menubar
		self.menuBar = Menu(self.root)
		self.root.config(menu = self.menuBar)

		#File menu
		self.fileMenu = Menu(self.menuBar, tearoff = 0)
		self.menuBar.add_cascade(label="File", menu=self.fileMenu)

		self.fileMenu.add_command(label = 'Save   ', command = self.saveFile)
		self.fileMenu.add_command(label = 'Save As..  ', command = self.saveAs)
		self.fileMenu.add_command(label = 'Open', command = self.openFile)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label = 'Exit', command = self.closeHandler)

		#edit menu
		self.editMenu = Menu(self.menuBar, tearoff = 0)
		self.menuBar.add_cascade(label="Edit", menu=self.editMenu)

		self.editMenu.add_command(label = 'Copy    ', command = lambda: pyautogui.hotkey('ctrl', 'c'))
		self.editMenu.add_command(label = 'Cut', command = lambda: pyautogui.hotkey('ctrl', 'x'))
		self.editMenu.add_command(label = 'Paste', command = lambda: pyautogui.hotkey('ctrl', 'v'))

		#Format menu
		self.formatMenu = Menu(self.menuBar, tearoff = 0)
		self.menuBar.add_cascade(label="Format", menu=self.formatMenu)
		#sub menu for font size
		self.fontSize = Menu(self.formatMenu, tearoff = 0)
		self.formatMenu.add_cascade(label = "font Size", menu = self.fontSize)

		self.fontSize.add_command(label = '8', command = lambda: self.txtCtrl('size', 8))
		self.fontSize.add_command(label = '12', command = lambda: self.txtCtrl('size', 12))
		self.fontSize.add_command(label = '14', command = lambda: self.txtCtrl('size', 14))
		self.fontSize.add_command(label = '16', command = lambda: self.txtCtrl('size', 16))
		self.fontSize.add_command(label = '22', command = lambda: self.txtCtrl('size', 22))
		self.fontSize.add_command(label = '26', command = lambda: self.txtCtrl('size', 26))
		self.fontSize.add_command(label = '32', command = lambda: self.txtCtrl('size', 32))
		self.fontSize.add_command(label = '38', command = lambda: self.txtCtrl('size', 38))
		self.fontSize.add_command(label = '44', command = lambda: self.txtCtrl('size', 44))
		self.fontSize.add_command(label = '50', command = lambda: self.txtCtrl('size', 50))

		#sub menu for color
		self.colors = Menu(self.formatMenu, tearoff = 0)
		self.formatMenu.add_cascade(label = "Font Color", menu = self.colors)

		self.colors.add_command(label = 'black', command = lambda: self.txtCtrl('color', 'black'))
		self.colors.add_command(label = 'red', command = lambda: self.txtCtrl('color', 'red'))
		self.colors.add_command(label = 'blue', command = lambda: self.txtCtrl('color', 'blue'))
		self.colors.add_command(label = 'green', command = lambda: self.txtCtrl('color', 'green'))
		self.colors.add_command(label = 'orange', command = lambda: self.txtCtrl('color', 'orange'))
		self.colors.add_command(label = 'purple', command = lambda: self.txtCtrl('color', 'purple'))
		self.colors.add_command(label = 'pink', command = lambda: self.txtCtrl('color', 'pink'))
		self.colors.add_command(label = 'yellow', command = lambda: self.txtCtrl('color', 'yellow'))



		#init pre txt
		self.preTxt = self.mainEntry.get(1.0, END)

	def txtCtrl(self, opt, val):

		if opt == 'size':
			self.mainEntry.config(font = ('aerial', val, 'bold'))
			self.txtSize = val
		elif opt == 'color':
			self.mainEntry.config(fg = val)
			self.txtColor = val



	def saveAs(self):
		
		try:
			self.fileType = [('Plain Text(*.txt)','*.txt ')]
			self.file = filedialog.asksaveasfile(initialdir = "C:\Smayan's Files",
			 								filetypes = self.fileType, defaultextension = self.fileType)

			self.file.write(self.mainEntry.get(1.0, END))
			self.fileDir = self.file.name

			self.file.close()

			self.saved = True
			self.currentSaveAs = True
			self.currentOpen = False
			self.titleSet()

		except:
			pass

		self.preTxt = self.mainEntry.get(1.0, END)


	def saveFile(self):

		if self.currentOpen or self.currentSaveAs:
			with open(self.fileDir, 'w') as f:
				f.write(self.mainEntry.get(1.0, END))
				self.saved = True

			self.titleSet()

		else:
			self.saveAs()

		self.preTxt = self.mainEntry.get(1.0, END)

	
	def openFile(self):

		try:
			if self.saved:
				
				self.fileDir = filedialog.askopenfilename(parent = self.root, initialdir = "C:\Smayan's Files")

				with open(self.fileDir, 'r') as f:
					self.mainEntry.delete(1.0, END)
					self.mainEntry.insert(1.0, f.read())

				self.saved = True
				self.currentOpen = True
				self.currentSaveAs = False

				self.titleSet()
				
				#reading and applying text data
				try:
					with open('fileData.json', 'r') as f:
						data = json.load(f)

					for val in data:
						if val['file'] == self.fileDir:
							self.txtCtrl('size', val['size'])
							self.txtCtrl('color', val['color'])
							
							break
				except:
					pass


			else:
				if messagebox.askokcancel("Open New?", "your file is not saved\nAre you sure you want to open a new file"):
					self.saved = True
					self.openFile()
		except:
			pass

		self.preTxt = self.mainEntry.get(1.0, END)


	def loop(self):

		self.currentTxt = self.mainEntry.get(1.0, END)
		
		if self.preTxt != self.currentTxt:
			self.saved = False
			self.titleSet()

		#checking for hotkey presses
		if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift') and keyboard.is_pressed('s'):
			self.saveAs()
		if keyboard.is_pressed('ctrl') and keyboard.is_pressed('s'):
			self.saveFile()

		self.root.after(100, self.loop)

	def titleSet(self):

		if self.fileDir == "":
			self.fileDir = "Untitled"


		else:
			if self.saved:
				title = "Text Editor - " + self.fileDir
				self.root.title(title)
			else:
				title = "Text Editor - " + "* " + self.fileDir +  " *"
				self.root.title(title)

	def closeHandler(self):

		#json file handling to store text info
		if self.fileDir != "" and self.fileDir != "Untitled": 
			with open('fileData.json', 'r') as f:
				data = json.load(f)
			
			x = 0
			for element in data:
				if element['file'] == self.fileDir:
					data.pop(x)
					x += 1

			txtData = {"file": self.fileDir, "size": self.txtSize, "color": self.txtColor}
				
			data.append(txtData)
			
			with open('fileData.json', 'w') as f:
				json.dump(data, f, indent = 2)



		if self.saved:
			self.root.destroy()
		else:
			if messagebox.askokcancel("Quit?", "your file is not saved\nAre you sure you want to quit"):
				self.root.destroy()
			else:
				pass



def main():

	root = Tk()
	root.title("Text Editor")
	root.geometry('700x500')
	run = main_handle(root)
	run.initUI()
	run.loop()

	root.protocol("WM_DELETE_WINDOW", run.closeHandler)

	root.mainloop()



if __name__ == '__main__':
	main()