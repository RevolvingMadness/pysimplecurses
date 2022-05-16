# PySimpleCurses
### PySimpleCurses is a module that aims to make a easy TUI. (Text User Interface)

## Main Window
### To make a window, you type `<name of window> = Window()`

### Colors
### Colors are RGB values that can be used on certain widgets shown below:
- ### Label
- ### Checkbox
- ### Textbox
- ### Box
- ### Button
- ### MultipleSelection
- ### OneSelection

### The built in colors are:
- #### Red
- #### Green
- #### Blue
- #### Yellow
- #### Cyan
- #### Magenta
- #### White
- #### Black
- #### Gray
- #### Dark Gray
- #### Light Gray

### Or optionally you can use RGB values like this:
- #### (R, G, B)
- #### [R, G, B]

## Widgets
- ### Label
### A label is a widget that adds text onto the screen
### Optional arguments:
- ### color - Chooses the color of the text
### Usage: `<name of window>.add(Label(x, y, text, color=COLOR_<COLOR>))`

- ### Checkbox
### A checkbox is a widget that has 2 states, on and off
### Optional arguments:
- #### state - Chooses the state of the checkbox (default=0)
- #### color - Chooses the color of the checkbox (default=COLOR_WHITE)
- #### side  - Chooses the side that the checkbox is on (default='left')