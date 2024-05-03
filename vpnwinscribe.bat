@echo off
cd "C:\Program Files\Windscribe"
set username=tek13181
set password=Jasper13
start Windscribe.exe --username %username% --password %password% --connect
timeout 10
exit
