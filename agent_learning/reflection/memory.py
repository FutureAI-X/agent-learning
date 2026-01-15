from typing import List, Dict, Any, Optional

class Memory:
    def __init__(self):
        self.recodes: List[Dict[str, Any]] = []

    def add_recode(self, record_type: str, content: str):
        self.recodes.append({"type": record_type, "content": content})

    def get_trajectory(self) -> str:
        """
        将所有记忆记录格式化为一个连贯的字符串文本，用于构建提示词。
        """
        trajectory_parts = []
        for recode in self.recodes:
            recode_type = recode["type"]
            if recode_type == "execution":
                trajectory_parts.append(f"--- 上一轮尝试(代码) ---\n{recode['content']}")
            elif recode_type == "reflection":
                trajectory_parts.append(f"--- 评审员反馈 ---\n{recode['content']}")
        return "\n\n".join(trajectory_parts)

    def get_last_execution(self) -> Optional[str]:
        for recode in reversed(self.recodes):
            if recode["type"] == "execution":
                return recode["content"]
        return None