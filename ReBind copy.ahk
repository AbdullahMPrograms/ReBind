;reads code from the cfg folder and executes it
;dumb way for my python program but eh
;this works

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
