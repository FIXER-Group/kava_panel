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
:::: Do stuff here
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py hypercorn kava.asgi:application
:::: Return to menu
goto :Menu


:Option2
:::: Do stuff here
hypercorn kava.asgi:application

:::: Return to menu
goto :Menu


:Option3

goto :End


:::: End of file. Pause and clean up
:End
echo.
echo Exiting....
echo.

pause

cls