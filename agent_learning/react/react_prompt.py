REACT_PROMPT_TEMPLATE="""
你可以调用工具来解决用户的问题

可用工具
{tools}

输出要求
必须是以下格式:
Thought: 你的思考过程
Action: 你要采取的行动


关于Action的要求
必须是以下格式之一:
- `tool_name[tool_input]`: 调用一个可用的工具
- `finish[最终答案]`

问题
{question}

对话历史
{history}
"""