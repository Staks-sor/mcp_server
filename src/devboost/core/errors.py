class DevBoostError(Exception):
    """Базовый класс для ошибок DevBoost."""
    pass

class DatabaseConnectionError(DevBoostError):
    """Ошибка при подключении к базе данных (неверный URL или БД недоступна)."""
    pass

class QueryExecutionError(DevBoostError):
    """Ошибка при выполнении SQL-запроса (например, синтаксическая ошибка)."""
    pass

class ProcessManagementError(DevBoostError):
    """Ошибка при управлении системными процессами."""
    pass
