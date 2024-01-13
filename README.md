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
- maybe add checkbox in replace key window when a program is typed, checkbox will control if the program needs to be focused (ifwindowexist vs ifwindowactive)
- in keys.txt, add variable that holds the original button key text, for resetting keys
- in modification bar, if program dropdown has text, create a checkbox to the right of it with text "Require Program Focus: " 

- add font theme options
- place create sidebar buttons function inside create sidebar frame function etc
- Add autocorrect to comboboxes (maybe use ctkscrollabledropdown on github)
- pull combobox modifier options and program combobox options from file or function
- fix sidebar buttons not taking whole x (Hard)
- expanding sidebar no longer pushes home frame, will appear over and dim home frame (Hard)
- seperate gui functions into new file?
- eventually fix the button hover on corners