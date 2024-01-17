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
- remove cancel from the replace_key_window
  - if key does not match remapped key, where the cancel used to be reset key will now appear
  - calls function called reset key that will reset the key
  - have save reset cancel


- if a key is written in text then + is added select that key as you would normally with click (if the text == lowercase of a key autofill and select it)
- remove multiple duplicate keys in the replace key window
- make it so that when a modifier key is selected it will shrink the corresponding modifier key like in the shrink function, if that text exists shrink
- maybe add segmented button in replace window with keys, macros, layer options

- in keys.txt, add variable that holds the original button key text, for resetting keys
  - also make it so that each key has a real name and a shown name, for instance the real name would be LShift but the shown name would be Shift
  - implemented this but the current key arrays will not work, will need to do proper ini file structure

- add font theme options
- place create sidebar buttons function inside create sidebar frame function etc
- Add autocorrect to comboboxes (maybe use ctkscrollabledropdown on github)
- pull combobox modifier options and program combobox options from file or function
- fix sidebar buttons not taking whole x (Hard)
- expanding sidebar no longer pushes home frame, will appear over and dim home frame (Hard)
- eventually fix the button hover on corners (borderwidth, border colour matches keys frame?)