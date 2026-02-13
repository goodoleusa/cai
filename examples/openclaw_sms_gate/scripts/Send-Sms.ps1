<#
    Send-Sms.ps1 - Send a text via SMS-Gate
    Parameters:
        -Phone   : Destination number in E.164 format (e.g. +11234567890)
        -Message : Message body
#>

param(
    [Parameter(Mandatory=$true)][string]$Phone,
    [Parameter(Mandatory=$true)][string]$Message
)

$authHeader = "Basic $env:SMSGATE_AUTH"

$payload = @{
    textMessage = @{ text = $Message }
    phoneNumbers = @($Phone)
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod `
    -Method Post `
    -Uri "https://api.sms-gate.app/3rdparty/v1/messages" `
    -Headers @{ Authorization = $authHeader } `
    -ContentType "application/json" `
    -Body $payload

$response | ConvertTo-Json -Depth 5
