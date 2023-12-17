#NoEnv
#MaxHotkeysPerInterval,50000
#SingleInstance Force
#Persistent
#MenuMaskKey vkE8 ; Replace default mask key Ctrl with vkE8 (Unused) 
SetTitleMatchMode 2
DetectHiddenWindows, On
SendMode Input


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