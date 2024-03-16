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
- Macros should have id (1, 2, 3)
  - will be used for showing M1, M2, M3 (Macro 1, Macro 2, Macro 3) on keyboard when rebound

- re-add x to notification frame, now if click on notification frame it will close
- fix the notification progress bar if more then 1 opened (maybe set hardcoded time using after)

- for layouts several things need to be changed
  - the keys_frame will now be called keyboard_keys_frame and placed in keyboard_frame (follow gmmk packaging)
  - in the JSON file for the layout each button should have "key_colour_1" "key_colour_2" for proper keyboard colour layouts (like keycaps)
  - the spacing for the keys will need to be reset to 0,0 and remove the max_x max_y code

- for numwheel, add segmented button at the top of the replace_key_window to select between (press, left, right)
- make it so that scroll bar appears only if hovering over replace buttons in replace_key_window
  - can be done with frame enter/leave + sidebar_button_color
- modifier shift should show the shift number keys, shift + 2 = @

- maybe make the keyboard frame update only after the sidebar has been expanded in the animation ver

- make it so that when a modifier key is selected it will shrink the corresponding modifier key like in the shrink function, if that text exists shrink
  - will require keyboardkeys json integration
- when selecting a program/layer it should update the keyboard to show the keys rebound in that program/layer
- if a key is written in text then + is added select that key as you would normally with click (if the text == lowercase of a key autofill and select it)
- eventually seperate functions massively to avoid cross and over computation (reading variables from json and computing on top of them)
  - like when saving keys or resetting or in update_buttons, they should all call a function for values
- add font theme options

- Add autocorrect to comboboxes (maybe use ctkscrollabledropdown on github)
- pull combobox modifier options and program combobox options from file or function

- eventually fix the button hover on corners (borderwidth, border colour matches keys frame?)
- when toggling the sidebar maybe make like a for x=0 to 200 pixels sidebarwidth = sidebarwidth + 1 and then when it reaches 200 it stops and then when you toggle it again it does the opposite, and same for the homeframe

- for eventual mouse support make it work like the ghub ui
  - mouse in middle with boxes around the various mouse buttons/mouse buttons selectable
  - requires drawing
  - swap mouse/keyboard with toggle switch in the modification bar
    - left side of toggle is keyboard (default), right side of toggle is mouse
    - toggling right will move the label to the right and say "Mouse" and viceversa
- QMK/VIA support (just for fun)?
