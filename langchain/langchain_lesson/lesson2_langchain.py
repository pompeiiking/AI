#lesson_1 
import os #这是os库，用于操作系统
from dotenv import load_dotenv #这是环境变量库，用于加载环境变量
from langchain.chat_models import init_chat_model #这是langchain的模型库，用于调用大模型的api
from langchain_core.messages import SystemMessage,HumanMessage #这是message库，用于创建消息

load_dotenv() #加载环境变量
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

model = init_chat_model(model_name="deepseek-chat",api_key=deepseek_api_key)

messages = [
    SystemMessage(content="你是一个帮助用户解决问题的助手。"),
    HumanMessage(cotent="你好")
]

result = model.invoke(messages)
print(result.content)



