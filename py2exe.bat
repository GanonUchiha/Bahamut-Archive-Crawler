conda activate base & ^
pyinstaller -F crawler_interactive.py & ^
move /y %cd%\dist\crawler_interactive.exe %cd% & ^
rmdir dist build __pycache__ /S /Q & del *.spec & pause