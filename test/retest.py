import re

text = "finish[华为最新的手机主要是Mate 70系列和Pura 70系列。Mate 70系列的主要卖点是顶级的全焦段拍照配置、专业摄影能力以及出色的户外抗摔设计；Pura 70系列则主打先锋影像技术，注重美学与创新设计。]"

# 使用正则表达式匹配 finish[...] 并提取中间内容
match = re.search(r'finish\[(.*)\]', text)

if __name__ == '__main__':
    if match:
        content = match.group(1)
        print(content)
    else:
        print("未找到匹配内容")