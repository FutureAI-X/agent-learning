from agent_learning.llms.openai_compatible_client import OpenAICompatibleClient
from agent_learning.plan_and_solve.plan_and_solve_agent import PlanAndSolveAgent

from dotenv import load_dotenv
load_dotenv()
import os

LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")

llm_client = OpenAICompatibleClient(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)
agent = PlanAndSolveAgent(llm_client)

if __name__ == "__main__":
    question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
    agent.run(LLM_MODEL_ID, question)