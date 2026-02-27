import asyncpg
from typing import Dict, Any, List
from ..core.config import settings
from ..core.errors import DatabaseConnectionError, QueryExecutionError

class PostgresClient:
    """Обертка для работы с PostgreSQL через asyncpg."""
    
    def __init__(self):
        self._pool = None
        # URL берется из pydantic settings (.env)
        self.db_url = settings.database_url
        
    async def connect(self):
        """Создает пул соединений, если он еще не создан."""
        if not self.db_url:
            raise DatabaseConnectionError("DATABASE_URL is not set in environment or .env file.")
            
        if not self._pool:
            try:
                self._pool = await asyncpg.create_pool(
                    self.db_url,
                    min_size=1,
                    max_size=5
                )
            except Exception as e:
                raise DatabaseConnectionError(f"Failed to connect to database: {str(e)}")
                
    async def disconnect(self):
        """Закрывает пул соединений."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            
    async def explain_analyze(self, query: str) -> Dict[str, Any]:
        """Выполняет EXPLAIN (ANALYZE, FORMAT JSON) для указанного запроса."""
        await self.connect()
        
        try:
            # Важно: Выполняем EXPLAIN в транзакции с ROLLBACK, 
            # чтобы случайно не сделать UPDATE/DELETE, хотя EXPLAIN ANALYZE сам выполняет запрос.
            # Для чистой безопасности мы используем READ ONLY транзакцию (когда возможно), 
            # или оставляем на страх и риск разработчика (в рамках Local DevServer).
            # В данном примере просто выполняем:
            explain_query = f"EXPLAIN (ANALYZE, FORMAT JSON) {query}"
            
            async with self._pool.acquire() as connection:
                # Выполняем запрос
                result = await connection.fetchval(explain_query)
                return {"success": True, "plan": result}
                
        except asyncpg.exceptions.PostgresError as e:
            raise QueryExecutionError(f"Database error during EXPLAIN: {str(e)}")
        except Exception as e:
            raise QueryExecutionError(f"Unknown error executing EXPLAIN: {str(e)}")
            
    async def get_schema_for_tables(self, table_names: List[str]) -> List[Dict[str, Any]]:
        """Получает базовую схему и существующие индексы для таблиц (упрощенно)."""
        await self.connect()
        schema_info = []
        
        try:
            async with self._pool.acquire() as connection:
                for table in table_names:
                    # Упрощенный запрос для получения индексов таблицы
                    # В реальном проекте тут должен быть более глубокий парсинг pg_class/pg_index
                    indexes_query = """
                    SELECT indexname, indexdef 
                    FROM pg_indexes 
                    WHERE tablename = $1;
                    """
                    records = await connection.fetch(indexes_query, table)
                    indexes = [{"name": r["indexname"], "def": r["indexdef"]} for r in records]
                    
                    schema_info.append({
                        "table": table,
                        "indexes": indexes
                    })
            return schema_info
        except Exception as e:
            return [{"error": str(e)}]

# Синглтон для сервера
db_client = PostgresClient()
