from agent_learning.llms.openai_compatible_client import OpenAICompatibleClient

from agent_learning.reflection.reflection_prompt import INITIAL_PROMPT_TEMPLATE, REFLECT_PROMPT_TEMPLATE, REFINE_PROMPT_TEMPLATE
from agent_learning.reflection.memory import Memory


def print_task(task: str):
    print(f"--- 开始执行任务 ---")
    print(task)
    print("\n")


class ReflectionAgent:
    def __init__(self, llm_client: OpenAICompatibleClient, max_step: int = 10):
        self.llm_client = llm_client
        self.max_step = max_step

    def run(self, model_id: str, task: str):
        print_task(task)

        memory = Memory()

        # 1. 让模型先生成一次答案
        print("--- 初始执行 ---")
        initial_prompt = INITIAL_PROMPT_TEMPLATE.format(task=task)
        messages = [{'role': 'user', 'content': initial_prompt}]
        initial_response = self.llm_client.chat(model_id=model_id, messages=messages)
        memory.add_recode(record_type='execution', content=initial_response)
        print(initial_response + "\n")

        # 2. 反思与优化
        for i in range(self.max_step):
            print(f"--- 第{i+1}次迭代 ---")
            last_code = memory.get_last_execution()
            # 反思
            reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(task=task, code=last_code)
            messages = [{'role': 'user', 'content': reflect_prompt}]
            reflect_response = self.llm_client.chat(model_id=model_id, messages=messages)
            memory.add_recode(record_type='reflection', content=reflect_response)
            print(f"【反思】\n{reflect_response}\n")

            if "无需改进" in reflect_response:
                break

            # 优化
            refine_prompt = REFINE_PROMPT_TEMPLATE.format(task=task, last_code_attempt=last_code, feedback=reflect_response)
            messages = [{'role': 'user', 'content': refine_prompt}]
            refine_response = self.llm_client.chat(model_id=model_id, messages=messages)
            memory.add_recode(record_type='execution', content=refine_response)
            print(f"【优化】\n{refine_response}\n")

        final_response = memory.get_last_execution()
        print(f"--- 最终答案 ---\n{final_response}")
        return final_response

