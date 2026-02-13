# Setup SMSGATE_AUTH environment variable (PowerShell)
# Run: .\setup_credentials.ps1
# Replace USERNAME and PASSWORD with your SMS-Gate API credentials

# Replace with your SMS-Gate API credentials
$username = "YOUR_USERNAME"
$password = "YOUR_PASSWORD"

$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${username}:${password}"))
[Environment]::SetEnvironmentVariable("SMSGATE_AUTH", $cred, "User")

Write-Host "SMSGATE_AUTH has been set. Restart your terminal for changes to take effect."
