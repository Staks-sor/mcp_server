FROM python:3.10-slim

WORKDIR /app

# Устанавливаем системные утилиты, необходимые для инструментов (lsof, postgres client)
RUN apt-get update && apt-get install -y \
    lsof \
    net-tools \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем проект
COPY . /app/

# Устанавливаем зависимости и сам пакет через pip (poetry не ставим ради простоты демо)
RUN pip install --no-cache-dir build && \
    pip install -e .

# Создаем не-root пользователя (чтобы kill_port_hog был более безопасен, хотя внутри докера он один)
RUN useradd -m devboostuser
USER devboostuser

# Сервер FastMCP работает через stdio, поэтому открывать порты не нужно
# При запуске из Claude Desktop / Inspector он будет общаться через stdin/stdout
ENTRYPOINT ["devboost"]
