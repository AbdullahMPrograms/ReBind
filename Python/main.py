from pathlib import *
from ahkunwrapped import *
import keyboard

ahk = Script.from_file(Path('AHK/ReBind.ahk'))
def send_space(key):
    ahk.call('SendKey', 'key')
    print("Sent Key")

keyboard.add_hotkey('ctrl+space', lambda: send_space("{Space}"))

# Block forever, to keep the script running.
keyboard.wait() 