from agent_learning.tools.tool_executor import ToolExecutor
from agent_learning.tools.get_weather import get_weather
from agent_learning.tools.search_serpapi import search

tool_executor = ToolExecutor()


if __name__ == '__main__':
    tool_executor.register_tool(name="get_weather", description="获取天气", func=get_weather)
    tool_executor.register_tool(name="search", description="搜索", func=search)

    available_tools = tool_executor.get_available_tools()
    print("=" * 30 + f"\n【可用工具清单】\n{available_tools}")

    tool_search = tool_executor.get_tool('search')
    tool_weather = tool_executor.get_tool('get_weather')
    print("=" * 30 + "\n【获取指定工具】")
    print(type(tool_search))
    print(type(tool_weather))