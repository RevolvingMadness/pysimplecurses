from curses import *

class Window:
	def __init__(self):
		self.win = initscr()
		noecho()
		start_color()
		self.win.nodelay(1)
		self.widgets = []
		self.selidx = 0
		init_pair(38, COLOR_BLACK, COLOR_WHITE)
		init_pair(97, COLOR_GREEN, COLOR_BLACK)

	def add(self, widget):
		self.widgets.append(widget)
		widget.win = self.win
		widget.update()
		self.widgets[0].selected = 1
		self.widgets[0].update()

	def update(self, key=-1):
		for i in range(len(self.widgets)):
			if self.widgets[i].selectable == 1:
				if self.selidx == i:
					self.widgets[i].selected = 1
				else:
					self.widgets[i].selected = 0

				if self.widgets[i].type == 'button':
					self.widgets[i].master = self

				self.widgets[i].update(key)

	def exit(self):
		endwin()
		exit()

	def getch(self): return self.win.getch()
	def getkey(self): return self.win.getkey()

	def run(self):
		while 1:
			try:
				key = self.win.getkey()
				if key == '\n':
					if self.selidx != len(self.widgets)-1:
						try:
							if self.widgets[self.selidx+1].selectable == 1:
								self.selidx += 1
							else:
								a = 1
								while 1:
									if self.widgets[self.selidx+a].selectable == 1:
										self.selidx += a
										a = 1
										break
									else:a += 1
						except IndexError:
							self.selidx = 0
					else:
						self.selidx = 0
				self.update(key)
			except error:
				pass

class Label:
	def __init__(self, x, y, Label):
		self.win = None
		self.x = x
		self.y = y
		self.Label = Label
		self.selected = 0
		self.type = 'Label'
		self.selectable = 1

	def update(self, key=-1):
		if self.selected:
			self.win.addstr(self.y, self.x, self.Label, color_pair(97))
		else:
			self.win.addstr(self.y, self.x, self.Label)

class Input:
	def __init__(self, x, y, name):
		self.win = None
		self.x = x
		self.y = y
		self.type = 'input'
		self.Label = ''
		self.selected = 0
		self.name = name
		self.selectable = 1

	def update(self, key=-1):
		if self.selected:
			if key != -1 and key != '\n':
				if key != '\b':
					if key == '\t':
						self.Label += ' '*4
					else:
						self.Label += key
				if key == '\b' and len(self.Label) != 0:
					self.backspace()

		if self.selected:
			self.win.addstr(self.y, self.x, self.name, color_pair(97))
		else:
			self.win.addstr(self.y, self.x, self.name)
		self.win.addstr(self.y, self.x+len(self.name), self.Label)

	def backspace(self):
		self.Label = list(self.Label)
		self.Label[-1] = ' '
		self.Label = ''.join(self.Label)
		self.win.addstr(self.y, self.x+len(self.name), self.Label)
		self.Label = list(self.Label)
		self.Label.pop()
		self.Label = ''.join(self.Label)

class Checkbox:
	def __init__(self, x, y, name, state=0):
		self.win = None
		self.x = x
		self.y = y
		self.name = name
		self.selected = 0
		self.s = state
		self.type = 'checkbox'
		self.selectable = 1

	def update(self, key=-1):
		if self.selected:
			if key != -1:
				if key == ' ':
					self.s = 1 if not self.s else 0


		if self.s:
			if self.selected:self.win.addstr(self.y, self.x, '[*] ')
			else:self.win.addstr(self.y, self.x, '[*] ')
		else:
			if self.selected:self.win.addstr(self.y, self.x, '[ ] ')
			else:self.win.addstr(self.y, self.x, '[ ] ')
		if self.selected:
			self.win.addstr(self.y, self.x+4, self.name, color_pair(97))
		else:
			self.win.addstr(self.y, self.x+4, self.name)

class Button:
	def __init__(self, x, y, name, onclick=None, state=0):
		self.win = None
		self.master = None
		self.x = x
		self.y = y
		self.name = name
		self.onclick = onclick
		self.selected = 0
		self.s = state
		self.type = 'button'
		self.selectable = 1
		
	def update(self, key=-1):
		if self.selected:
			if key != -1 and key == ' ' and self.onclick != None:
				self.onclick()
				self.master.widgets[0].selected = 0
				self.master.widgets[0].update()

		if self.selected:self.win.addstr(self.y, self.x, self.name, color_pair(97))
		else:self.win.addstr(self.y, self.x, self.name)

class Box:
	def __init__(self, x, y, w, h, title=''):
		self.win = None
		self.x = x
		self.y = y
		self.w = w+len(title)
		self.h = h
		self.title = title
		self.type = 'box'
		self.selectable = 0
		self.selected = 0

	def update(self, key=-1):
		for x in range(self.w):
			if self.selected:
				self.win.addstr(self.y, self.x, '┌─' + self.title + '─'*(self.w-3-len(self.title)) + '┐', color_pair(97))
				for y in range(self.h-2):
					self.win.addstr(self.y+y+1, self.x, '│' + ' '*(self.w-2) + '│', color_pair(97))
					self.win.addstr(self.y+y+2, self.x, '└' + '─'*(self.w-2) + '┘', color_pair(97))
			else:
				self.win.addstr(self.y, self.x, '┌─' + self.title + '─'*(self.w-3-len(self.title)) + '┐')
				for y in range(self.h-2):
					self.win.addstr(self.y+y+1, self.x, '│' + ' '*(self.w-2) + '│')
					self.win.addstr(self.y+y+2, self.x, '└' + '─'*(self.w-2) + '┘')
		

'''
┌───────────────────────────────────────────────┐
│	─	│	┌	┐	└	┘	├	┤	┬	┴	┼	│
│												│
│	═	║	╔	╗	╚	╝	╠	╣	╦	╩	╬	│
└───────────────────────────────────────────────┘
'''