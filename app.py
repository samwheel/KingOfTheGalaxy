#! /Users/Samwise/Projects/Python/KingOfTheGalaxy/.venv/bin/python

import webview
webview.create_window('King of the Galaxy', 'http://localhost:5173', width=1200, height=800, resizable=True, fullscreen=False, min_size=(800, 600))
webview.start()