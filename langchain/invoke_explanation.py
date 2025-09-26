# invoke方法详细解释
import os
from dotenv import load_dotenv
load_dotenv(override=True)

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

# 创建模型
model = init_chat_model(model="deepseek-chat", model_provider="deepseek")

print("=== invoke方法详细解释 ===\n")

# 1. 直接对模型使用invoke
print("1. 直接对模型使用invoke：")
question = "你好，你是谁？"
result = model.invoke(question)
print(f"输入：{question}")
print(f"输出类型：{type(result)}")
print(f"输出内容：{result.content}")
print("-" * 50)

# 2. 对处理链使用invoke
print("\n2. 对处理链使用invoke：")
basic_chain = model | StrOutputParser()
result = basic_chain.invoke(question)
print(f"输入：{question}")
print(f"输出类型：{type(result)}")
print(f"输出内容：{result}")
print("-" * 50)

# 3. 对带提示模板的处理链使用invoke
print("\n3. 对带提示模板的处理链使用invoke：")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个AI助手，请用简洁的语言回答问题"),
    ("user", "问题：{topic}")
])

chain_with_prompt = prompt | model | StrOutputParser()
result = chain_with_prompt.invoke({"topic": "什么是Python？"})
print(f"输入：{{'topic': '什么是Python？'}}")
print(f"输出类型：{type(result)}")
print(f"输出内容：{result}")
print("-" * 50)

# 4. 布尔判断示例
print("\n4. 布尔判断示例：")
bool_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个AI助手，请根据问题进行判断，如果问题正确，请返回True，如果问题错误，请返回False"),
    ("user", "这是我的问题：{topic}")
])

bool_chain = bool_prompt | model | StrOutputParser()
result = bool_chain.invoke({"topic": "1+1 = 2"})
print(f"输入：{{'topic': '1+1 = 2'}}")
print(f"输出：{result}")
