from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os

class OpenAICompatibleClient:
    """兼容 OpenAI 接口规范的 LLM 客户端"""
    def __init__(self, provider: str = None, timeout: int = 60):
        """
        初始化
        Args:
            base_url:   API服务地址
            api_key:    API Key
            timeout:    超时时间(秒), 默认60秒
        """
        if not provider:
            provider = os.getenv("LLM_DEFAULT_PROVIDER")
        base_url = os.getenv(f"LLM_BASE_URL_{provider.upper()}")
        api_key = os.getenv(f"LLM_API_KEY_{provider.upper()}")
        self.provider = provider
        self.client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)
        self.default_model_id = os.getenv(f"LLM_DEFAULT_MODEL_ID_{provider.upper()}")

    def generate(self, model_id: str, system_prompt: str, user_prompt: str):
        try:
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ]
            response = self.chat(model_id=model_id, messages=messages)
            return response
        except Exception as e:
            raise

    def chat(self, model_id: str, messages: list, temperature: float = 0):
        """
        对话(非流式)

        Args:
            model_id:       模型ID
            messages:       消息列表
            temperature:    温度
        """
        try:
            response = self.client.chat.completions.create(
                model=model_id if model_id else self.default_model_id,
                messages=messages,
                temperature=temperature,
                stream=False,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise

    def chat_stream(self, model_id: str, messages: list, temperature: float = 0):
        """
        对话(非流式)

        Args:
            model_id:       模型ID
            messages:       消息列表
            temperature:    温度
        """
        try:
            response = self.client.chat.completions.create(
                model=model_id if model_id else self.default_model_id,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                yield content
        except Exception as e:
            raise

if __name__ == "__main__":
    client = OpenAICompatibleClient(provider = 'a')
    print(client.client.base_url)