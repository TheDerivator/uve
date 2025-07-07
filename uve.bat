@echo off
REM -------------------------------------------------
REM Step 1: local parsing environment
SETLOCAL ENABLEDELAYEDEXPANSION

IF "%1"=="" (
  echo Usage: uve activate name
  exit /b 1
)
SET CMD=%1
SHIFT

IF /I "!CMD!" neq "activate" (
  echo Only activate is implemented in this demo.
  exit /b 1
)

SET "ENVNAME=%1"
IF "!ENVNAME!"=="" (
  echo Missing environment name.
  exit /b 1
)
IF "!UV_ENV_DIR!"=="" (
  echo UV_ENV_DIR must be set.
  exit /b 1
)

REM Prepare to escape the values out of the SETLOCAL
REM Note: %UV_ENV_DIR% and %ENVNAME% are expanded _now_ (inside SETLOCAL)
ENDLOCAL & (
  set "ENVNAME=%ENVNAME%"
  set "UV_ENV_DIR=%UV_ENV_DIR%"
)

REM -------------------------------------------------
REM Step 2: call the real activate in the live shell
SET "ACT=%UV_ENV_DIR%\%ENVNAME%\Scripts\activate.bat"
IF NOT EXIST "%ACT%" (
  echo No such environment: "%ACT%"
  exit /b 1
)

call "%ACT%"