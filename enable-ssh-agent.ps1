# Run this script as Administrator (right-click -> Run with PowerShell as admin)
# One-time setup for Windows OpenSSH Authentication Agent

Set-Service ssh-agent -StartupType Manual
Start-Service ssh-agent

Write-Host "ssh-agent status:"
Get-Service ssh-agent | Format-List Name, Status, StartType

Write-Host "Adding SSH key..."
ssh-add $env:USERPROFILE\.ssh\id_ed25519

Write-Host "Loaded keys:"
ssh-add -l
