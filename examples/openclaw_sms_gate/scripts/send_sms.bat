@echo off
REM -------------------------------------------------
REM send_sms.bat  -  Send a text via SMS-Gate
REM -------------------------------------------------
REM Arguments:
REM   %1 = phone number (E.164, e.g. +11234567890)
REM   %2 = message text (quotes required if spaces)
REM -------------------------------------------------

if "%~1"=="" (
    echo Usage: send_sms.bat ^<phone^> ^<message^>
    exit /b 1
)

set "PHONE=%~1"
set "TEXT=%~2"

curl -X POST ^
     -H "Authorization: Basic %SMSGATE_AUTH%" ^
     -H "Content-Type: application/json" ^
     --data "{\"textMessage\":{\"text\":\"%TEXT%\"},\"phoneNumbers\":[\"%PHONE%\"]}" ^
     https://api.sms-gate.app/3rdparty/v1/messages

exit /b %ERRORLEVEL%
