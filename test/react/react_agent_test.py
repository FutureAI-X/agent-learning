from agent_learning.llms.openai_compatible_client import OpenAICompatibleClient
from agent_learning.tools.tool_executor import ToolExecutor
from agent_learning.tools.search_serpapi import search, SEARCH_DESCRIPTION
from agent_learning.react.react_agent import ReactAgent

from dotenv import load_dotenv
load_dotenv()

import os
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")

llm_client = OpenAICompatibleClient()
tool_executor = ToolExecutor()
tool_executor.register_tool(name='search', description=SEARCH_DESCRIPTION, func=search)
react_agent = ReactAgent(llm_client, tool_executor)



if __name__ == "__main__":
    react_agent.run(question="华为最新的手机是哪一款？它的主要卖点是什么？")