# PySimpleCurses
### PySimpleCurses is a module that aims to make a easy TUI. (Text User Interface)<br></br>

# Main Window
### To make a window, you type `<name of window> = Window()`
### You also need to make a main loop by doing:
```python
while 1:
    win.refresh()
```
<br>

# Colors
### Colors are RGB values that can be used on certain widgets to change the color of the text shown below:
- ### Label
- ### Checkbox
- ### Textbox
- ### Box
- ### Button
- ### MultipleSelection
- ### OneSelection

### The built in colors are:
- ### Red
- ### Green
- ### Blue
- ### Yellow
- ### Cyan
- ### Magenta
- ### White
- ### Black
- ### Gray
- ### Dark Gray
- ### Light Gray

### Or optionally you can use RGB values like this:
- ### (R, G, B) (Tuple)
- ### [R, G, B] (List)

# Widgets
- ### Label
### A label is a widget that adds text onto the screen
### Optional arguments:
- ### color - Chooses the color of the text
### Usage: `<name of window>.add(Label(x, y, text, color=<color>))`<br></br>

# Checkbox
### A checkbox is a widget that has 2 states, on and off
### Optional arguments:
- ### state - Chooses the state of the checkbox (default=False)
- ### color - Chooses the color of the checkbox (default=COLOR_WHITE)
- ### side  - Chooses the side that the checkbox is on (default='left')

### Usage: `<name of window>.add(Checkbox(x, y, text, state, color, side))`<br></br>

# Textbox
### A textbox that is like input() and will get the users input
### Optional arguments:
- ### color       - Chooses the color of the checkbox (default=COLOR_WHITE)
- ### maxlength   - Chooses the max amount of characters that is allowed in the textbox (default=<infinite>)
- ### ispassword  - Chooses if the textbox is a password (default=False)

### Usage: `<name of window>.add(Textbox(x, y, name, color, maxlength, ispassword))`<br></br>

# Rect
### A box draws a rectangle to the screen
### Optional arguments:
- ### color       - Chooses the color of the box (default=COLOR_WHITE)
- ### solid       - Chooses if the box is solid (default=False)

### Usage: `<name of window>.add(Rect(x, y, width, height, color, solid))`<br></br>

# Button
### A button is a widget that when you press space it will run the function that it is givin
### Optional arguments:
- ### onclick     - When you press the space bar it will run the function that it is givin (default=None)
- ### color       - Chooses the color of the button (default=COLOR_WHITE)

### Usage: `<name of window>.add(Button(x, y, width, height, onclick, color))`<br></br>

# MultipleSelection
### A multipleselection widget that has items and you can select multiple of them
### Optional Arguments:
- ### color       - Chooses the color of the highlighted item (defualt=COLOR_DARK_GRAY)

### Usage: `<name of window>.add(MultipleSelection(x, y, items, color))`<br></br>

# OneSelection
### A oneselection widget that has items and you can only select one item
### Optional arguments:
- ### color       - Chooses the color of the highlighted item (default=COLOR_DARK_GRAY)

### Usage: `<name of window>.add(OneSelection(x, y, items, color))`<br></br>

# Frame
### A frame is a widget that acts like a window except it is a window with a border and a title
### Optional arguments:
- ### None

### Usage: `<name of window>.add(Frame(x, y, width, height, title))`<br></br>

# Authors notes
- #### I Didn't know what to name MultipleSelection and OneSelection
- #### `<name of window>` is the name of the window variable
- #### On windows, pysimplecurses.py may trigger windows defender