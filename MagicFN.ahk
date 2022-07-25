#NoEnv
#MaxHotkeysPerInterval,50000
#SingleInstance Force
SetTitleMatchMode 2
DetectHiddenWindows, On

;disable numlock and capslock
SetNumLockState, AlwaysOff
SetCapsLockState, AlwaysOff

;reload program in case of edge case failure
^!r::Reload
;close program
^!e::ExitApp

;core rebind
CapsLock & 1:: F1
CapsLock & 3:: F3
CapsLock & 2:: F2
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
If (GetKeyState(CapsLock,"p")) {
	; fn + wheel to skip and go back on media
	CapsLock & Volume_Up::Media_Next
	CapsLock & Volume_Down::Media_Prev
}
-------------------------------------------------------------
; Universal Methods
-------------------------------------------------------------
; SendKey Method
SendKey(Key)
{
    ControlFocus
    ControlSend ahk_parent, % Key
	Return
}

; Get the HWND of the Spotify main window.
getSpotifyHwnd() {
	WinGet, spotifyHwnd, ID, ahk_exe spotify.exe
	Return spotifyHwnd
}

; Send a key to Spotify.
spotifyKey(key)  { 
	spotifyHwnd := getSpotifyHwnd()
	; Chromium ignores keys when it isn't focused.
	; Focus the document window without bringing the app to the foreground.
	ControlFocus, Chrome_RenderWidgetHostHWND1, ahk_id %spotifyHwnd%
	ControlSend, , %key%, ahk_id %spotifyHwnd%
	Return
}
-------------------------------------------------------------
; App specific keybinds
-------------------------------------------------------------
; YouTube
#IfWinExist, YouTube
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

	RAlt & Volume_Up::
	{
		SendKey("{Right}") ; Seek forwards
		Return
	}
		
	RAlt & Volume_Down::
	{
		SendKey("{Left}") ; Seek backward
		Return
	}

	RAlt & Right::
	{
		SendKey("+{N}") ; Next video
		Return
	}

	^!a::MsgBox YouTube Detected
}
-------------------------------------------------------------
; Stremio
#IfWinExist, Stremio 
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
		SendKey("{Space}") ; Volume Down
		Return
	}

	RAlt & Volume_Up::
	{
		SendKey("{Right}") ; Seek forwards
		Return
	}
		
	RAlt & Volume_Down::
	{
		SendKey("{Left}") ; Seek backward
		Return
	}
	
	RAlt & Right::
	{
		SendKey("+{N}") ; Next video
		Return
	}

	^!a::MsgBox Stremio Detected
}
-------------------------------------------------------------
; Spotify
#IfWinExist, Spotify
{
	*Volume_Up::
	{
		spotifyKey("^{Up}") ; Volume Up
		Return
	}

	*Volume_Down::
	{
		spotifyKey("^{Down}") ; Volume Down
		Return
	}

	RAlt & Volume_Up::
	{
		spotifyKey("+{Right}") ; Seek forwards
		Return
	}
		
	RAlt & Volume_Down::
	{
		spotifyKey("+{Left}") ; Seek backward
		Return
	}

	^!a::MsgBox Spotify Detected
}
-------------------------------------------------------------