#!/bin/bash
echo "======================================================="
echo "       Запуск MCP Inspector (Панель Управления)        "
echo "======================================================="
echo ""
echo "Внимание: Требуется установленный Node.js (npx)."
echo "При первом запуске скачивание может занять около минуты."
echo ""
echo "Подключение к серверу по адресу: http://localhost:8080/mcp"
echo ""

npx -y @modelcontextprotocol/inspector SSE http://localhost:8080/mcp
