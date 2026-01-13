# 兼容 OpenAI 接口规范的 LLM 客户端

from openai import OpenAI

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAICompatibleClient:
    def __init__(self, base_url: str, api_key:str, model_id: str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_id = model_id

    def generate(self, system_prompt: str, user_prompt: str):
        try:
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ]
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                stream=False
            )
            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            logger.exception("调用LLM时发生异常")
            raise