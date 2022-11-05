@REM RUN A BATCH FILE COMMAND THAT WILL RUN A FLASK APP WHEN EXECUTED
@REM
@REM Author: 	iT Central
@REM Date: 	01/1/2022
@REM Version: 	1.0
@REM

@ECHO OFF
@SETLOCAL
@SET PATH=%PATH%;C:\Users\LENOVO\Documents\REMS\rems-api-main\rems-api-main
@SET DATABASE_URI=postgresql://postgres:adamu@localhost:5432/rems
@SET FLASK_APP=main
@SET FLASK_DEBUG=1
@CALL flask db upgrade
@CALL flask run 
@ENDLOCAL