import os
from dotenv import load_dotenv
load_dotenv(override=True)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

from openai import OpenAI
client = OpenAI(api_key=DEEPSEEK_API_KEY,base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role":"system","content":"你是一个AI助手，你叫deepseek-chat，我正在测试你的正常功能"},
        {"role":"user","content":"你好，你是否成功启动"}
    ],
)

print(response.choices[0].message.content)