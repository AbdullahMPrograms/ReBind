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

;< ---------------- TRAY MENU ---------------- >
Menu, tray, nostandard ; removes original menu
Menu, Tray, Add, Set Microphone Volume, LoopMicVolume ; Add a menu item named "Set Microphone Volume" that calls the subroutine "MicVolume"
Menu, Tray, Add, F-Key Rebind, FKeyRebind 
Menu, Tray, Add ; Seperator
Menu, Tray, Standard ; puts original back "under" custom menu

SetTimer PreFlightCheck, -1 ; Run PreFlightCheck once on script start

;reload program in case of edge case failure
^!r::Reload
;-------------------------------------------------------------
; Deactivate volume wheel
*Volume_Up::Return
*Volume_Down::Return
;-------------------------------------------------------------
; If FN (CapsLock) is pressed Next Media
While (GetKeyState(CapsLock,"p")) {
	; fn + wheel to skip and go back on media
	CapsLock & Volume_Up::Media_Next
	CapsLock & Volume_Down::Media_Prev
}
;-------------------------------------------------------------
; Methods
;-------------------------------------------------------------
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

;-------------------------------------------------------------
; Macros
;-------------------------------------------------------------
;Rapid Fire 
~XButton1 & LButton::
{
	RapidFire()
	Return
}	
;-------------------------------------------------------------
; App specific keybinds
;-------------------------------------------------------------
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
;-------------------------------------------------------------
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
;-------------------------------------------------------------
;< ---------------- Preflight Check ---------------- >
PreFlightCheck:
{
    IniRead, toggleLoopMicVolumeValue, %A_ScriptDir%\config.ini, Settings, ToggleLoopMicVolume
    IniRead, toggleFKeyRebindValue, %A_ScriptDir%\config.ini, Settings, ToggleFKeyRebind

    if (toggleLoopMicVolumeValue = 1) 
    {
        SetTimer LoopMicVolume, -1
		;return
    }

    if (toggleFKeyRebindValue = 1) 
    {
        SetTimer FKeyRebind, -1
		;return
    }

    return
}
;< ---------------- Scripts ---------------- >
LoopMicVolume:
{
	If (toggleLoopMicVolume := !toggleLoopMicVolume) ; Toggle a variable between true and false
	{
		Menu, Tray, Check, Set Microphone Volume
		running := true ; Set a variable to indicate that the loop is running
		;Msgbox "Toggled On"
		IniWrite, %toggleLoopMicVolume%, %A_ScriptDir%\config.ini, Settings, ToggleLoopMicVolume
		Loop ; Start a loop without a label name
		{
			If (!running) ; Check if the variable is false
				Break ; Break out of the loop if it is
			SoundSet, 70, MASTER, VOLUME, 7 ; Set the volume to 70%, 8 corresponds to AT2020 Mic
			Sleep, 600000   ;10 minute delay
		}
		
	} 
	else 
	{
		;Msgbox "Toggled Off"
		Menu, Tray, UnCheck, Set Microphone Volume
		running := false ; Set the variable to false to stop the loop
		IniWrite, %toggleLoopMicVolume%, %A_ScriptDir%\config.ini, Settings, ToggleLoopMicVolume
	}
	return
}

FKeyRebind:
{
	If (toggleFKeyRebind := !toggleFKeyRebind) ; Toggle a variable between true and false
	{
		Menu, Tray, Check, F-Key Rebind
		IniWrite, %toggleFKeyRebind%, %A_ScriptDir%\config.ini, Settings, ToggleFKeyRebind
		RemapToggle := true
		;Msgbox "Toggled On"
	} 
	else 
	{
		Menu, Tray, UnCheck, F-Key Rebind
		IniWrite, %toggleFKeyRebind%, %A_ScriptDir%\config.ini, Settings, ToggleFKeyRebind
		RemapToggle := false
		;Msgbox "Toggled Off"
	}
	return
}

#IF RemapToggle
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