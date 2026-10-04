@echo off
chcp 65001 >nul

REM 切换到脚本所在目录（项目根目录，与 manage.py 同级）
cd /d "%~dp0"

REM 启动 Django 开发服务器（端口 8080）
REM Django 4.2 仅兼容 Python 3.8~3.12，优先用 py 启动器选择 3.11；
REM 若本机没有 3.11，则回退到 PATH 中的 python
py -3.11 -c "import django" >nul 2>nul
if %errorlevel%==0 (
    py -3.11 manage.py runserver 8080
) else (
    python manage.py runserver 8080
)

REM 服务器停止后暂停，方便查看输出与错误信息
pause
