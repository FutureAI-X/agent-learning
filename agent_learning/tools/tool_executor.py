from typing import Dict, Any, Callable

class ToolExecutor:
    """工具执行器：负责管理和执行工具"""

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name:str, description:str, func: Callable):
        """工具注册

        Args:
            name            工具名称
            description     工具描述
            func            可调用的函数
        """
        self.tools[name] = {'description': description, 'func': func}
        print(f"工具注册成功：{name}")

    def get_tool(self, name: str) -> Callable | None:
        """获取可执行的工具函数

        Args:
            name    工具名称
        """
        return self.tools.get(name, {}).get('func', None)

    def execute_tool(self, tool_name:str, tool_input:str):
        tool_function = self.get_tool(tool_name)
        if not tool_function:
            return f"错误：未找到工具{tool_name}"
        else:
            return tool_function(tool_input)

    def get_available_tools(self):
        tools = [f"{name}: {info.get('description')}" for name, info in self.tools.items()]
        return '\n'.join(tools)