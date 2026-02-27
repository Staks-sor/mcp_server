-- Создаем таблицу без индексов для демонстрации Seq Scan
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Генерируем тестовые данные (100,000 строк)
INSERT INTO users (email, first_name, last_name)
SELECT 
    'user_' || generate_series || '@example.com',
    'First_' || generate_series,
    'Last_' || generate_series
FROM generate_series(1, 100000);

-- Создаем конкретного пользователя для поиска в демо
INSERT INTO users (email, first_name, last_name) 
VALUES ('target@mcp.test', 'Target', 'User');
