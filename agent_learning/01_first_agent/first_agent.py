from agent_learning.utils.log_util import setup_logging
setup_logging()

from agent_learning.llms.openai_compatible_client import OpenAICompatibleClient
from agent_learning.tools.get_weather import get_weather
from agent_learning.tools.search_attraction import get_attraction

from dotenv import load_dotenv
load_dotenv()

import re
import os

import logging
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("LLM_BASE_URL")
API_KEY = os.getenv("LLM_API_KEY")
MODEL_ID = os.getenv("LLM_MODEL_ID")

llm = OpenAICompatibleClient(base_url=BASE_URL, api_key=API_KEY)

AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

# 行动格式:
你的回答必须严格遵循以下格式。首先是你的思考过程，然后是你要执行的具体行动，每次回复只输出一对Thought-Action：
Thought: [这里是你的思考过程和下一步计划]
Action: [这里是你要调用的工具，格式为 function_name(arg_name="arg_value")]

# 任务完成:
当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `finish(answer="...")` 来输出最终答案。

请开始吧！
"""

available_tools = {
    'get_weather': get_weather,
    'get_attraction': get_attraction,
}

question = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f'用户输入：{question}']

def main():
    for i in range(5):
        logger.info(f"============= 第{i}循环 =============")
        # 1. 构建用户输入
        user_prompt = "\n".join(prompt_history)
        # 2. 调用模型
        llm_output = llm.generate(model_id=MODEL_ID, system_prompt=AGENT_SYSTEM_PROMPT, user_prompt=user_prompt)
        # 3. 解析模型输出
        match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output,
                          re.DOTALL)
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm_output = truncated
                logger.info("已截断多余的 Thought-Action 对")
        logger.info(f"模型输出：{llm_output}")
        prompt_history.append(llm_output)
        # 4. 根据输出执行操作
        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            logger.error("解析错误:模型输出中未找到 Action。")
            break
        action_str = action_match.group(1).strip()

        if action_str.startswith("finish"):
            final_answer = re.search(r'finish\(answer="(.*)"\)', action_str).group(1)
            logger.info(f"任务完成，最终答案: {final_answer}")
            break

        tool_name = re.search(r"(\w+)\(", action_str).group(1)
        args_str = re.search(r"\((.*)\)", action_str).group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

        if tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"

        # 3.4. 记录观察结果
        observation_str = f"Observation: {observation}"
        prompt_history.append(observation_str)
        logger.info(observation_str)

        logger.info(f"====================================")

if __name__ == "__main__":
    main()