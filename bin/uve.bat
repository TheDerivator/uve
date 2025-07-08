@echo off
REM -------------------------------------------------
REM Step 1: local parsing environment
SETLOCAL ENABLEDELAYEDEXPANSION

IF "!UVE_DIR!"=="" (
  echo UVE_DIR must be set.
  exit /b 1
)

IF "%1"=="" (
  echo Usage: uve [activate|create|install] [args]
  exit /b 1
)
SET CMD=%1
SHIFT

IF /I "!CMD!" neq "activate" (
  REM echo Executing uvx --no-cache U:\Sync\Projects\uve %*
  REM uvx --no-cache U:\Sync\Projects\uve %*
  echo Executing uvx --find-links %UVE_DIR%\bin uve %*
  uvx --find-links %UVE_DIR%\bin uve %*
  exit /b 1
)

SET "ENVNAME=%1"
IF "!ENVNAME!"=="" (
  echo Missing environment name.
  exit /b 1
)

SET UVE_ACT_PATH=!UVE_DIR!\envs\!ENVNAME!\Scripts\activate.bat
IF NOT EXIST "!UVE_ACT_PATH!" (
    echo No such environment: "!UVE_ACT_PATH!"
    exit /b 1
)

REM Prepare to escape the values out of the SETLOCAL
REM Note: %UV_ENV_DIR% is expanded _now_ (inside SETLOCAL)
ENDLOCAL & (
  set "UVE_ACT_PATH=%UVE_ACT_PATH%"
)

call "%UVE_ACT_PATH%"