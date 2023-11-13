;reads code from the cfg folder and executes it
;dumb way for my python program but eh
;this works

; Method:
; Can use a persistent AHK program (ReBind) that reads a cfg file like below to run code
; inside python program whenever you change something in the gui it will write to the file and restart the ahk process (or the AHK program will read the file every 5-10 seconds idk yet)
; thus you get a python gui but AHK functionality (kinda stupid ik)
; Later on will have to be a full code conversion, either AHK wrapper (AHKUnwrapped most likely) or rewrite functions in python

; Include initial setup
#Include %A_ScriptDir%\cfg\InitialSetup.txt

; Include hotkeys setup
#Include %A_ScriptDir%\cfg\HotkeysSetup.txt

; Include methods
#Include %A_ScriptDir%\cfg\Methods.txt

; Include tray menu setup
#Include %A_ScriptDir%\cfg\TrayMenuSetup.txt

; Include program-specific keybinds
#Include %A_ScriptDir%\cfg\ProgramSpecificKeybinds.txt

; Include preflight check and scripts
#Include %A_ScriptDir%\cfg\PreflightCheckAndScripts.txt
