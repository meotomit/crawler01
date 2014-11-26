@echo off
rem cd /d %0\..
cd /d %~dp0
java -Xms512M -jar vn.hus.nlp.tokenizer-4.1.1.jar %*
if NOT "%COMSPEC%" == "%SystemRoot%\system32\cmd.exe" goto end
if %errorlevel% == 9009 echo Java is not in your PATH. Cannot run program.
if errorlevel 1 pause

:end
