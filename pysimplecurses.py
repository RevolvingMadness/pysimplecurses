from operator import attrgetter
import os
import time
if os.name != 'nt':
    from getch import getch
    from pynput import keyboard
else:
    import msvcrt
width, height = os.get_terminal_size()
os.system('color' if os.name == 'nt' else '')

### COLORS ###

COLOR_RED = [255, 0, 0]
COLOR_GREEN = [0, 255, 0]
COLOR_BLUE = [0, 0, 255]
COLOR_YELLOW = [255, 255, 0]
COLOR_CYAN = [0, 255, 255]
COLOR_MAGENTA = [255, 0, 255]
COLOR_WHITE = [255, 255, 255]
COLOR_BLACK = [0, 0, 0]
COLOR_GRAY = [128, 128, 128]
COLOR_DARK_GRAY = [64, 64, 64]
COLOR_LIGHT_GRAY = [192, 192, 192]

### SPECIAL KEYS ###

SPECIAL_KEYS = ['LEFT_ARROW', 'RIGHT_ARROW', 'DOWN_ARROW', 'UP_ARROW', '\\t', '\\n', '\\r']


###  FUNCTIONS  ###

if os.name == 'nt':
    def getch():
        if msvcrt.kbhit():
            k = msvcrt.getch()
            if k == b'\xe0':
                k = msvcrt.getch()
                if k in [b'H', b'M', b'K', b'P', b'S', b'\x08']:
                    if k == b'H':
                        return 'UP_ARROW'
                    elif k == b'M':
                        return 'RIGHT_ARROW'
                    elif k == b'K':
                        return 'LEFT_ARROW'
                    elif k == b'P':
                        return 'DOWN_ARROW'
            elif k == b'\x08':
                return 'BACKSPACE'
            else:
                return str(k)[2:-1]
                
