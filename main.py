from pathlib import Path
from ahkunwrapped import Script

ahk = Script.from_file(Path('ReBindexp.ahk'))
ahk.call('MyMsg', "Wooo!")

ahk.call('SendKey', '{Space}')