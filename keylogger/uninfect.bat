@echo off
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v AVAADA /f
attrib -s -h -r %cd%\keylogger.exe
taskkill /f /im keylogger.exe
del %cd%\keylogger.exe
