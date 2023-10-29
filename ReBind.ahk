;THIS WORKS
;this dynamically changes activeProgram every 5 seconds super simple logic but it works

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

; Add the hotkey for Alt + Delete to toggle the active program
!Delete::ToggleActiveProgram()  ; ! is the symbol for Alt in AHK

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

CheckPrograms:
	if (WinExist("YouTube") and !WinExist("Stremio"))
	{
		activeProgram := "YouTube"
	}
	else if (!WinExist("YouTube") and WinExist("Stremio"))
	{
		activeProgram := "Stremio"
	}
return

; Define ToggleActiveProgram function
ToggleActiveProgram() {
    global currentProgramIndex, programs, activeProgram
    openPrograms := GetOpenPrograms()  ; Get the list of open programs
    if (openPrograms.Length() > 1) {  ; Only proceed if more than one program is open
        currentProgramIndex := Mod(currentProgramIndex, openPrograms.Length()) + 1  ; Cycle through the open program list
        activeProgram := openPrograms[currentProgramIndex]  ; Update activeProgram
        UpdateGUI(activeProgram)  ; Update the GUI with the new active program
    }
}

; Update SendKey function to use currentProgram from the list of open programs
SendKey(Key) {
    global currentProgramIndex, programs
    openPrograms := GetOpenPrograms()  ; Get the list of open programs
    ControlFocus,, % openPrograms[currentProgramIndex]  ; Set focus to the current open program
    ControlSend,, %Key%, % openPrograms[currentProgramIndex]  ; Send key to the current open program
    Return  ; clear buffer
}

; Define UpdateGUI function
UpdateGUI(program) {
    Gui, Destroy  ; Destroy any existing GUI
    Gui, +AlwaysOnTop +ToolWindow -Caption ; Make the GUI always on top and style it as an overlay
    ;Gui, Color, EEAA99 ; Set a background color (optional, you can remove this line for a completely transparent GUI)
    Gui, Font, s20 cBlack, Verdana ; Set the font size to 20 and color to black (adjust as needed)
    Gui, Add, Text,, Now Focused: %program%  ; Add text indicating the currently focused program
	WinGetPos, X, Y,,, %program%
    Gui, Show, x%X% y%Y% NoActivate, Focus Indicator ; Show the GUI at the top left corner without activating it
    SetTimer, DestroyGUI, -1500  ; Set a timer to destroy the GUI after 2 seconds
}

; New function to destroy the GUI when the timer triggers
DestroyGUI:
    Gui, Destroy
return

; Define GetOpenPrograms function
GetOpenPrograms() {
    global programs
    openPrograms := []  ; Initialize an empty array
    for index, program in programs {
        if WinExist(program)
            openPrograms.Push(program)  ; Add the program to the list if it's open
    }
    return openPrograms
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
#If (activeProgram = "YouTube")
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

	{
	>+Volume_Up::
		SendKey("{l}") ; Seek forwards
		Return
	}
	
	>+Volume_Down::
	{
		SendKey("{j}") ; Seek backward
		Return
	}
	
	>!Right::
	{
		SendKey("+{N}") ; Next video			;here it sends lshift to focused program as well as rshift to browser (why?)
		TriggerVolumeOSD()
		Return
	}
	
	>!Left::
	{
		SendKey("!{Left}") ; Previous Tab/Last Video
		TriggerVolumeOSD()
		Return
	}
	
	>+PgUp::
	{
		SendKey("{f}") ; Activate Mini-Player
		Return
	}
	
	>+PgDn::
	{
		SendKey("{i}") ; Fullscreen to focus player
		Return
	}
	
	^!a::MsgBox YouTube Detected
#If
;-------------------------------------------------------------
; Stremio
#If (activeProgram = "Stremio")
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
	
	Media_Play_Pause::
	{
		SendKey("{Space}") ; Play/Pause
		Return
	}
	
	>+Volume_Up::
	{
		SendKey("{Right}") ; Seek forwards
		Return
	}
	
	>+Volume_Down::
	{
		SendKey("{Left}") ; Seek backward
		Return
	}
	
	>!Right::
	{
		SendKey("+{N}") ; Next video
		Return
	}

	>+PgUp::
	{
		SendKey("{f}") ; Activate Mini-Player
		Return
	}

	^!a::MsgBox Stremio Detected
#If
;-------------------------------------------------------------
;< ---------------- Preflight Check ---------------- >
PreFlightCheck:
{
    IniRead, toggleLoopMicVolumeValue, %A_ScriptDir%\config.ini, Settings, ToggleLoopMicVolume
    IniRead, toggleFKeyRebindValue, %A_ScriptDir%\config.ini, Settings, ToggleFKeyRebind

    if (toggleLoopMicVolumeValue = 1) {
        SetTimer LoopMicVolume, -1
    }

    if (toggleFKeyRebindValue = 1) {
        SetTimer FKeyRebind, -1
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
{
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
}
; Initialize the GUI
openPrograms := GetOpenPrograms()  ; Get the list of open programs
if (openPrograms.Length() > 0) {  ; Only show the GUI if at least one program is open
    UpdateGUI(openPrograms[1])  ; Show the initial GUI with the first open program
}
