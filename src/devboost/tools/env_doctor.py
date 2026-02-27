from mcp.server.fastmcp import Context
from ..server import mcp
from ..services.sys_process import get_system_versions, kill_process_on_port
from typing import List, Dict, Any

@mcp.tool()
async def check_versions(tools: List[str], ctx: Context) -> str:
    """
    Получает текущие версии установленных разработчиком инструментов.
    Полезно для диагностики проблем с окружением и "у меня не работает".
    
    Args:
        tools: Список программ для проверки (например: ['node', 'python', 'docker'])
    """
    ctx.info(f"Checking versions for: {tools}")
    
    if not tools:
        return "List of tools cannot be empty."
        
    results = await get_system_versions(tools)
    
    # Форматируем вывод для AI-агента
    report = ["System Versions Report:", "=" * 25]
    for tool, data in results.items():
        if data["installed"]:
            report.append(f"✅ {tool}: {data['version']}")
        else:
            report.append(f"❌ {tool}: Not found ({data.get('error', 'unknown error')})")
            
    return "\n".join(report)

@mcp.tool()
async def kill_port_hog(port: int, ctx: Context) -> str:
    """
    Находит и убивает процесс, который занимает указанный порт.
    Полезно при ошибках EADDRINUSE при локальной разработке.
    Безопасно: убивает только процессы текущего пользователя.
    
    Args:
        port: Номер порта (например: 3000, 8080)
    """
    ctx.info(f"Attempting to free port {port}")
    
    if port < 1024:
        return f"Warning: Port {port} is a privileged port. Cannot kill processes on privileged ports for security reasons."
        
    try:
        result = kill_process_on_port(port)
        if result["success"]:
            killed = result["killed"]
            details = ", ".join([f"{p['name']} (PID: {p['pid']})" for p in killed])
            return f"✅ Successfully freed port {port}. Killed processes: {details}"
        else:
            return f"ℹ️ {result['message']}"
    except Exception as e:
        ctx.error(f"Error freeing port: {str(e)}")
        return f"❌ Failed to free port {port}: {str(e)}"
