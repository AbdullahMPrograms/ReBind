AutoExec() {
	; Initial setup
	global programs := ["Stremio", "YouTube"]
	global currentProgramIndex := 1  ; start with the first program in the list

	#NoEnv
	#MaxHotkeysPerInterval,50000
	#SingleInstance Force
	#Persistent
	#MenuMaskKey vkE8 ; Replace default mask key Ctrl with vkE8 (Unused) 
	SetTitleMatchMode 2
	DetectHiddenWindows, On
	SendMode Input

	;disable numlock and capslock
	SetNumLockState, AlwaysOff
	SetCapsLockState, AlwaysOff

	SetTimer, CheckPrograms, 5000  ; Checks every second

	;< ---------------- TRAY MENU ---------------- >
	Menu, tray, nostandard ; removes original menu
	Menu, Tray, Add, Set Microphone Volume, LoopMicVolume ; Add a menu item named "Set Microphone Volume" that calls the subroutine "MicVolume"
	Menu, Tray, Add, F-Key Rebind, FKeyRebind 
	Menu, Tray, Add ; Seperator
	Menu, Tray, Standard ; puts original back "under" custom menu

	SetTimer PreFlightCheck, -1 ; Run PreFlightCheck once on script start
}

MyMsg(text) {
  MsgBox, % text
}

SendKey(Key, Program) {
; SendKey Method
	ControlFocus
	ControlSend ahk_parent, % Key, % Program
	Return 									; clear buffer
}

SendKey("+{N}", "YouTube")
MsgBox, "sent bind"