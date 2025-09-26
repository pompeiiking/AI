# 导入必要的库
import os
from dotenv import load_dotenv
load_dotenv(override=True)

# 导入langchain相关模块
from langchain.chat_models import init_chat_model

# 创建DeepSeek聊天模型实例
# model = init_chat_model(model="deepseek-chat", model_provider="deepseek")

# # 方法1：直接使用模型（返回完整响应对象）
# print("=== 方法1：直接使用模型 ===")
# question = "你好，你是谁？"
# result = model.invoke(question)
# print("完整响应对象：")
# print(result)
# print("\n只显示回答内容：")
# print(result.content)

from langchain_core.output_parsers import StrOutputParser

# model = init_chat_model(model="deepseek-chat",model_provider="deepseek")
# basic_qa_chain = model | StrOutputParser()
# question = "你好，你是谁？"
# result = basic_qa_chain.invoke(question)
# print("纯文本回答：")
# print(result)

from langchain.prompts import ChatPromptTemplate

model = init_chat_model(model="deepseek-chat", model_provider="deepseek")
# prompt = ChatPromptTemplate.from_messages([
#     ("system","你是一个AI助手，你叫deepseek-chat，我正在测试你的正常功能,请根据问题进行判断，如果问题正确，请返回True，如果问题错误，请返回False"),
#     ("user","这是我的问题：{topic}")
# ])

# bool_qa_chain = prompt | model | StrOutputParser()
# question = "1+1 = 2"
# result = bool_qa_chain.invoke(question)
# print(result)

from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema,StructuredOutputParser

schema =[
    ResponseSchema(name="name", description="用户的姓名"),
    ResponseSchema(name="age", description="用户的年龄"),
    ResponseSchema(name="gender", description="用户的性别")
]
parser = StructuredOutputParser.from_response_schemas(schema)

prompt = PromptTemplate.from_template(
    "请根据以下内容提取用户信息，并返回一个json格式：{input}\n{format_instructions}"                                      
)

chain = (
    prompt.partial(format_instructions=parser.get_format_instructions())
    | model
    | parser
)

result = chain.invoke({"input":"用户叫神四，今年37岁，是一个忍者"})
print(result)
