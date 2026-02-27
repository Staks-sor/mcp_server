import asyncio
import platform
import psutil
import subprocess
from typing import Dict, Any, Optional
from ..core.errors import ProcessManagementError

async def get_system_versions(tools: list[str]) -> Dict[str, Any]:
    """
    Получает локальные версии указанных инструментов (node, python, docker и т.д.)
    """
    results = {}
    for tool in tools:
        try:
            # Используем разные команды в зависимости от инструмента
            cmd = [tool, "--version"]
            if tool == "docker":
                cmd = ["docker", "-v"]
                
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            
            if process.returncode == 0:
                # Очищаем вывод (например "Python 3.10.12\n" -> "Python 3.10.12")
                results[tool] = {"installed": True, "version": stdout.decode().strip()}
            else:
                results[tool] = {"installed": False, "error": "Command failed"}
        except FileNotFoundError:
            results[tool] = {"installed": False, "error": "Not found in PATH"}
        except Exception as e:
            results[tool] = {"installed": False, "error": str(e)}
            
    return results

def kill_process_on_port(port: int) -> Dict[str, Any]:
    """
    Находит процесс, занимающий указанный порт, и убивает его.
    ВНИМАНИЕ: Убивает только процессы текущего пользователя (security).
    """
    import getpass
    current_user = getpass.getuser()
    
    try:
        killed_processes = []
        # Проходим по всем процессам с помощью psutil
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                # Пропускаем процессы других пользователей
                if proc.info['username'] != current_user and current_user != 'root':
                    continue
                    
                connections = proc.connections()
                for conn in connections:
                    # Ищем LISTEN порт
                    if conn.status == 'LISTEN' and conn.laddr.port == port:
                        proc_name = proc.info['name']
                        proc_id = proc.info['pid']
                        proc.kill()
                        killed_processes.append({"pid": proc_id, "name": proc_name})
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
                
        if killed_processes:
            return {"success": True, "killed": killed_processes, "port": port}
        else:
            return {"success": False, "message": f"No process found listening on port {port}"}
            
    except Exception as e:
        raise ProcessManagementError(f"Failed to manage processes: {str(e)}")
