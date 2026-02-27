#!/bin/sh

set -e

# Убедимся, что мы в виртуальном окружении
export PATH="/app/.venv/bin:$PATH"

CMD=$1

if [ "$CMD" = "smoke" ]; then
    echo "Running smoke test..."
    # Пытаемся запустить сервер в фоне и проверить health
    fastmcp run src/devboost/server.py:mcp --transport sse --host 0.0.0.0 --port 8000 --path /mcp &
    PID=$!
    
    # Даем серверу время на старт
    sleep 3
    
    # Проверяем health
    echo "Checking /health endpoint..."
    if curl -s -f http://127.0.0.1:8000/health > /dev/null; then
        echo "✅ Smoke test passed: /health is reachable"
        kill $PID
        exit 0
    else
        echo "❌ Smoke test failed: /health is not reachable"
        kill $PID
        exit 1
    fi
elif [ "$CMD" = "serve" ]; then
    echo "Starting MCP Server in SSE mode on port 8000..."
    exec fastmcp run src/devboost/server.py:mcp --transport sse --host 0.0.0.0 --port 8000 --path /mcp
else
    echo "Usage: docker run IMAGE [serve|smoke]"
    exit 1
fi
