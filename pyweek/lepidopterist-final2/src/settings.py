import sys

resolution = 800, 400
showdots = "--showdots" in sys.argv
printfps = "--printfps" in sys.argv
nosound = "--nosound" in sys.argv
nomusic = "--nomusic" in sys.argv
restart = "--restart" in sys.argv
cheat = "--cheat" in sys.argv
unlockall = "--unlockall" in sys.argv
alwaysshow = "--alwaysshow" in sys.argv  # Repeat cutscenes
hidefeatnames = "--hidefeatnames" in sys.argv
easy = False  # Easy mode

savefile = "savegame"
for arg in sys.argv:
    if arg.startswith("--savefile="):
        savefile = arg[11:]

money0 = 0
for arg in sys.argv:
    if arg.startswith("--money="):
        money0 = int(arg[8:])



