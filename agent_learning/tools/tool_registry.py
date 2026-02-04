from typing import Any, Callable
from agent_learning.tools.tool import Tool

class ToolRegistry:
    """工具注册表"""
    def __init__(self):
        self._tools: dict[str, Tool] = {}
        self._functions: dict[str, dict[str, Any]] = {}

    def register_tool(self, tool: Tool):
        """注册Tool"""
        self._tools[tool.name] = tool

    def register_function(self, name: str, description: str, func: Callable[[str], str]):
        pass