from agent_learning.react.react_prompt import REACT_PROMPT_TEMPLATE
from agent_learning.tools.tool_executor import ToolExecutor
from agent_learning.llms.openai_compatible_client import OpenAICompatibleClient
from dotenv import load_dotenv
load_dotenv()

import re
import os
MODEL_ID = os.getenv("LLM_MODEL_ID")

class ReactAgent:
    def __init__(self, llm_client: OpenAICompatibleClient, tool_executor: ToolExecutor, max_step: int = 3):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_step = max_step
        self.history = []
        pass

    # (这些方法是 ReActAgent 类的一部分)
    def _parse_output(self, text: str):
        """解析LLM的输出，提取Thought和Action。"""
        thought_match = re.search(r'^Thought:\s*(.*?)(?=\nAction:|\Z)', text, re.DOTALL | re.MULTILINE)
        action_match = re.search(r'^Action:\s*(.*?)(?=\nThought:|\Z)', text, re.DOTALL | re.MULTILINE)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        """解析Action字符串，提取工具名称和输入。"""
        match = re.match(r"(\w+)\[(.*)\]", action_text)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def run(self, question: str):
        self.history = []
        for i in range(self.max_step):
            print("=" * 20)
            # 1. 构建本次循环的用户消息
            history = '\n'.join(self.history)
            user_prompt = REACT_PROMPT_TEMPLATE.format(
                tools=self.tool_executor.get_available_tools(),
                history=history,
                question=question
            )
            messages = [{'role':'user', 'content':user_prompt}]

            # 2. 调用LLM
            response = self.llm_client.chat(model_id=MODEL_ID, messages=messages)

            if not response:
                raise RuntimeError("模型调用失败")

            # 3. 解析输出
            thought, action = self._parse_output(response)
            if thought:
                print(f"Thought: {thought}")

            if not action:
                print(f"错误：未解析出有效的Action, 流程终止")
                break

            # 4. 执行Action
            print(f"Action: {action}")
            # 4.1 先检查是否为 finish 指令，如果
            if action.startswith("finish"):
                final_answer = re.search(r'finish\[(.*)\]', action).group(1)
                print(f"答案：{final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                continue

            observation = self.tool_executor.execute_tool(tool_name, tool_input)
            print(f"Observation: {observation}")

            # 5. 历史消息整合
            # 将当前步骤的 Action 与 Observation 添加到历史中，在下一轮对话中就知道之前的行动与结果
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

