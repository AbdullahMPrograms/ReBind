#NoEnv
#MaxHotkeysPerInterval,50000
#SingleInstance Force
#MenuMaskKey vkE8 ; Replace default mask key Ctrl with vkE8 (Unused) 
;^ MenuMaskKey does not fix misinput in games
SetTitleMatchMode 2
DetectHiddenWindows, On
SendMode Input

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
CapsLock & 0:: F10
CapsLock & -:: F11
CapsLock & =:: F12
CapsLock & Esc:: `
-------------------------------------------------------------
; De-activate volume wheel
*Volume_Up::Return
*Volume_Down::Return
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

; SendKey Method
SendKey(Key) {
	ControlFocus
	ControlSend ahk_parent, % Key
	Return 									; clear buffer
}

-------------------------------------------------------------
; Universal Game Keybinds
-------------------------------------------------------------
;Rapid Fire 
~XButton1 & LButton::
{
	RapidFire()
	Return
}

;CapsLock & l::
;{
;	WinGetTitle, title, A
;	MsgBox, "%title%"
;	return
;}

;Screenshot
<!Delete:: 
{
	Send {PrintScreen}
	Return
}	
-------------------------------------------------------------
; App specific keybinds
-------------------------------------------------------------
; YouTube
#If WinExist("YouTube")
{
	
	*RShift::Return
	
	*Volume_Up::
	{
		SendKey("{Up}") ; Volume Up
		Return
	}
	
	*Volume_Down::
	{
		SendKey("{Down}") ; Volume Down
		Return
	}
	
	RShift & Volume_Up::
	{
		SendKey("{l}") ; Seek forwards
		Return
	}
	
	RShift & Volume_Down::
	{
		SendKey("{j}") ; Seek backward
		Return
	}
	
	RShift & Right::
	{
		SendKey("+{N}") ; Next video
		Return
	}
	
	RShift & Left::
	{
		SendKey("!{Left}") ; Previous Tab/Last Video
		Return
	}
	
	RShift & PgUp::
	{
		SendKey("{f}") ; Activate Mini-Player
		Return
	}
	
	RShift & PgDn::
	{
		SendKey("{i}") ; Fullscreen to focus player
		Return
	}
	
	^!a::MsgBox YouTube Detected
}
-------------------------------------------------------------
; OneNote
#If WinExist("abdullah's Notebook") 
{
	XButton2 & LButton::	;LAlt + Mouse1
	{
		Send {PrintScreen}
		Return
	}
	
	^!a::MsgBox Notebook Detected
}
-------------------------------------------------------------
; Stremio
#If WinExist("Stremio")
{
	*Volume_Up::
	{
		SendKey("{Up}") ; Volume Up
		Return
	}
	
	*Volume_Down::
	{
		SendKey("{Down}") ; Volume Down
		Return
	}
	
	CapsLock & Media_Play_Pause::
	{
		SendKey("{Space}") ; Play/Pause
		Return
	}
	
	RShift & Volume_Up::
	{
		SendKey("{Right}") ; Seek forwards
		Return
	}
	
	RShift & Volume_Down::
	{
		SendKey("{Left}") ; Seek backward
		Return
	}
	
	RShift & Right::
	{
		SendKey("+{N}") ; Next video
		Return
	}
	
	^!a::MsgBox Stremio Detected
}
-------------------------------------------------------------
