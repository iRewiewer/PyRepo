import ctypes, random, time, math

rng = 8 # random.randint(1, 20)

#  Message Box Styles:
#  0 : OK
#  1 : OK | Cancel
#  2 : Abort | Retry | Ignore
#  3 : Yes | No | Cancel
#  4 : Yes | No
#  5 : Retry | Cancel 
#  6 : Cancel | Try Again | Continue

match rng:
    case 1:
        # Message box 'n' times
        i = random.randint(1, 3)
        while i > 0:
            ctypes.windll.user32.MessageBoxW(0, f"Catastrophic Error\nRetry ({i - 2})", "Error", 5)
            time.sleep(random.randint(1, 2))
            i -= 1

    case 2:
        # Screen off ; Screen on
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)

    case 3:
        # Select whole screen (multi monitor setup)
        ctypes.windll.user32.SetCursorPos(0, 0)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left click down
        ctypes.windll.user32.SetCursorPos(ctypes.windll.user32.GetSystemMetrics(78), ctypes.windll.user32.GetSystemMetrics(79))

    case 4:
        # Move mouse randomly for a 'n' seconds
        i = random.randint(4, 8)
        while i > 0:
            monitor_x = ctypes.windll.user32.GetSystemMetrics(0)
            monitor_y = ctypes.windll.user32.GetSystemMetrics(1)

            ctypes.windll.user32.SetCursorPos(random.randint(0, monitor_x), random.randint(0, monitor_y))
            time.sleep(0.5)
            i -= 1
    
    case 5:
        # Mouse mouse mathematically
        for i in range(500):
            monitor_x = ctypes.windll.user32.GetSystemMetrics(0)
            monitors_x = ctypes.windll.user32.GetSystemMetrics(78)
            monitors_y = ctypes.windll.user32.GetSystemMetrics(79)
            x = int(math.sin(math.pi * i / 200) * monitors_x / 2) + int(monitor_x / 2)
            y = int(math.cos(i) * monitors_y)
            print(x, y)
            ctypes.windll.user32.SetCursorPos(x, y)
            time.sleep(.01)

    case 6:
        # Logout
        ctypes.windll.user32.ExitWindowsEx(0, 1)

    case 7:
        # Popup 'n' message boxes at once
        ctypes.windll.user32.MessageBoxW(0, "Try again!", f"Error", 0)

    case 8:
        # Cursed text
        cursedLetters = "°‹EÜ‰E¸‹Eà‰E´‹Eì‰EÄ‹EèV‰EÀÿÀ ë9‹EÀ‰E´‹E¼‰E¸‹E ‰EÀ‹EœV‰EÄÿÀ ë‹EÀ‰E´‹E¼‰E¸‹E ‰EÀ‹Eœ‰EÄ;}¨t	WèuƒÄ‹}¤‹u°‹ÿu¬W‹@lÿÐ‰E¬…À„ÿÿÿƒÃ,‹ËQf‹ƒÁf…Àuõ‹+ÊÑùQS‹€Œ  WÿÐ‹È…É„Ýþÿÿ‹‹]¬Qÿ5Ä ‹€   SWÿÐ‹Vÿ5È‹€´  SWÿÐÿu´‹ÿu¸ÿ5Ì ‹€¸  SWÿÐÿuÀ‹ÿuÄÿ5Ð ‹€¸  SWÿÐ‹Mü‹Ã_^3Í[èø  ‹å]ÃÌÌÌÌÌÌÌÌÌÌÌÌU‹ìƒì"
        cursedText = ''.join(random.choice(cursedLetters) for _ in range(random.randint(100, 200))) + '?'
        cursedTitle = ''.join(random.choice(cursedLetters) for _ in range(random.randint(20, 40)))
        ctypes.windll.user32.MessageBoxW(0, cursedText, cursedTitle, 4)

    case _:
        # Simple message box
        ctypes.windll.user32.MessageBoxW(0, "League client could not start.", "Error", 0)