' Get the script directory
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
strPath = "D:\projects\all_green"

' Change to the correct directory
objShell.CurrentDirectory = strPath

' Run the batch file minimized (0=hidden, 6=minimized)
objShell.Run "cmd /c " & strPath & "\start_contributor.bat", 6, True

' Clean up
Set objShell = Nothing
Set objFSO = Nothing