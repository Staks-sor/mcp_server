from mcp.server.fastmcp import FastMCP
from devboost.core.config import settings

# Инициализируем сервер MCP
# Имя сервера будет отображаться в Inspector/Claude Desktop
mcp = FastMCP("DevBoost", dependencies=["pydantic", "psutil", "asyncpg", "pydantic-settings"])

# Импортируем модули инструментов.
# При импорте срабатывают декораторы @mcp.tool(), которые регистрируют функции в mcp-инстансе
import devboost.tools.env_doctor
import devboost.tools.db_profiler

def run():
    """Точка входа для запуска сервера через CLI."""
    print(f"[{mcp.name}] Starting DevBoost MCP Server...")
    mcp.run()
