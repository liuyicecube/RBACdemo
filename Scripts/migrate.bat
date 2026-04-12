@echo off
chcp 65001 >nul
echo ============================================================
echo 企业级RBAC系统 - 数据库迁移工具
echo ============================================================
echo.

cd /d "%~dp0.."

if not exist ".env" (
    echo [警告] 未找到 .env 文件
    if exist ".env.example" (
        echo [提示] 正在从 .env.example 创建 .env 文件...
        copy ".env.example" ".env" >nul
        echo [提示] 请编辑 .env 文件配置数据库连接信息
        echo.
    )
)

echo [信息] 正在执行数据库迁移...
echo.

python Scripts\migrate.py %*

if errorlevel 1 (
    echo.
    echo [错误] 迁移失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo [完成] 迁移成功!
pause
