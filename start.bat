where uv >nul 2>&1
if errorlevel 1 (
	echo 'uv' not found
	powershell -NoProfile -ExecutionPolicy Bypass -Command "irm 'https://astral.sh/uv/install.ps1' | iex"
	if errorlevel 1 (
		echo Failed to install 'uv'. Please install manually and re-run.
		endlocal
		exit /b 1
	)

    set "PATH=%PATH%;%USERPROFILE%\.local\bin;"
    where uv >nul 2>&1
    if errorlevel 1 (
        echo Unable to locate 'uv' after install. Please restart your shell or add uv to PATH manually.
        exit /b 1
    )
)

uv sync
uv run src/main.py
pause