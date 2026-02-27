#!/bin/bash
echo "======================================================="
echo "    Запуск Сервера DevBoost MCP и Базы Данных (Стенд)  "
echo "======================================================="
echo ""

echo "Шаг 1: Проверка и создание виртуального окружения (Python)..."
if [ ! -d ".venv" ]; then
    echo "Виртуальное окружение не найдено. Создаем .venv..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[ОШИБКА] Не удалось создать виртуальное окружение. Проверьте установку Python3."
        exit 1
    fi
else
    echo "Виртуальное окружение уже существует."
fi

echo ""
echo "Шаг 2: Установка зависимостей проекта (включая DevBoost MCP)..."
source .venv/bin/activate
pip install -e .
if [ $? -ne 0 ]; then
    echo "[ВНИМАНИЕ] Возникли ошибки при установке зависимостей локально."
    echo "Возможно, у вас отсутствует компилятор C (build-essential). "
    echo "Не страшно, продолжим запуск стенда через Docker!"
fi

echo ""
echo "Шаг 3: Собираем основной Docker образ сервера..."
docker build -t devboost-mcp .
if [ $? -ne 0 ]; then
    echo "[ОШИБКА] Не удалось собрать Docker образ. Проверьте запущен ли daemon Docker."
    exit 1
fi

echo ""
echo "Шаг 4: Переходим в папку демо-стенда и запускаем базу данных + сервер..."
cd demo_project || exit
docker-compose up -d --build
if [ $? -ne 0 ]; then
    echo "[ОШИБКА] Не удалось запустить стенд через docker-compose."
    exit 1
fi

echo ""
echo "Ожидаем 5 секунд для старта базы данных..."
sleep 5

echo ""
echo "URL MCP Сервера (через SSE): http://localhost:8080/mcp"
echo ""
echo "======================================================="
echo ""
echo "Открываем браузерный интерфейс MCP Inspector..."

npx -y @modelcontextprotocol/inspector --transport sse --server-url http://localhost:8080/sse
