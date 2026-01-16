# agent_learning/llms/openai_compatible_client.py 测试类

from agent_learning.llms.openai_compatible_client import OpenAICompatibleClient
import os
import time

from dotenv import load_dotenv
load_dotenv()

# 获取指定环境变量值
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")

# 创建 LLM Client
client = OpenAICompatibleClient()

if __name__ == "__main__":
    # 定义对话消息体
    messages = [
        {'role': 'user', 'content': '你好'}
    ]

    # 非流式调用并打印
    print("=" * 20 + "非流式调用" + "=" * 20)
    response = client.chat(model_id=LLM_MODEL_ID, messages=messages)
    print(f"{response}")


    # 流式调用并打印
    print("=" * 20 + "流式调用" + "=" * 20)
    response_stream = client.chat_stream(model_id=LLM_MODEL_ID, messages=messages)

    for content in response_stream:
        time.sleep(0.2)
        print(content, end="")