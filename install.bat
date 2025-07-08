setx UVE_DIR C:\uve
set UVE_DIR=C:\uve
mkdir %UVE_DIR%
mkdir %UVE_DIR%\bin
mkdir %UVE_DIR%\envs
uv build .
copy dist\*whl %UVE_DIR%\bin
copy bin\uve.bat %UVE_DIR%\bin
REM refresh the package cache
uvx --refresh-package uve --find-links %UVE_DIR%\bin uve env list