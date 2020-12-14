@echo off

:Menu
echo Kava-panel launch script
echo 1) First time launch
echo 2) Normal launch
echo 3) Exit
echo.
choice /C:123 /M Choice?


if ERRORLEVEL 3 (
goto :End
)

if ERRORLEVEL 2 (
goto :Option2
)

if ERRORLEVEL 1 (
goto :Option1
)


:Option1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
uvicorn kava.asgi:application --host 0.0.0.0
goto :End


:Option2
uvicorn kava.asgi:application --host 0.0.0.0

goto :End



goto :End


:End
echo.
echo Exiting....
echo.

pause

cls