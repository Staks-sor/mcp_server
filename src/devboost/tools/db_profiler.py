from mcp.server.fastmcp import Context
from ..server import mcp
from ..services.db_client import db_client
from ..core.errors import DevBoostError
from typing import List

@mcp.tool()
async def explain_query(query: str, ctx: Context) -> str:
    """
    Профилирует SQL-запрос в PostgreSQL, выполняя EXPLAIN ANALYZE и возвращая план выполнения.
    Помогает найти узкие места в базе данных, такие как Seq Scan.
    Сервер сам использует настроенный DATABASE_URL, его не нужно передавать.
    
    Args:
        query: SQL-запрос для анализа (например, "SELECT * FROM users WHERE email='test@example.com'")
    """
    # Базовая защита от инъекций (для прототипа)
    if not query.strip().upper().startswith(("SELECT", "WITH")):
        return "❌ Error: explain_query only supports SELECT or WITH queries to prevent accidental data modification."
        
    ctx.info(f"Analyzing query starting with: {query[:50]}...")
    
    try:
        result = await db_client.explain_analyze(query)
        if result["success"]:
            # В реальном плагине тут можно использовать LLM или статический анализ для парсинга JSON
            # Для прототипа вернем сырой вывод, так как Claude отлично умеет читать EXPLAIN JSON
            return f"✅ Query Explain Plan:\n```json\n{result['plan']}\n```\n\nAnalyze this plan and look for 'Seq Scan' on large tables."
        else:
            return "❌ Failed to retrieve explanation plan."
    except DevBoostError as e:
        ctx.error(f"Database Error: {str(e)}")
        return f"❌ Database Execution Error: {str(e)}\nMake sure the DATABASE_URL environment variable is set correctly."

@mcp.tool()
async def suggest_index(tables: List[str], ctx: Context) -> str:
    """
    Анализирует указанные таблицы и показывает текущие индексы. 
    Полезно вызывать после explain_query для понимания структуры таблиц, участвующих в запросе.
    
    Args:
        tables: Список названий таблиц в БД (например, ['users', 'orders'])
    """
    ctx.info(f"Fetching index schema for tables: {tables}")
    
    try:
        schemas = await db_client.get_schema_for_tables(tables)
        
        report = ["📋 Database Index Schema Report:", ""]
        for schema in schemas:
            if "error" in schema:
                report.append(f"❌ Error fetching schema: {schema['error']}")
                continue
                
            table_name = schema["table"]
            indexes = schema["indexes"]
            
            report.append(f"Table `{table_name}`:")
            if not indexes:
                report.append("  No indexes found (except maybe primary key, depending on DB settings).")
            else:
                for idx in indexes:
                    report.append(f"  - {idx['name']}: \n      {idx['def']}")
            report.append("")
            
        report.append("\n💡 How to use this: Match these existing indexes against the Seq Scans from `explain_query`.")
        report.append("If a column is frequently used in WHERE or JOIN but lacks an index, suggest `CREATE INDEX ...` via chat.")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"❌ Error fetching schema: {str(e)}"
