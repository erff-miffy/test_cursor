# Arduino CLI helpers (works without Cursor extension commands)
# Usage examples:
#   .\arduino.ps1 verify -Board uno
#   .\arduino.ps1 upload -Board uno -Port COM4
#   .\arduino.ps1 upload -Board mega -Port COM4

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('verify', 'upload', 'ports')]
    [string]$Action,

    [ValidateSet('uno', 'mega')]
    [string]$Board = 'uno',

    [string]$Port = 'COM4',

    [string]$Sketch = "$PSScriptRoot\blink"
)

$Cli = "$env:USERPROFILE\.cursor\extensions\vscode-arduino.vscode-arduino-community-0.7.1\assets\platform\win32-x64\arduino-cli\arduino-cli.exe"
$Fqbn = if ($Board -eq 'mega') { 'arduino:avr:mega' } else { 'arduino:avr:uno' }

if (-not (Test-Path $Cli)) {
    Write-Error "arduino-cli not found: $Cli"
    exit 1
}

switch ($Action) {
    'ports' {
        & $Cli board list
    }
    'verify' {
        & $Cli compile --fqbn $Fqbn $Sketch
    }
    'upload' {
        & $Cli compile --fqbn $Fqbn $Sketch
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        & $Cli upload -p $Port --fqbn $Fqbn $Sketch
    }
}
