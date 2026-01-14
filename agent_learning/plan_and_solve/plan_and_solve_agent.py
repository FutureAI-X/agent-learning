from agent_learning.llms.openai_compatible_client import OpenAICompatibleClient
from agent_learning.plan_and_solve.planner import Planner
from agent_learning.plan_and_solve.executor import Executor


class PlanAndSolveAgent:
    def __init__(self, llm_client: OpenAICompatibleClient):
        self.planner = Planner(llm_client)
        self.executor = Executor(llm_client)

    def run(self, model_id:str, question: str):
        self.print_qustion(question)

        plan = self.planner.plan(model_id, question)
        if not plan:
            print("错误：未生成方案")
        self.planner.print_plan(plan)

        final_answer = self.executor.execute(model_id, question, plan)
        self.print_answer(final_answer)
        return final_answer

    def print_qustion(self, question: str):
        print("--- 开始处理问题 ---")
        print(f"问题：{question}\n")

    def print_answer(self, answer: str):
        print("\n--- 任务完成 ---")
        print(f"最终答案：{answer}")