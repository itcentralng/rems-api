@REM RUN A BATCH FILE COMMAND THAT WILL RUN A FLASK APP WHEN EXECUTED
@REM
@REM Author: 	iT Central
@REM Date: 	01/1/2022
@REM Version: 	1.0
@REM

@ECHO OFF
@SETLOCAL
@SET PATH=%PATH%;C:\Documents\REMS\rems-api

@REM CALL PIP INSTALL && FLASK RUN COMMAND

@CALL pip install -r requirements.txt
@CALL ./run

@ENDLOCAL