# Import the ahk package
import ahk

# Create an AHK object
ahk = ahk.AHK()

# Define the global variables
programs = ["Stremio", "YouTube"]
currentProgramIndex = 1 # start with the first program in the list
activeProgram = None

# Define the hotkey for Alt + Delete to toggle the active program
ahk.hotkey("!Delete", lambda: toggleActiveProgram()) # ! is the symbol for Alt in AHK

# Define the toggleActiveProgram function
def toggleActiveProgram():
    global currentProgramIndex, programs, activeProgram
    openPrograms = getOpenPrograms() # Get the list of open programs
    if len(openPrograms) > 1: # Only proceed if more than one program is open
        currentProgramIndex = (currentProgramIndex % len(openPrograms)) + 1 # Cycle through the open program list
        activeProgram = openPrograms[currentProgramIndex - 1] # Update activeProgram
        updateGUI(activeProgram) # Update the GUI with the new active program

# Define the updateGUI function
def updateGUI(program):
    ahk.run_script(f"""
    Gui, Destroy ; Destroy any existing GUI
    Gui, +AlwaysOnTop +ToolWindow -Caption ; Make the GUI always on top and style it as an overlay
    Gui, Font, s20 cBlack, Verdana ; Set the font size to 20 and color to black (adjust as needed)
    Gui, Add, Text,, Now Focused: {program} ; Add text indicating the currently focused program
    WinGetPos, X, Y,,, {program}
    Gui, Show, x%X% y%Y% NoActivate, Focus Indicator ; Show the GUI at the top left corner without activating it
    SetTimer, DestroyGUI, -1500 ; Set a timer to destroy the GUI after 2 seconds
    """) # Use run_script to execute AHK code

# Define the destroyGUI function
def destroyGUI():
    ahk.run_script("Gui, Destroy") # Use run_script to execute AHK code

# Define the getOpenPrograms function
def getOpenPrograms():
    global programs
    openPrograms = [] # Initialize an empty list
    for program in programs:
        if ahk.win_exist(program): # Check if the program is open
            openPrograms.append(program) # Add the program to the list if it is
    return openPrograms

# Define the sendKey function
def sendKey(key):
    global currentProgramIndex, programs
    openPrograms = getOpenPrograms() # Get the list of open programs
    ahk.control_focus("", openPrograms[currentProgramIndex - 1]) # Set focus to the current open program
    ahk.control_send(key, "", openPrograms[currentProgramIndex - 1]) # Send key to the current open program

# Define the triggerVolumeOSD function
def triggerVolumeOSD():
    ahk.send("{Volume_Up 1}") # Send Volume Up key

# Define the hotkeys and hotstrings for the macros and app specific keybinds
ahk.hotkey("~XButton1 & LButton", lambda: rapidFire()) # Rapid Fire
ahk.hotkey("*Volume_Up", lambda: sendKey("{Up}")) # Volume Up
ahk.hotkey("*Volume_Down", lambda: sendKey("{Down}")) # Volume Down
ahk.hotkey("+*Volume_Up", lambda: sendKey("{l}")) # Seek forwards
ahk.hotkey("+*Volume_Down", lambda: sendKey("{j}")) # Seek backward
ahk.hotkey(">!Right", lambda: sendKey("+{N}")) # Next video
ahk.hotkey(">!Left", lambda: sendKey("!{Left}")) # Previous Tab/Last Video
ahk.hotkey("+>PgUp", lambda: sendKey("{f}")) # Activate Mini-Player
ahk.hotkey("+>PgDn", lambda: sendKey("{i}")) # Fullscreen to focus player
ahk.hotkey("^!a", lambda: ahk.msgbox("YouTube Detected")) # MsgBox YouTube Detected

# Define the rapidFire function
def rapidFire():
    while ahk.get_key_state("LButton", "P") and ahk.get_key_state("XButton1", "P"): # Check if both buttons are pressed
        ahk.send("{LButton down}") # Send left mouse button down
        ahk.sleep(7) # Sleep for 7 milliseconds
        ahk.send("{LButton up}") # Send left mouse button up
        ahk.sleep(7) # Sleep for 7 milliseconds

# Initialize the GUI
openPrograms = getOpenPrograms() # Get the list of open programs
if len(openPrograms) > 0: # Only show the GUI if at least one program is open
    updateGUI(openPrograms[0]) # Show the initial GUI with the first open program
