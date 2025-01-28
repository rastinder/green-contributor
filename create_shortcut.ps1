$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Green Contributor.lnk")
$Shortcut.TargetPath = "D:\projects\all_green\start_hidden.vbs"
$Shortcut.WorkingDirectory = "D:\projects\all_green"
$Shortcut.Description = "GitHub Green Contributor Automation"
$Shortcut.IconLocation = "C:\Windows\System32\SHELL32.dll,238"
$Shortcut.Save()

Write-Host "Startup shortcut has been created successfully!"
Write-Host "Location: $env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Green Contributor.lnk"
Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')