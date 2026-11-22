@echo off
REM Menjalankan Apache Jena Fuseki 6.x dengan SahamExpertKB v2 (Windows)
REM Pemakaian: start_fuseki.bat C:\path\apache-jena-fuseki-6.2.0
set DIR=%~dp0
set DIR=%DIR:~0,-1%
set FUSEKI_HOME=%1
if "%FUSEKI_HOME%"=="" set FUSEKI_HOME=%USERPROFILE%\Downloads\apache-jena-fuseki-6.2.0
set DIRURI=%DIR:\=/%
powershell -Command "(Get-Content '%DIR%\config_saham.template.ttl') -replace '__DIR__', '/%DIRURI%' | Set-Content '%DIR%\config_saham.ttl'"
java -version
cd /d "%FUSEKI_HOME%"
call fuseki-server.bat --config="%DIR%\config_saham.ttl"
