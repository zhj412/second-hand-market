@echo off
chcp 65001 >nul

REM 切换到脚本所在目录（项目根目录，与 manage.py 同级）
cd /d "%~dp0"

REM 启动 Django 开发服务器（端口 8080）
REM 优先使用 python 命令；若未加入 PATH，则回退到 Windows 的 py 启动器
where python >nul 2>nul
if %errorlevel%==0 (
    python manage.py runserver 8080
) else (
    py manage.py runserver 8080
)

REM 服务器停止后暂停，方便查看输出与错误信息
pause