def cprint(text='', r=255, g=255, b=255, end='\n'):
    print("\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text), end=end)

### WIDGETS ###

class Window:
    def __init__(self):
        self.layout = []
        self.widgets = []
        self.selectablewidgets = []
        self.selectedindex = 0
        self.defaultindex = 0
        self.i = 0
        self.currkey = None
        self.currentcolor = COLOR_WHITE
        self.run = True
        if os.name != 'nt':
            listener = keyboard.Listener(on_press=self.getch)
            listener.start()
        self.init_layout()
        self.refresh()

    def init_layout(self):
        for y in range(height):
            self.layout.append([])
            for x in range(width):
                self.layout[y].append([' ', 255, 255, 255])
    
    def close(self):
        os.system('cls')
        exit()
    
    def init_selected(self):
        for i, widget in enumerate(self.widgets):
            if widget.selectable:
                self.selectedindex = i
                self.defaultindex = i
                break
    
    def getch(self, key=''):
        try:
            self.currkey = key.char.replace('Key.', '')
        except AttributeError:
            key = str(key)
            if key == 'Key.down':
                self.currkey = 'DOWN_ARROW'
            elif key == 'Key.up':
                self.currkey = 'UP_ARROW'
            elif key == 'Key.left':
                self.currkey = 'LEFT_ARROW'
            elif key == 'Key.right':
                self.currkey = 'RIGHT_ARROW'
            elif key == 'Key.space':
                self.currkey = ' '
            elif key == 'Key.backspace':
                self.currkey = 'BACKSPACE'
            elif key == 'Key.shift':
                self.currkey = None
            elif key == 'Key.tab':
                self.currkey = '\\t'

    def add(self, widget):
        self.widgets.append(widget)
        widget.win = self
        widget.selected = False
        self.widgets.sort(key=attrgetter('y'))
        if widget.selectable:
            self.selectablewidgets.append(self.i)
        self.i += 1
        self.init_selected()
        widget.update()

    def addstr(self, x, y, text, isbold=False):
        for i in range(len(text)):
            if isbold:
                self.layout[y][x+i][0] = '\033[1m'+text[i]+'\033[0m'
            else:
                self.layout[y][x+i][0] = text[i]
            self.layout[y][x+i][1] = self.currentcolor[0]
            self.layout[y][x+i][2] = self.currentcolor[1]
            self.layout[y][x+i][3] = self.currentcolor[2]

    def color(self, text_color):
        if type(text_color) == tuple:
            self.currentcolor = [text_color[0], text_color[1], text_color[2]]
        elif type(text_color) == list:
            self.currentcolor = text_color

    def refresh(self):
        self.i = 0
        for y in range(len(self.layout)-1):
            for x in range(len(self.layout[y])):
                cprint(self.layout[y][x][0], r=self.layout[y][x][1], g=self.layout[y][x][2], b=self.layout[y][x][3], end='')
            print()
        for y in range(len(self.layout)-1):
            print('\033[F', end='')
        if os.name == 'nt':
            key = getch()
        if os.name != 'nt':
            key = self.currkey

        if key != None:
            if self.selectedindex != self.defaultindex:
                if key == 'UP_ARROW':
                    while self.selectedindex-1 not in self.selectablewidgets:
                        self.selectedindex -= 1
                    self.selectedindex -= 1
            if self.selectedindex != len(self.widgets)-1:
                if key == 'DOWN_ARROW' or key == 'Key.down':
                    while self.selectedindex+1 not in self.selectablewidgets:
                        self.selectedindex += 1
                    self.selectedindex += 1

        for i, widget in enumerate(self.widgets):
            if i == self.selectedindex:
                widget.selected = 1
            else:
                widget.selected = 0
            widget.update(key)
        self.currkey = None

class Label:
    def __init__(self, x, y, text, color=COLOR_WHITE):
        self.win = None
        self.x = x
        self.y = y
        self.value = text
        self.selectable = False
        self.color = color

    def update(self, key=''):
        self.win.color(self.color if self.selected else COLOR_LIGHT_GRAY)
        self.win.addstr(self.x, self.y, self.value)
        self.win.color(COLOR_WHITE)

class Checkbox:
    def __init__(self, x, y, text, state=0, color=COLOR_WHITE, side='left'):
        self.win = None
        self.x = x
        self.y = y
        self.value = text
        self.state = state
        self.selectable = True
        self.color = color
        self.side = side

    def update(self, key=''):
        if key != None and key != '':
            if key == ' ' and self.selected:
                self.state = not self.state

        self.win.color(self.color if self.selected else COLOR_LIGHT_GRAY)
        if self.side == 'left':
            self.win.addstr(self.x, self.y, '[*] ' + self.value if self.state else '[ ] ' + self.value)
        else:
            self.win.addstr(self.x, self.y, self.value + ' [*]' if self.state else self.value + ' [ ]')
        self.win.color(COLOR_WHITE)

class Textbox:
    def __init__(self, x, y, name, color=COLOR_WHITE, maxlength=-1, ispassword=False):
        self.win = None
        self.x = x
        self.y = y
        self.name = name
        self.value = ''
        self.selectable = True
        self.color = color
        self.maxlength = maxlength
        self.ispassword = ispassword

    def update(self, key=''):
        if key != None and self.selected and key != '':
            if key == 'BACKSPACE':
                if len(self.value) != 0:
                    self.value = list(self.value)
                    self.value[-1] = ' '
                    self.win.addstr(self.x+len(self.name), self.y, ''.join(self.value))
                    self.value = list(self.value)
                    self.value = self.value[:-1]
                    self.value = ''.join(self.value)
            else:
                if self.ispassword:
                    if self.maxlength != -1:
                        if len(self.value) != self.maxlength:
                            if key not in SPECIAL_KEYS:
                                self.value += key
                    else:
                        if key not in SPECIAL_KEYS:
                            self.value += key
                else:
                    if self.maxlength != -1:
                        if len(self.value) != self.maxlength:
                            if key not in SPECIAL_KEYS:
                                self.value += key
                    else:
                        if key not in SPECIAL_KEYS:
                            self.value += key
        self.win.color(self.color if self.selected else COLOR_LIGHT_GRAY)
        self.win.addstr(self.x, self.y, self.name + self.value if not self.ispassword else self.name + '*'*len(self.value))
        self.win.color(COLOR_WHITE)

class Rect:
    def __init__(self, x, y, width, height, color=COLOR_WHITE, solid=False):
        self.win = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.selectable = False
        self.solid = solid

    def update(self, key=''):
        if self.solid:
            for i in range(self.height):
                for j in range(self.width):
                    self.win.addstr(self.x+j, self.y+i, '█')
        else:
            for i in range(self.height):
                for j in range(self.width):
                    self.win.color(self.color)
                    if i == 0:
                        self.win.addstr(self.x+j, self.y+i, '─')
                    if i == self.height-1:
                        self.win.addstr(self.x+j, self.y+i, '─')
                    if j == 0:
                        self.win.addstr(self.x+j, self.y+i, '│')
                    if j == self.width-1:
                        self.win.addstr(self.x+j, self.y+i, '│')
                    if i == 0 and j == 0:
                        self.win.addstr(self.x+j, self.y+i, '┌')
                    if i == 0 and j == self.width-1:
                        self.win.addstr(self.x+j, self.y+i, '┐')
                    if i == self.height-1 and j == self.width-1:
                        self.win.addstr(self.x+j, self.y+i, '┘')
                    if i == self.height-1 and j == 0:
                        self.win.addstr(self.x+j, self.y+i, '└')
        self.win.color(COLOR_WHITE)

class Button:
    def __init__(self, x, y, text, onclick=None, color=COLOR_WHITE):
        self.win = None
        self.x = x
        self.y = y
        self.value = '[' + text + ']'
        self.selectable = True
        self.on_click = onclick
        self.color = color

    def update(self, key=''):
        if key == ' ' and self.selected and self.on_click != None:
            self.on_click()
        self.win.color(self.color if self.selected else COLOR_LIGHT_GRAY)
        self.win.addstr(self.x, self.y, self.value)
        self.win.color(COLOR_WHITE)

class MultipleSelection:
    def __init__(self, x, y, items, color=COLOR_DARK_GRAY):
        self.x = x
        self.y = y
        self.items = items
        self.selectable = True
        self.selectedindex = 0
        self.selecteditems = []
        self.value = {}
        self.color = color

    def update(self, key=''):
        if key == '\\t' and self.selected:
            if self.selectedindex == len(self.items)-1:
                self.selectedindex = 0
            else:
                self.selectedindex += 1
        if key == ' ' and self.selected:
            if self.selectedindex not in self.selecteditems:
                self.selecteditems.append(self.selectedindex)
            else:
                self.selecteditems.remove(self.selectedindex)
        for i, item in enumerate(self.items):
            if self.selected:
                if i == self.selectedindex:
                    self.win.color(self.color)
                else:
                    self.win.color(COLOR_WHITE)
            else:
                self.win.color(COLOR_LIGHT_GRAY)
            self.win.addstr(self.x, self.y+i, '[*]' + item if i in self.selecteditems else '[ ]' + item)
            self.win.color(COLOR_WHITE)
        self.value = {}
        for j, item in enumerate(self.items):
            self.value[item] = True if j in self.selecteditems else False
        self.value = str(self.value)

class OneSelection:
    def __init__(self, x, y, items, color=COLOR_DARK_GRAY):
        self.x = x
        self.y = y
        self.items = items
        self.selectable = True
        self.selectedindex = 0
        self.selecteditems = []
        self.value = {}
        self.color = color

    def update(self, key=''):
        if key == '\\t' and self.selected:
            if self.selectedindex == len(self.items)-1:
                self.selectedindex = 0
            else:
                self.selectedindex += 1
        if key == ' ' and self.selected:
            if self.selectedindex in self.selecteditems:
                self.selecteditems = []
            else:
                self.selecteditems = [self.selectedindex]
        
        for i, item in enumerate(self.items):
            if self.selected:
                if i == self.selectedindex:
                    self.win.color(self.color)
                else:
                    self.win.color(COLOR_WHITE)
            else:
                self.win.color(COLOR_LIGHT_GRAY)
            self.win.addstr(self.x, self.y+i, '(*) ' + item if i in self.selecteditems else '( ) ' + item)
            self.win.color(COLOR_WHITE)
            self.value = {}
            for j, item in enumerate(self.items):
                self.value[item] = True if j in self.selecteditems else False
            self.value = str(self.value)

class Frame:
    def __init__(self, x, y, w, h, t):
        self.win = None
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.t = t
        self.selectable = False

    def update(self, key=None):
        self.win.add(Box(self.x, self.y, self.w, self.h))
        self.win.add(Label(self.x+3, self.y, ' ' + self.t + ' '))

    def add(self, w):
        w.x += self.x+1
        w.y += self.y+1
        self.win.add(w)
