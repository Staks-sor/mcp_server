@echo off
chcp 65001 >nul
echo =======================================================
echo     Запуск Сервера DevBoost MCP и Базы Данных (Стенд)
echo =======================================================
echo.

echo Шаг 1: Проверка и создание виртуального окружения (Python)...
if not exist ".venv\" (
    echo Виртуальное окружение не найдено. Создаем .venv...
    python -m venv .venv
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось создать виртуальное окружение. Проверьте установку Python.
        pause
        exit /b 1
    )
) else (
    echo Виртуальное окружение уже существует.
)

echo.
echo Шаг 2: Установка зависимостей проекта (включая DevBoost MCP)...
call .venv\Scripts\activate.bat
pip install -e .
if errorlevel 1 (
    echo [ВНИМАНИЕ] Возникли ошибки при установке зависимостей локально.
    echo Если вы на Python 3.13, эта ошибка ожидаема для пакета asyncpg.
    echo Не страшно, продолжим запуск стенда через Docker!
)

echo.
echo Шаг 3: Собираем основной Docker образ сервера...
docker build -t devboost-mcp .
if errorlevel 1 (
    echo [ОШИБКА] Не удалось собрать Docker образ. Проверьте запущен ли Docker Desktop.
    pause
    exit /b 1
)

echo.
echo Шаг 4: Переходим в папку демо-стенда и запускаем базу данных + сервер...
cd demo_project
docker-compose up -d --build
if errorlevel 1 (
    echo [ОШИБКА] Не удалось запустить стенд через docker-compose.
    pause
    exit /b 1
)

echo.
echo Ожидаем 5 секунд для старта базы данных...
timeout /t 5 /nobreak >nul

echo.
echo URL MCP Сервера (через SSE): http://localhost:8080/mcp
echo.
echo =======================================================
echo.
echo Открываем браузерный интерфейс MCP Inspector...

call npx -y @modelcontextprotocol/inspector --transport sse --server-url http://localhost:8080/sse

pause
