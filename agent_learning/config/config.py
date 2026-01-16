from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

class Config(BaseModel):
    """配置类：从环境变量中获取配置，以便复用"""
    # LLM 相关配置
    temperature: float = 0.7

    # 系统配置

    # 其他配置

    @classmethod
    def from_env(cls) -> 'Config':
        """从环境变量创建对象"""
        return cls(
            temperature=float(os.getenv("TEMPERATURE", '0.7')),
        )

if __name__ == '__main__':
    config = Config()
    print(config.model_dump())
    print(config.temperature)