from openai import OpenAI

class OpenAICompatibleClient:
    """兼容 OpenAI 接口规范的 LLM 客户端"""
    def __init__(self, base_url: str, api_key:str, timeout: int = 60):
        """
        初始化
        Args:
            base_url:   API服务地址
            api_key:    API Key
            timeout:    超时时间(秒), 默认60秒
        """
        self.client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)

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

    def chat(self, model_id: str, messages, temperature: float = 0):
        """
        对话(非流式)

        Args:
            model_id:       模型ID
            messages:       消息列表
            temperature:    温度
        """
        try:
            response = self.client.chat.completions.create(
                model=model_id,
                messages=messages,
                temperature=temperature,
                stream=False,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise

    def chat_stream(self, model_id: str, messages, temperature: float = 0):
        """
        对话(非流式)

        Args:
            model_id:       模型ID
            messages:       消息列表
            temperature:    温度
        """
        try:
            response = self.client.chat.completions.create(
                model=model_id,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                yield content
        except Exception as e:
            raise