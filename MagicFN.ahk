#MaxHotkeysPerInterval,50000

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

;capslock state so it does not overwrite osd flyout when using capslock + volume~~~      
If (GetKeyState(CapsLock,"p")) {
	; fn + wheel to skip and go back on media
	CapsLock & Volume_Up::Media_Next
	CapsLock & Volume_Down::Media_Prev
}

; otherwise volume for chrome and spotify (media sources)
; * to bypass shift, control, alt esc macro override
*Volume_Up::run "C:\Tools\MagicFN\Resources\soundvolumeview\SoundVolumeView.exe" /ChangeVolume "Chrome" +3 /ChangeVolume "Spotify" +7 /ChangeVolume "WWAHost.exe" +7
*Volume_Down::run "C:\Tools\MagicFN\Resources\soundvolumeview\SoundVolumeView.exe" /ChangeVolume "Chrome" -3 /ChangeVolume "Spotify" -3 /ChangeVolume "WWAHost.exe" -3
