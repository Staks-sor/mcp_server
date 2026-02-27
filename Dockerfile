FROM python:3.10-slim

WORKDIR /app

# Устанавливаем системные утилиты, необходимые для инструментов (lsof, postgres client)
RUN apt-get update && apt-get install -y \
    lsof \
    net-tools \
    curl \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*


# Копируем проект
COPY . /app/

# Устанавливаем зависимости и сам пакет через pip (poetry не ставим ради простоты демо)
RUN pip install --no-cache-dir build && \
    pip install -e .

# Слушаем порт 8000
EXPOSE 8000

# Создаем скрипт запуска и выдаем права
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Создаем не-root пользователя
RUN useradd -m devboostuser
RUN chown -R devboostuser:devboostgroup /app || chown -R devboostuser /app
USER devboostuser

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["serve"]
