#NoEnv
#MaxHotkeysPerInterval,50000
#SingleInstance Force
#MenuMaskKey vkE8 ; Replace default mask key Ctrl with vkE8 (Unused) 
;^ MenuMaskKey does not fix misinput in games
SetTitleMatchMode 2
DetectHiddenWindows, On
SendMode Input

toggle := false ; Set the toggle variable to true
Menu, Tray, Add, Set Microphone Volume, MicVolume ; Add a menu item named "Set Microphone Volume" that calls the subroutine "MicVolume"
Menu, Tray, Default, Set Microphone Volume ; Make the menu item the default action when the icon is clicked
GoSub MicVolume ; Call the subroutine once to start the loop and check the menu item

;disable numlock and capslock
SetNumLockState, AlwaysOff
SetCapsLockState, AlwaysOff

;reload program in case of edge case failure
^!r::Reload

;core rebind
CapsLock & 1:: F1
CapsLock & 2:: F2
CapsLock & 3:: F3
CapsLock & 4:: F4 
CapsLock & 5:: F5
CapsLock & 6:: F6
CapsLock & 7:: F7
CapsLock & 8:: F8
CapsLock & 9:: F9
CapsLock & -:: F11
CapsLock & 0:: F10
CapsLock & =:: F12
CapsLock & Esc:: `
CapsLock & Delete:: Numpad1
-------------------------------------------------------------
; Deactivate volume wheel
*Volume_Up::Return
*Volume_Down::Return

;Deactivate RShift
;*RShift::Return
;Deactivate RAlt
*RAlt::Return
-------------------------------------------------------------
; If FN (CapsLock) is pressed Next Media
While (GetKeyState(CapsLock,"p")) {
	; fn + wheel to skip and go back on media
	CapsLock & Volume_Up::Media_Next
	CapsLock & Volume_Down::Media_Prev
}
-------------------------------------------------------------
; Methods
-------------------------------------------------------------
; RapidFire Method
RapidFire() {
	While(GetKeyState("LButton","P") And GetKeyState("XButton1","P")) 
	{
		send {LButton down}
		Sleep 7
		send {LButton up}
		Sleep 7
	}
}

SendKey(Key, Program) {
; SendKey Method
	ControlFocus
	ControlSend ahk_parent, % Key, % Program
	Return 									; clear buffer
}

; Trigger VolumeOSD Method
TriggerVolumeOSD() {
	send {Volume_Up 1}
	Return
}

-------------------------------------------------------------
; Universal Keybinds
-------------------------------------------------------------
;Rapid Fire 
~XButton1 & LButton::
{
	RapidFire()
	Return
}	
-------------------------------------------------------------
; App specific keybinds
-------------------------------------------------------------
; YouTube
#If WinExist("YouTube") 
	
	*Volume_Up::
	{
		SendKey("{Up}", "YouTube") ; Volume Up
		Return
	}
	
	*Volume_Down::
	{
		SendKey("{Down}", "YouTube") ; Volume Down
		Return
	}
	
	{
	>+Volume_Up::
		SendKey("{l}", "YouTube") ; Seek forwards
		Return
	}
	
	>+Volume_Down::
	{
		SendKey("{j}", "YouTube") ; Seek backward
		Return
	}
	
	>!Right::
	{
		SendKey("+{N}", "YouTube") ; Next video			;here it sends lshift to focused program as well as rshift to browser (why?)
		TriggerVolumeOSD()
		Return
	}
	
	>!Left::
	{
		SendKey("!{Left}", "YouTube") ; Previous Tab/Last Video
		TriggerVolumeOSD()
		Return
	}
	
	>+PgUp::
	{
		SendKey("{f}", "YouTube") ; Activate Mini-Player
		Return
	}
	
	>+PgDn::
	{
		SendKey("{i}", "YouTube") ; Fullscreen to focus player
		Return
	}
	
	^!a::MsgBox YouTube Detected
-------------------------------------------------------------
; OneNote
#If WinExist("abdullah's Notebook") 
	
	^<!LButton::	;LAlt + Mouse1
	{
		Send {PrintScreen}
		Return
	}
	
	^!a::MsgBox Notebook Detected
-------------------------------------------------------------
; Stremio
#If WinExist("Stremio")
	
	*Volume_Up::
	{
		SendKey("{Up}", "Stremio") ; Volume Up
		Return
	}
	
	*Volume_Down::
	{
		SendKey("{Down}", "Stremio") ; Volume Down
		Return
	}
	
	CapsLock & Media_Play_Pause::
	{
		SendKey("{Space}", "Stremio") ; Play/Pause
		Return
	}
	
	>+Volume_Up::
	{
		SendKey("{Right}", "Stremio") ; Seek forwards
		Return
	}
	
	>+Volume_Down::
	{
		SendKey("{Left}", "Stremio") ; Seek backward
		Return
	}
	
	>!Right::
	{
		SendKey("+{N}", "Stremio") ; Next video
		Return
}

^!a::MsgBox Stremio Detected
-------------------------------------------------------------
MicVolume:
If (toggle := !toggle) ; Toggle a variable between true and false
{
	Menu, Tray, Check, Set Microphone Volume
	running := true ; Set a variable to indicate that the loop is running
	Loop ; Start a loop without a label name
	{
		If (!running) ; Check if the variable is false
			Break ; Break out of the loop if it is
		SoundSet, 70, MASTER, VOLUME, 8 ; Set the volume to 70%, 8 corresponds to AT2020 Mic
		Sleep, 600000   ;10 minute delay
	}
	
} 
else 
{
	Menu, Tray, UnCheck, Set Microphone Volume
	running := false ; Set the variable to false to stop the loop
}
return