# ReBind Beta

CURRENT ISSUES:

TO DO:
- Add switching for if more then one youtube tab exists (same keybind as regular switching)
- make a 50% (or lower) opacity gui of the app icon when sending a keystroke (if more then one window is open) 
  - for instance if volume is sent to yt the youtube icon will appear at the top left the of the window and will be lightly visible (makes it easier to know where keys are being sent for multiple program sends)
- Universal Audio Keybinds (combine python + ahk via wrapper/via cfg)

TO DO LATER:
- Make either extension or code modifications to make sure all keybinds sent to youtube tab go only to the video player (use selenium for python)
- Make it so that you can send youtube hotkeys even when youtube is not the focused tab (use selenium for python)
- Make it so that you can skip forward and back when edge is focused (use selenium for python)
- Python GUI (In progress)
- Make toggle gui opaque (python most likely)
- OPTIMIZATION/Clean-Up

# ReBind GUI (Python)
TO DO:
- in keys.txt, add variable that holds the original button key text, for resetting keys
  - also make it so that each key has a real name and a shown name, for instance the real name would be LShift but the shown name would be Shift
  - implemented this but the current method is not ideal, should make proper ini structure
  - for modifier or program or layer keys, they should be made in the ini file when they are binded in the program
- to speed up the replace key window async build the keys to speed up the open window

- when saving a key or reset a key notification will appear at the top right similar to material
- if a key is written in text then + is added select that key as you would normally with click (if the text == lowercase of a key autofill and select it)
- remove multiple duplicate keys in the replace key window
- make it so that when a modifier key is selected it will shrink the corresponding modifier key like in the shrink function, if that text exists shrink
- maybe add segmented button in replace window with keys, macros, layer options

- add font theme options
- place create sidebar buttons function inside create sidebar frame function etc
- Add autocorrect to comboboxes (maybe use ctkscrollabledropdown on github)
- pull combobox modifier options and program combobox options from file or function
- fix sidebar buttons not taking whole x (Hard)
- expanding sidebar no longer pushes home frame, will appear over and dim home frame (Hard)
- eventually fix the button hover on corners (borderwidth, border colour matches keys frame?)
- when toggling the sidebar maybe make like a for x=0 to 200 pixels sidebarwidth = sidebarwidth + 1 and then when it reaches 200 it stops and then when you toggle it again it does the opposite, and same for the homeframe
- add a colour effect to the sidebar button indicating current screen (same as pydracula)