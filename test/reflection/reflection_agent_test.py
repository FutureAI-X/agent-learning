import os

from dotenv import load_dotenv
load_dotenv()

LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")

from agent_learning.llms.openai_compatible_client import OpenAICompatibleClient
from agent_learning.reflection.reflection_agent import ReflectionAgent

llm_client = OpenAICompatibleClient()
reflection_agent = ReflectionAgent(llm_client)

if __name__ == "__main__":
    task = "编写一个Python函数，找出1到n之间所有的素数 (prime numbers)。"
    reflection_agent.run(model_id=LLM_MODEL_ID, task=task)

