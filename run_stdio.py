#!/usr/bin/env python3
import sys
import os

# Добавляем src в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from devboost.server import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
