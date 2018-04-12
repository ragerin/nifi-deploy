@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
if "%SPHINXAPIDOC%" == "" (
    set SPHINXAPIDOC=sphinx-apidoc
)
set SOURCEDIR=source
set BUILDDIR=build
set SPHINXPROJ=nifi-deploy

if "%1" == "" goto help

%SPHINXAPIDOC% >NUL 2>NUL
if errorlevel 9009 (
	echo.The 'sphinx-apidoc' command was not found.
	exit /b 1
)
%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.The 'sphinx-build' command was not found.
	exit /b 1
)

%SPHINXAPIDOC% -o %SOURCEDIR% ..\nifi_deploy\
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%

:end
popd

