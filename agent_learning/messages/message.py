from typing import Literal, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

# 指定 message 的取值范围, 这是 OpenAI API 规范中的定义
MessageRole = Literal["system", "user", "assistant", "tool"]

class Message(BaseModel):
    role: MessageRole                           # 角色
    content: str                                # 内容
    timestamp: Optional[datetime] = None        # 时间戳
    metadata: Optional[Dict[str, Any]] = None   # 元数据

    def __init__(self, role: MessageRole, content: str, **kwargs):
        super().__init__(
            role=role,
            content=content,
            timestamp=kwargs.get('timestamp', datetime.now()),
            metadata=kwargs.get('metadata', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换成 OpenAI API 标准的字典格式"""
        return {
            'role': self.role,
            'content': self.content,
        }

    def __str__(self):
        """调用print(object)会自动调用此方法"""
        return f'[{self.role}] {self.content}'

if __name__ == '__main__':
    message = Message("system", "你是一个有用的助手")
    print(message)
    print(message.to_dict())
    print(message.model_dump_json())